from ..commands.resolver import get_resolver
from ..config import OARepoConfig
from .base import command_sequence, nrp_command
from .build import build_command_internal
from ..pypi_proxy.proxy import start_pypi_proxy




@nrp_command.command(name="upgrade")
@command_sequence()
def upgrade_command(*, config: OARepoConfig, **kwargs):
    """Upgrades the repository.

    Resolves the newest applicable packages, downloads them and rebuilds the repository.
    """
    start_pypi_proxy(config.pypi_proxy_target)
    return (lambda config: get_resolver(config).build_requirements(),) + build_command_internal(config=config)




