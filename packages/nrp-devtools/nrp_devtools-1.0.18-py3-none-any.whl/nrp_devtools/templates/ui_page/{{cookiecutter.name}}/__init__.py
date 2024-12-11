from oarepo_ui.resources.config import TemplatePageUIResourceConfig
from oarepo_ui.resources.resource import TemplatePageUIResource


class {{cookiecutter.capitalized_name}}PageResourceConfig(TemplatePageUIResourceConfig):
    url_prefix = "/"
    blueprint_name = "{{cookiecutter.name}}"
    template_folder = "templates"
    pages = {
        "": "{{cookiecutter.template_name}}",
        # add a new page here. The key is the URL path, the value is the name of the template
        # then put <name>.jinja into the templates folder
    }


def create_blueprint(app):
    """Register blueprint for this resource."""
    return TemplatePageUIResource({{cookiecutter.capitalized_name}}PageResourceConfig()).as_blueprint()
