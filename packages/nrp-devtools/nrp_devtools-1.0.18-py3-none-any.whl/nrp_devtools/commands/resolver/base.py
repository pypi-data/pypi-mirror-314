import os
import re
import shutil
import sys

import click
import requirements
import tomli
import tomli_w

from nrp_devtools.commands.check import check_failed
from nrp_devtools.commands.forks import apply_forks
from nrp_devtools.config import OARepoConfig
from nrp_devtools.commands.utils import install_python_modules, run_cmdline, call_pip
from requirements.parser import Requirement


class PythonResolver:

    def __init__(self, config):
        self.config = config

    def clean_previous_installation(self, **kwargs):
        self.destroy_venv()

    def create_empty_venv(self):
        self.destroy_venv()
        install_python_modules(
            self.config,
            self.config.venv_dir,
            "setuptools",
            "pip",
            "wheel",
        )

    def destroy_venv(self):
        if self.config.venv_dir.exists():
            shutil.rmtree(self.config.venv_dir)

    def build_requirements(self, **kwargs):
        self.destroy_venv()
        self.create_empty_venv()
        temporary_project_dir = ".nrp/oarepo-pdm"
        self.create_oarepo_project_dir(temporary_project_dir)
        self.lock_python_repository(temporary_project_dir)
        oarepo_requirements = self.export_requirements(temporary_project_dir)

        self.lock_python_repository()
        all_requirements = self.export_requirements()

        oarepo_requirements = list(requirements.parse(oarepo_requirements))
        all_requirements = list(requirements.parse(all_requirements))

        # get the current version of oarepo
        oarepo_requirement = [x for x in oarepo_requirements if x.name == "oarepo"][0]

        # uv does not keep the extras in the generated requirements.txt, so adding these here for oarepo
        original_oarepo_dependency, _ = self.get_original_oarepo_dependency()
        if '[' in original_oarepo_dependency:
            oarepo_requirement.extras = original_oarepo_dependency.split("[")[1].split("]")[0].split(',')

        oarepo_requirement = Requirement(
            re.split('[><=]', original_oarepo_dependency)[0] +
            "==" + oarepo_requirement.line.split("==")[1]
        )

        # now make the difference of those two (we do not want to have oarepo dependencies in the result)
        # as oarepo will be installed to virtualenv separately (to handle system packages)
        oarepo_requirements_names = {x.name for x in oarepo_requirements}
        non_oarepo_requirements = [
            x for x in all_requirements if x.name not in oarepo_requirements_names
        ]

        # remove local packages
        non_oarepo_requirements = [
            x for x in non_oarepo_requirements if "file://" not in x.line
        ]

        # and generate final requirements
        resolved_requirements = "\n".join(
            [oarepo_requirement.line, *[x.line for x in non_oarepo_requirements]]
        )
        (self.config.repository_dir / "requirements.txt").write_text(resolved_requirements)

    def lock_python_repository(self, subdir=None):
        raise NotImplementedError()

    def install_project_packages(self):
        raise NotImplementedError()

    def check_invenio_callable(self, will_fix=False, **kwargs):
        try:
            run_cmdline(
                self.config.venv_dir / "bin" / "invenio",
                "oarepo",
                "version",
                raise_exception=True,
                grab_stdout=True,
            )
        except:
            check_failed(
                f"Virtualenv directory {self.config.venv_dir} does not contain a callable invenio installation",
                will_fix=will_fix,
            )

    def install_python_repository(self, **kwargs):
        self.install_project_packages()

        # apply forks
        apply_forks(self.config, self)


    def create_oarepo_project_dir(self, output_directory: str):
        oarepo_dependency, original_pdm_file = self.get_original_oarepo_dependency()

        original_pdm_file["project"]["dependencies"] = [oarepo_dependency]

        output_path = self.config.repository_dir / output_directory
        output_path.mkdir(parents=True, exist_ok=True)

        (output_path / "pyproject.toml").write_text(tomli_w.dumps(original_pdm_file))

    def get_original_oarepo_dependency(self):
        original_pyproject_file = tomli.loads(
            (self.config.repository_dir / "pyproject.toml").read_text()
        )
        dependencies = original_pyproject_file["project"]["dependencies"]
        oarepo_dependency = [
            x
            for x in dependencies
            if re.match(
                r"^\s*oarepo\s*(\[[^\]]+\])?\s*[><=]+.*", x
            )  # take only oarepo package, discard others
        ][0]
        return oarepo_dependency, original_pyproject_file

    def remove_virtualenv_from_env(self):
        current_env = dict(os.environ)
        virtual_env_dir = current_env.pop("VIRTUAL_ENV", None)
        if not virtual_env_dir:
            return current_env
        current_env.pop("PYTHONHOME", None)
        current_env.pop("PYTHON", None)
        path = current_env.pop("PATH", None)
        split_path = path.split(os.pathsep)
        split_path = [x for x in split_path if not x.startswith(virtual_env_dir)]
        current_env["PATH"] = os.pathsep.join(split_path)
        return current_env

    def export_requirements(self, subdir=None):
        raise NotImplementedError()

    def install_packages(self, config, *packages):
        call_pip(
            config.venv_dir,
            "install",
            "-U",
            "--no-input",
            "--force",
            "--no-deps",
            "--pre",
            *packages,
            no_environment=True,
            raise_exception=True,
            no_input=True,
        )


    def install_local_packages(self, local_packages=None):
        if not local_packages:
            return
        for lp in local_packages:
            run_cmdline(
                self.config.venv_dir / "bin" / "pip",
                "install",
                "--config-settings",
                "editable_mode=compat",
                "-e",
                lp,
                cwd=self.config.repository_dir,
            )

    def check_virtualenv(self, will_fix=False, **kwargs):
        if not self.config.venv_dir.exists():
            click.secho(
                f"Virtualenv directory {self.config.venv_dir} does not exist", fg="red", err=True
            )
            sys.exit(1)

        try:
            run_cmdline(
                self.config.venv_dir / "bin" / "python",
                "--version",
                raise_exception=True,
            )
        except:  # noqa
            check_failed(
                f"Virtualenv directory {self.config.venv_dir} does not contain a python installation",
                will_fix=will_fix,
            )

        try:
            run_cmdline(
                self.config.venv_dir / "bin" / "pip",
                "list",
                raise_exception=True,
                grab_stdout=True,
            )
        except:  # noqa
            check_failed(
                f"Virtualenv directory {self.config.venv_dir} does not contain a pip installation",
                will_fix=will_fix,
            )

    def fix_virtualenv(self, **kwargs):
        self.destroy_venv()
        self.create_empty_venv()

    def check_requirements(self, will_fix=False, **kwargs):
        reqs_file = self.config.repository_dir / "requirements.txt"
        if not reqs_file.exists():
            check_failed(f"Requirements file {reqs_file} does not exist", False)

        # if any pyproject.toml is newer than requirements.txt, we need to rebuild
        pyproject = self.config.repository_dir / "pyproject.toml"

        if pyproject.exists() and pyproject.stat().st_mtime > reqs_file.stat().st_mtime:
            check_failed(
                f"Requirements file {reqs_file} is out of date, {pyproject} has been modified",
                will_fix=will_fix,
            )
