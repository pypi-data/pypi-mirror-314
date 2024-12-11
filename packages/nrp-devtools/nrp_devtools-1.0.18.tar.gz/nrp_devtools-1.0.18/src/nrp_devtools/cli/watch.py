import click

from ..commands.develop import Runner
from ..commands.develop.controller import run_develop_controller
from ..commands.develop.runner import FileCopier
from ..commands.ui.link_assets import copy_assets_to_webpack_build_dir
from ..commands.utils import make_step
from ..config import OARepoConfig
from .base import command_sequence, nrp_command
from .check import check_commands


@nrp_command.command(name="watch")
@command_sequence()
def watch_command(
    *, config: OARepoConfig, **kwargs
):
    """Starts the file watcher that copies UI files to invenio instance."""
    def run_copier(config):
        copier = FileCopier(config)
        copier.watcher.join()

    return [
        make_step(run_copier)
    ]
