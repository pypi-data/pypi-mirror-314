from ..commands.alembic import build_alembic
from ..config import OARepoConfig
from .base import command_sequence, nrp_command


@nrp_command.command(name="alembic")
@command_sequence()
def alembic_command(*, config: OARepoConfig, **kwargs):
    """Builds the repository"""
    return (build_alembic,)
