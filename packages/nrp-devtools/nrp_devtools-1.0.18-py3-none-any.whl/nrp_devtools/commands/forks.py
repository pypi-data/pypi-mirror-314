import json

from nrp_devtools.commands.utils import call_pip
from nrp_devtools.config import OARepoConfig


def apply_forks(config: OARepoConfig, resolver):
    packages_and_versions = json.loads(
        call_pip(
            config.venv_dir,
            "list",
            "--format",
            "json",
            no_environment=True,
            raise_exception=True,
            grab_stdout=True,
            no_input=True,
        )
    )
    packages_and_versions = {
        package["name"]: package for package in packages_and_versions
    }

    urls_to_install = []

    for fork_package, fork_repository in config.forks.items():
        if fork_package not in packages_and_versions:
            raise ValueError(
                f"Package {fork_package} not found in the installed packages."
            )
        expected_version = packages_and_versions[fork_package]["version"]
        if "#" in fork_repository:
            fork_repository, egginfo = fork_repository.split("#")
            egginfo = f"#{egginfo}"
        else:
            egginfo = ""
        fork_pip_url = (
            f"{fork_repository}/archive/oarepo-{expected_version}.tar.gz{egginfo}"
        )
        urls_to_install.append(fork_pip_url)

    if urls_to_install:
        resolver.install_packages(config, *urls_to_install)
