import shutil

from .base import PythonResolver
from nrp_devtools.commands.utils import install_python_modules, run_cmdline
from nrp_devtools.config import OARepoConfig


class PDMResolver(PythonResolver):
    def create_empty_venv(self):
        super().create_empty_venv()
        install_python_modules(self.config, self.config.pdm_dir, "pdm")

    def destroy_venv(self):
        super().destroy_venv()
        if self.config.pdm_dir.exists():
            shutil.rmtree(self.config.pdm_dir)

    def lock_python_repository(self, subdir=None):
        self.write_pdm_python()
        self.run_pdm("lock", subdir=subdir)

    def export_requirements(self, subdir=None):
        return self.run_pdm(
            "export",
            "-f",
            "requirements",
            "--without-hashes",
            grab_stdout=True,
            subdir=subdir,
        )

    def install_project_packages(self):
        self.run_pip("install", "--pre", "-r", "requirements.txt")
        self.run_pip("install", "--no-deps", "-e", ".")

    def run_pip(self, *args, subdir=None, **kwargs):

        cwd = self.config.repository_dir
        if subdir:
            cwd = cwd / subdir

        environ = {
            **self.remove_virtualenv_from_env(),
        }

        venv_path = self.config.venv_dir
        assert venv_path.exists()

        environ["VIRTUAL_ENV"] = str(venv_path)

        return run_cmdline(
            str(venv_path / "bin" / "pip"),
            *args,
            cwd=cwd,
            environ=environ,
            no_environment=True,
            raise_exception=True,
            **kwargs,
        )



    def run_pdm(self, *args, subdir=None, **kwargs):
        self.write_pdm_python()

        cwd = self.config.repository_dir
        if subdir:
            cwd = cwd / subdir

        if (cwd / "__pypackages__").exists():
            shutil.rmtree(cwd / "__pypackages__")

        environ = {
            "PDM_IGNORE_ACTIVE_VENV": "1",
            "PDM_IGNORE_SAVED_PYTHON": "1",
            **self.remove_virtualenv_from_env(),
        }
        venv_path = self.config.venv_dir
        if venv_path.exists():
            environ.pop("PDM_IGNORE_ACTIVE_VENV", None)
            environ["VIRTUAL_ENV"] = str(venv_path)
            print(f"Using venv for pdm: {environ['VIRTUAL_ENV']}")

        return run_cmdline(
            self.config.pdm_dir / "bin" / "pdm",
            *args,
            cwd=cwd,
            environ=environ,
            no_environment=True,
            raise_exception=True,
            **kwargs,
        )

    def write_pdm_python(self):
        pdm_python_file = self.config.repository_dir / ".pdm-python"
        if pdm_python_file.exists():
            previous_content = pdm_python_file.read_text().strip()
        else:
            previous_content = None
        new_content = str(self.config.venv_dir / "bin" / "python")
        if new_content != previous_content:
            pdm_python_file.write_text(new_content)
