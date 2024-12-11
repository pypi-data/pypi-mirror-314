import json
from pathlib import Path

import click

from ..commands.ui.create import (
    create_model_ui,
    create_page_ui,
    register_model_ui,
    register_page_ui,
)
from ..commands.utils import capitalize_name, make_step
from ..config import OARepoConfig
from ..config.ui_config import UIConfig
from .base import command_sequence, nrp_command


@nrp_command.group(name="ui")
def ui_group():
    """
    UI management commands.
    """


"""
nrp ui pages create <ui-name> <ui-endpoint>
```

The `ui-endpoint` is the endpoint of the root for pages, for example
`/docs` or `/search`. The `ui-name` is the name of the collection of pages,
such as `docs` or `search`.

If `ui-endpoint` is not specified, it will be the same as
`ui-name` with '/' prepended.
"""


@ui_group.group(name="pages")
def pages_group():
    """
    UI pages management commands.
    """


@pages_group.command(
    name="create",
    help="""Create a new UI pages collection. 
    The ui-name is the name of the collection of pages, such as docs or search,
    ui-endpoint is the url path of the pages' root, for example /docs or /search. 
    If not specified, it will be the same as ui-name with '/' prepended.
    """,
)
@click.argument("ui-name")
@click.argument(
    "ui-endpoint",
    required=False,
)
@command_sequence(save=True)
def create_pages(config: OARepoConfig, ui_name, ui_endpoint, **kwargs):
    """
    Create a new UI pages collection.
    """
    ui_name = ui_name.replace("-", "_")
    ui_endpoint = ui_endpoint or ("/" + ui_name.replace("_", "-"))
    if not ui_endpoint.startswith("/"):
        ui_endpoint = "/" + ui_endpoint

    if config.get_ui(ui_name, default=None):
        click.secho(f"UI {ui_name} already exists", fg="red", err=True)
        return

    def set_ui_configuration(config: OARepoConfig, *args, **kwargs):
        config.add_ui(UIConfig(name=ui_name, endpoint=ui_endpoint))

    return (
        set_ui_configuration,
        make_step(create_page_ui, ui_name=ui_name),
        make_step(register_page_ui, ui_name=ui_name),
    )


@ui_group.group(name="model")
def model_group():
    """
    UI model management commands
    """


@model_group.command(
    name="create",
    help="""Create a new UI for metadata model. 
    The model-name is the name of the model, such as documents or records,
    ui-name is the name of the ui (default is the same as model-name).
    ui-endpoint, if not passed, is taken from the model's resource-config, 
    field base-html-url.
    """,
)
@click.argument("model-name")
@click.argument("ui-name", required=False)
@click.argument(
    "ui-endpoint",
    required=False,
)
@command_sequence(save=True)
def create_model(config: OARepoConfig, model_name, ui_name, ui_endpoint, **kwargs):
    """
    Create a new UI model.
    """
    if not ui_name:
        ui_name = model_name

    ui_name = ui_name.replace("-", "_")

    if config.get_ui(ui_name, default=None):
        click.secho(f"UI {ui_name} already exists", fg="red", err=True)
        return

    def set_ui_configuration(config: OARepoConfig, *args, **kwargs):
        nonlocal ui_endpoint

        model = config.get_model(model_name)

        model_data = json.loads(
            (
                config.repository_dir / model.model_package / "models" / "records.json"
            ).read_text()
        )
        api_service = model_data["model"]["service-config"]["service-id"]
        ui_serializer_class = model_data["model"]["json-serializer"]["class"]
        if not ui_endpoint:
            ui_endpoint = model_data["model"]["resource-config"]["base-html-url"]

        config.add_ui(
            UIConfig(
                name=ui_name,
                endpoint=ui_endpoint,
                model=model_name,
                api_service=api_service,
                ui_serializer_class=ui_serializer_class,
            )
        )

    return (
        set_ui_configuration,
        make_step(create_model_ui, ui_name=ui_name),
        make_step(register_model_ui, ui_name=ui_name),
    )


@ui_group.group(name="components")
def components_group(*args, **kwargs):
    pass


@components_group.command(
    name="create",
    help="""Create a new less component.  
The component-type is the type of the component, such as element, view, module, or collection.
The component-name is the name of the component, such as navbar or footer.
    """,
)
@click.argument("component-type")
@click.argument("component-name")
@click.option(
    "--jinjax/--no-jinjax", default=True, help="Generate jinjax template as well"
)
@command_sequence()
def create_less_component(
    config: OARepoConfig, component_type, component_name, jinjax, **kwargs
):
    ui_name = "components"
    # if the config.ui_dir/ui_name does not exist, run cookiecutter to create it
    ui_dir = config.ui_dir / ui_name

    def create_less_component(*args, **kwargs):
        # files and directories
        less_dir = ui_dir / "semantic-ui" / "less"
        definitions_dir = less_dir / ui_name / "definitions"
        default_theme_dir = less_dir / ui_name / "default"
        registration_less_file = less_dir / ui_name / "custom-components.less"

        component_type_plural = component_type + "s"

        component_file = (
            definitions_dir / component_type_plural / f"{component_name}.less"
        )
        component_variables_file = (
            default_theme_dir / component_type_plural / f"{component_name}.variables"
        )
        component_overrides_file = (
            default_theme_dir / component_type_plural / f"{component_name}.overrides"
        )

        # create variable and override files
        component_variables_file.parent.mkdir(parents=True, exist_ok=True)
        if not component_variables_file.exists():
            component_variables_file.write_text(
                f"""
/* https://github.com/Semantic-Org/example-github/blob/master/semantic/src/themes/default/globals/site.variables */
/* @{component_name}Background: @inputBackground; */
            """
            )
        click.secho(
            f"Place variables that parametrize the component inside {component_variables_file}",
            fg="green",
        )

        component_overrides_file.parent.mkdir(parents=True, exist_ok=True)
        if not component_overrides_file.exists():
            component_overrides_file.touch()

        # create the component
        less_data = (
            Path(__file__).parent.parent / "templates" / "component.less"
        ).read_text()
        less_data = less_data.replace("{{component_type}}", component_type)
        less_data = less_data.replace("{{component_name}}", component_name)

        component_file.parent.mkdir(parents=True, exist_ok=True)
        if not component_file.exists():
            component_file.write_text(less_data)
        click.secho(f"Put the default css to {component_file}", fg="green")

        # add the component to the registration file
        registration_less_data = registration_less_file.read_text()
        registration_less_data += f'\n& {{\n @import "@less/{ui_name}/definitions/{component_type_plural}/{component_name}"; \n}}'
        registration_less_file.write_text(registration_less_data)

    def create_jinjax_component(*args, **kwargs):
        if not jinjax:
            return
        component_name_capitalized = capitalize_name(component_name)
        jinjax_component_file = (
            ui_dir / "templates" / ui_name / f"{component_name_capitalized}.jinja"
        )

        jinjax_component_file.parent.mkdir(parents=True, exist_ok=True)
        if not jinjax_component_file.exists():
            jinjax_component_file.write_text(
                f"""{{# def #}}
    <div class="ui {component_name}">
      Overwrite this file with your own jinja template.
    </div>
            """
            )
        click.secho(
            f"Place the HTML code of the component to {jinjax_component_file} "
            f"and reference it from elsewhere as <components.{component_name_capitalized} /> or <{component_name_capitalized} />. "
            f"Do not forget to put css classes 'ui {component_name}' to the root element of the template.",
            fg="green",
        )

    return (
        create_less_component,
        create_jinjax_component,
    )
