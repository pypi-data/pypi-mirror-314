import tempfile
from pathlib import Path

import click
import shutil

from ..commands.model.compile import (
    add_model_to_i18n,
    add_requirements_and_entrypoints,
    compile_model_to_tempdir,
    copy_compiled_model,
    install_model_compiler,
)
from ..commands.model.create import create_model
from ..commands.resolver import get_resolver
from ..commands.utils import make_step
from ..config import OARepoConfig, ask_for_configuration
from ..config.model_config import ModelConfig, ModelFeature, BaseModel
from .base import command_sequence, nrp_command
from ..pypi_proxy.proxy import start_pypi_proxy


@nrp_command.group(name="model")
def model_group():
    """
    Model management commands
    """


@model_group.command(name="create", help="Create a new model")
@click.argument("model_name")
@click.option("--copy-model-config", help="Use a configuration file", type=click.Path())
@command_sequence(save=True)
def create_model_command(*, config: OARepoConfig, model_name, copy_model_config=None, **kwargs):
    for model in config.models:
        if model.model_name == model_name:
            click.secho(f"Model {model_name} already exists", fg="red", err=True)
            return

    if copy_model_config:
        # if the config file is ready, just copy and add note to oarepo.yaml
        # TODO: if possible, parse the values below from the copied config file
        values = {
            "base_model": BaseModel.empty,
            "model_name": model_name,
            "model_description": "",
            "features": [
                ModelFeature.tests,
                ModelFeature.custom_fields,
                ModelFeature.requests,
                ModelFeature.files,
                ModelFeature.drafts,
                ModelFeature.relations
            ]
        }
        values["model_package"] = ModelConfig.default_model_package(config, values)
        values["api_prefix"] = ModelConfig.default_api_prefix(config, values)
        values["pid_type"] = ModelConfig.default_pid_type(config, values)
        config.models.append(ModelConfig(**values))
        shutil.copy(copy_model_config, config.models_dir / f"{model_name}.yaml")
        return ()

    def set_model_configuration(config: OARepoConfig, *args, **kwargs):
        config.add_model(
            ask_for_configuration(
                config, ModelConfig, initial_values={"model_name": model_name}
            )
        )

    return (
        set_model_configuration,
        make_step(create_model, model_name=model_name),
    )


@model_group.command(name="compile", help="Compile a model")
@click.argument("model_name")
@click.option("--reinstall-builder/--keep-builder",
              is_flag=True, help="Reinstall the model builder", default=True)
@command_sequence()
def compile_model_command(*, config: OARepoConfig, model_name, reinstall_builder, **kwargs):
    start_pypi_proxy(config.pypi_proxy_target)
    model = config.get_model(model_name)
    # create a temporary directory using tempfile
    tempdir = str(Path(tempfile.mkdtemp()).resolve())

    if reinstall_builder:
        steps = [
            make_step(install_model_compiler, model=model)
        ]
    else:
        steps = []

    return (
        *steps,
        make_step(compile_model_to_tempdir, model=model, tempdir=tempdir),
        make_step(copy_compiled_model, model=model, tempdir=tempdir),
        make_step(add_requirements_and_entrypoints, model=model, tempdir=tempdir),
        make_step(lambda config: get_resolver(config).install_python_repository()),
        make_step(add_model_to_i18n, model=model),
    )
