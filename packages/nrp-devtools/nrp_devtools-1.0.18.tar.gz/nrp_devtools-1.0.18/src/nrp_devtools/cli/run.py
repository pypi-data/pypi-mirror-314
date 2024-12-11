from ..commands.develop import Runner
from ..commands.develop.controller import run_develop_controller
from ..commands.utils import make_step
from ..config import OARepoConfig
from .base import command_sequence, nrp_command


@nrp_command.command(name="run")
@command_sequence()
def run_command(*, config: OARepoConfig, local_packages=None, checks=True, **kwargs):
    """Starts the repository. Make sure to run `nrp check` first."""
    runner = Runner(config)
    return (
        make_step(
            lambda config=None, runner=None: runner.start_python_server(), runner=runner
        ),
        make_step(run_develop_controller, runner=runner, development_mode=False),
    )
