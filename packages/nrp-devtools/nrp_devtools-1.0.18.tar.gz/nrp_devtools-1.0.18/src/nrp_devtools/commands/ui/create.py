from pathlib import Path

import caseconverter

from nrp_devtools.commands.pyproject import PyProject
from nrp_devtools.commands.utils import capitalize_name, run_cookiecutter
from nrp_devtools.config import OARepoConfig
from nrp_devtools.config.model_config import ModelConfig

from .create_detail import create_detail_page


def create_page_ui(config: OARepoConfig, *, ui_name: str):
    ui_config = config.get_ui(ui_name)

    if (config.ui_dir / ui_config.name).exists():
        return

    capitalized_name = capitalize_name(ui_config.name)

    run_cookiecutter(
        config.ui_dir,
        template=Path(__file__).parent.parent.parent / "templates" / "ui_page",
        extra_context={
            "name": ui_config.name,
            "endpoint": ui_config.endpoint,
            "capitalized_name": capitalized_name,
            "template_name": capitalized_name + "Page",
        },
    )


def register_page_ui(config: OARepoConfig, *, ui_name: str):
    ui_config = config.get_ui(ui_name)

    pyproject = PyProject(config.repository_dir / "pyproject.toml")

    pyproject.add_entry_point(
        "invenio_base.blueprints",
        f"ui_{ui_config.name}",
        f"{config.repository.ui_package}.{ui_config.name}:create_blueprint",
    )

    pyproject.save()


def create_model_ui(config: OARepoConfig, *, ui_name: str):
    ui_config = config.get_ui(ui_name)

    if (config.ui_dir / ui_config.name).exists():
        return

    capitalized_name = caseconverter.camelcase(ui_config.name)
    capitalized_name = capitalized_name[0].upper() + capitalized_name[1:]

    model_name = ui_config.model
    prefix = model_name.capitalize()

    run_cookiecutter(
        config.ui_dir,
        template=Path(__file__).parent.parent.parent / "templates" / "ui_model",
        extra_context={
            "name": ui_config.name,
            "endpoint": ui_config.endpoint,
            "capitalized_name": capitalized_name,
            "resource": capitalized_name + "Resource",
            "resource_config": capitalized_name + "ResourceConfig",
            "ui_serializer_class": ui_config.ui_serializer_class,
            "api_service": ui_config.api_service,
            "root_component": prefix + "DetailRoot",
        },
    )

    model_config: ModelConfig = config.get_model(model_name)

    ui_file = config.repository_dir / model_config.model_package / "models" / "ui.json"
    ui_components_dir = (
        config.ui_dir / ui_config.name / "templates" / "semantic-ui" / "components"
    )
    ui_components_dir.mkdir(parents=True, exist_ok=True)
    create_detail_page(ui_file, ui_components_dir, prefix)


def register_model_ui(config: OARepoConfig, *, ui_name: str):
    ui_config = config.get_ui(ui_name)

    pyproject = PyProject(config.repository_dir / "pyproject.toml")

    pyproject.add_entry_point(
        "invenio_base.blueprints",
        f"ui_{ui_config.name}",
        f"{config.repository.ui_package}.{ui_config.name}:create_blueprint",
    )

    pyproject.add_entry_point(
        "invenio_assets.webpack",
        f"ui_{ui_config.name}",
        f"{config.repository.ui_package}.{ui_config.name}.webpack:theme",
    )

    pyproject.save()
