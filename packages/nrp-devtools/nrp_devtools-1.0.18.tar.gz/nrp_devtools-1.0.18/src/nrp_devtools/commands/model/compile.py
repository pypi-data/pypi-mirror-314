import configparser
import json
import shutil
import venv
from pathlib import Path

import click
import yaml

from nrp_devtools.commands.pyproject import PyProject
from nrp_devtools.commands.utils import run_cmdline
from nrp_devtools.config import OARepoConfig
from nrp_devtools.config.model_config import ModelConfig


def model_compiler_venv_dir(config: OARepoConfig, model):
    venv_dir = (
        config.repository_dir / ".nrp" / f"oarepo-model-builder-{model.model_name}"
    )
    return venv_dir.resolve()


def install_model_compiler(config: OARepoConfig, *, model: ModelConfig):
    venv_dir = model_compiler_venv_dir(config, model)
    print("model builder venv dir", venv_dir)
    click.secho(f"Installing model compiler to {venv_dir}", fg="yellow")

    if venv_dir.exists():
        shutil.rmtree(venv_dir)

    venv_args = [str(venv_dir)]
    venv.main(venv_args)

    run_cmdline(
        venv_dir / "bin" / "pip",
        "install",
        "-U",
        "setuptools",
        "pip",
        "wheel",
    )

    run_cmdline(
        venv_dir / "bin" / "pip",
        "install",
        f"oarepo-model-builder",
    )

    with open(config.models_dir / model.model_config_file) as f:
        model_data = yaml.safe_load(f)

    # install plugins from model.yaml
    _install_plugins_from_model(model_data, venv_dir)

    # install plugins from included files
    uses = model_data.get("use") or []
    if not isinstance(uses, list):
        uses = [uses]

    for use in uses:
        if not use.startswith("."):
            # can not currently find plugins in uses
            # that are registered as entrypoints
            continue
        with open(config.models_dir / use) as f:
            used_data = yaml.safe_load(f)
            _install_plugins_from_model(used_data, venv_dir)

    click.secho(f"Model compiler installed to {venv_dir}", fg="green")


def _install_plugins_from_model(model_data, venv_dir):
    plugins = model_data.get("plugins", {}).get("packages", [])
    for package in plugins:
        run_cmdline(
            venv_dir / "bin" / "pip",
            "install",
            package,
        )


def compile_model_to_tempdir(config: OARepoConfig, *, model: ModelConfig, tempdir):
    click.secho(f"Compiling model {model.model_name} to {tempdir}", fg="yellow")
    venv_dir = model_compiler_venv_dir(config, model)
    run_cmdline(
        venv_dir / "bin" / "oarepo-compile-model",
        "-vvv",
        str(config.models_dir / model.model_config_file),
        "--output-directory",
        str(tempdir),
    )
    click.secho(
        f"Model {model.model_name} successfully compiled to {tempdir}", fg="green"
    )


def copy_compiled_model(config: OARepoConfig, *, model: ModelConfig, tempdir):
    click.secho(
        f"Copying compiled model {model.model_name} from {tempdir} to {model.model_package}",
        fg="yellow",
    )
    alembic_path = Path(_get_alembic_path(tempdir, model.model_package)).resolve()

    remove_all_files_in_directory(
        config.repository_dir / model.model_package, except_of=alembic_path
    )

    copy_all_files_but_keep_existing(
        Path(tempdir) / model.model_package, config.repository_dir / model.model_package
    )

    click.secho(
        f"Compiled model {model.model_name} successfully copied to {model.model_package}",
        fg="green",
    )


def _get_alembic_path(rootdir, package_name):
    model_file = Path(rootdir) / package_name / "models" / "records.json"

    with open(model_file) as f:
        model_data = json.load(f)

    return model_data["model"]["record-metadata"]["alembic"].replace(".", "/")


def remove_all_files_in_directory(directory: Path, except_of=None):
    if not directory.exists():
        return True

    remove_this_directory = True
    for path in directory.iterdir():
        if path.resolve() == except_of:
            remove_this_directory = False
            continue
        if path.is_file():
            path.unlink()
        else:
            remove_this_directory = (
                remove_all_files_in_directory(path) and remove_this_directory
            )
    if remove_this_directory:
        directory.rmdir()
    return remove_this_directory


def copy_all_files_but_keep_existing(src: Path, dst: Path):
    def non_overwriting_copy(src, dst, *, follow_symlinks=True):
        if Path(dst).exists():
            return
        shutil.copy2(src, dst, follow_symlinks=follow_symlinks)

    return shutil.copytree(
        src, dst, copy_function=non_overwriting_copy, dirs_exist_ok=True
    )


def add_requirements_and_entrypoints(
    config: OARepoConfig, *, model: ModelConfig, tempdir
):
    click.secho(
        f"Adding requirements and entrypoints from {model.model_name}", fg="yellow"
    )

    setup_cfg = Path(tempdir) / "setup.cfg"
    # load setup.cfg via configparser
    config_parser = configparser.ConfigParser()
    config_parser.read(setup_cfg)
    dependencies = config_parser["options"].get("install_requires", "").split("\n")
    test_depedencies = (
        config_parser["options.extras_require"].get("tests", "").split("\n")
    )
    entrypoints = {}
    for ep_name, ep_values in config_parser["options.entry_points"].items():
        entrypoints[ep_name] = ep_values.split("\n")

    pyproject = PyProject(config.repository_dir / "pyproject.toml")

    pyproject.add_dependencies(*dependencies)
    pyproject.add_optional_dependencies("tests", *test_depedencies)

    for ep_name, ep_values in entrypoints.items():
        for val in ep_values:
            if not val:
                continue
            val = [x.strip() for x in val.split("=")]
            pyproject.add_entry_point(ep_name, val[0], val[1])

    pyproject.save()

    click.secho(
        f"Requirements and entrypoint successfully copied from {model.model_name}",
        fg="green",
    )


def add_model_to_i18n(config: OARepoConfig, *, model, **kwargs):
    i18n_config = config.i18n
    i18n_config.babel_source_paths.append(model.model_package)
