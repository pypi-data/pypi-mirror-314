from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    ".",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "{{cookiecutter.name}}_search": "./js/{{cookiecutter.name}}/search/index.js",
                "{{cookiecutter.name}}_deposit_form": "./js/{{cookiecutter.name}}/forms/index.js",
            },
            dependencies={},
            devDependencies={},
            aliases={},
        )
    },
)
