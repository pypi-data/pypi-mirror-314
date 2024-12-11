import click

from ..config import OARepoConfig
from .base import command_sequence, nrp_command
from .build import build_command_internal
from time import sleep
from ..pypi_proxy.proxy import start_pypi_proxy

@nrp_command.command(name="proxy")
@click.argument("time")
@command_sequence()
def start_proxy(*, config: OARepoConfig, time, **kwargs):
    start_pypi_proxy(config.pypi_proxy_target)
    sleep(int(time))