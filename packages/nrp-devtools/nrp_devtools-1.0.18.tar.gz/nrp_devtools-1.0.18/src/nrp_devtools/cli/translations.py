import click
from oarepo_tools.make_translations import main

from ..config import OARepoConfig
from .base import command_sequence, nrp_command


@nrp_command.command(name="translations")
@command_sequence()
@click.pass_context
def translations_command(
    ctx, *, config: OARepoConfig, local_packages=None, checks=True, **kwargs
):
    """Create translations for the repository.

    This command will create source translation files inside the i18n/translations directory.
    Edit the .po files there and run nrp translations again to compile the translations.

    To change the translated languages, edit the oarepo.yaml file.
    """
    ctx.invoke(main, config_path=config.config_file)
