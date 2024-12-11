"""
This is the main entry point for the nrp devtools command line interface.
"""

import functools
import sys
from pathlib import Path
from typing import Any, Callable, Dict, Union

import click

from nrp_devtools.commands.utils import run_steps
from nrp_devtools.config import OARepoConfig


@click.group()
def nrp_command(**kwargs):
    """NRP devtools command line interface."""


def command_sequence(
    repository_dir_must_exist=True,
    repository_dir_as_argument=False,
    continue_on_errors: Union[
        bool, Callable[[OARepoConfig, Dict[str, Any]], bool]
    ] = False,
    save: bool = False,
):
    def wrapper(command):
        command = click.option(
            "--override-config",
            multiple=True,
            help="Override configuration values. "
            "This parameter might be repeated, "
            "and the TEXT is <config-key>=<config-value>. "
            "Only venv_dir and invenio_instance_path are supported.",
        )(command)
        command = click.option(
            "--verbose", "-v", is_flag=True, help="Enables verbose mode."
        )(command)
        command = click.option("--step", help="Run only this step", multiple=True)(
            command
        )
        command = click.option(
            "--dry-run",
            is_flag=True,
            help="Show steps that would be run and exit.",
        )(command)
        command = click.option(
            "--steps",
            "show_steps",
            is_flag=True,
            help="Show steps that would be run and exit.",
        )(command)
        if repository_dir_as_argument:
            command = click.argument(
                "repository_dir",
                type=click.Path(exists=repository_dir_must_exist),
            )(command)
        else:
            command = click.option(
                "--repository-dir",
                "-d",
                default=".",
                help="Repository directory (default is the current directory).",
                type=click.Path(exists=False),
            )(command)

        @functools.wraps(command)
        def proxied(*args, **kwargs):
            repository_dir = kwargs["repository_dir"]
            steps = kwargs.pop("step", None)
            dry_run = kwargs.pop("dry_run", False) or kwargs.pop("show_steps", False)
            if repository_dir:
                kwargs["repository_dir"] = repository_dir = Path(
                    repository_dir
                ).resolve()

                if repository_dir_must_exist and not repository_dir.exists():
                    click.secho("Project directory must exist", fg="red")
                    sys.exit(1)

            config = OARepoConfig(repository_dir)
            config.load()

            override_config = kwargs.pop("override_config", [])
            for override in override_config:
                _k, _v = [x.strip() for x in override.split("=", maxsplit=1)]
                config.overrides[_k] = _v

            # run the command
            step_commands = command(*args, config=config, **kwargs)
            if dry_run:
                click.secho("Steps that would be run:\n", fg="green")
                for idx, step_cmd in enumerate(step_commands):
                    click.secho(f"{idx+1:3d} {step_cmd.__name__}", fg="green")
                return
            elif step_commands:
                _continue_on_errors = (
                    continue_on_errors(config, kwargs)
                    if callable(continue_on_errors)
                    else continue_on_errors
                )

                run_steps(
                    config, steps, step_commands, continue_on_errors=_continue_on_errors
                )
            if save:
                config.save()

        return proxied

    return wrapper
