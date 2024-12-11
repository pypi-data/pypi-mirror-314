import sys
from pathlib import Path

import click

from ..commands.initialize import initialize_repository
from ..config import OARepoConfig
from ..config.repository_config import RepositoryConfig
from ..config.wizard import ask_for_configuration
from .base import command_sequence, nrp_command


@nrp_command.command(name="initialize")
@click.option(
    "--initial-config",
    default=None,
    help="Initial configuration file",
    type=click.Path(exists=True),
)
@click.option(
    "--no-input",
    default=None,
    help="Do not ask for input, use the initial config only",
    is_flag=True,
)
@command_sequence(
    repository_dir_as_argument=True, repository_dir_must_exist=False, save=True
)
def initialize_command(
    *, repository_dir, config: OARepoConfig, verbose, initial_config, no_input
):
    """
    Initialize a new nrp project. Note: the project directory must be empty.
    """
    if repository_dir.exists() and len(list(repository_dir.iterdir())) > 0:
        click.secho(
            f"Project directory {repository_dir} must be empty", fg="red", err=True
        )
        sys.exit(1)

    def initialize_step(config: OARepoConfig):
        if initial_config:
            config.load(Path(initial_config))

        if not no_input:
            click.secho(
                """Please answer a few questions to configure your repository."""
            )
            config.repository = ask_for_configuration(
                config,
                RepositoryConfig,
            )

        initialize_repository(config)
        click.secho(
            f"""
Your repository is now initialized. 

You can start the repository in development mode
via ./nrp develop and head to https://127.0.0.1:5000/
to check that everything has been installed correctly.

Then add metadata models via ./nrp model add <model_name>,
edit the model and compile it via ./nrp model compile <model_name>.

Add jinjax template pages via ./nrp ui page create <page_name>
and model ui pages via ./nrp ui model create <model_name>.
""",
            fg="green",
        )

    return (initialize_step,)
