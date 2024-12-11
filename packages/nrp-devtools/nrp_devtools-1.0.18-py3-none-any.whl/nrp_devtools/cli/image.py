import click

from ..commands.utils import make_step, run_cmdline
from ..config import OARepoConfig
from .base import command_sequence, nrp_command


@nrp_command.command(name="image")
@command_sequence()
def image_command(*, config: OARepoConfig, local_packages=None, checks=True, **kwargs):
    """Starts the repository. Make sure to run `nrp check` first."""

    def build_image(*args, **kwargs):
        info_string = run_cmdline("docker", "info", grab_stdout=True)
        architecture_line = [
            x for x in info_string.split("\n") if "Architecture:" in x
        ][0]
        architecture = architecture_line.split(":")[1].strip()
        if architecture == "aarch64":
            build_platform = "linux/arm64/v8"
        else:
            build_platform = "linux/amd64"
        click.secho(f"Building image for {build_platform}")

        run_cmdline(
            "docker",
            "build",
            ".",
            "--target",
            "production",
            "-f",
            "docker/Dockerfile.production",
            "--build-arg",
            f"BUILDPLATFORM={build_platform}",
            environ={
                "BUILDKIT_PROGRESS": "plain",
                "BUILDPLATFORM": build_platform,
                "DOCKER_BUILDKIT": "1",
                **config.global_environment()
            },
        )

    return (make_step(build_image),)
