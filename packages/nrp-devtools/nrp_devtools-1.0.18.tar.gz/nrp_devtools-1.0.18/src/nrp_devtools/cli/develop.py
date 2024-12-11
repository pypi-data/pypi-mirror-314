import click

from ..commands.develop import Runner
from ..commands.develop.controller import run_develop_controller
from ..commands.ui.link_assets import copy_assets_to_webpack_build_dir
from ..commands.utils import make_step
from ..config import OARepoConfig
from .base import command_sequence, nrp_command
from .check import check_commands
from ..pypi_proxy.proxy import start_pypi_proxy


@nrp_command.command(name="develop")
@click.option(
    "--extra-library",
    "-e",
    "local_packages",
    multiple=True,
    help="Path to a local package to install",
)
@click.option(
    "--checks/--skip-checks",
    default=True,
    help="Check the environment before starting (default is to check, disable to get a faster startup)",
)
@click.option(
    "--shell/--no-shell",
    default=False,
    help="Start the new development environment that is based on "
         "shell script and does not suffer with problems with stdout/stderr",
)
@command_sequence()
def develop_command(
    *, config: OARepoConfig, local_packages=None, checks=True, shell=False, **kwargs
):
    """Starts the development environment for the repository."""
    context = {}
    start_pypi_proxy(config.pypi_proxy_target)
    commands = [
        *(check_commands(context, config, local_packages, fix=True) if checks else ()),
        copy_assets_to_webpack_build_dir,
    ]
    if not shell:
        runner = Runner(config)
        commands.extend([
            make_step(
                lambda config=None, runner=None: runner.start_python_server(
                    development_mode=True
                ),
                runner=runner,
            ),
            make_step(
                lambda config=None, runner=None: runner.start_webpack_server(),
                runner=runner,
            ),
            make_step(
                lambda config=None, runner=None: runner.start_file_watcher(), runner=runner
            ),
            make_step(run_develop_controller, runner=runner, development_mode=True),
        ])
    return commands
