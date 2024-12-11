from nrp_devtools.commands.utils import run_cmdline
from nrp_devtools.config import OARepoConfig


def build_production_ui(config: OARepoConfig):
    run_cmdline(
        config.invenio_command,
        "webpack",
        "build",
        "--production",
        environ={"INVENIO_INSTANCE_PATH": str(config.invenio_instance_path)},
    )

    # do not allow Clean plugin to remove files
    webpack_config = (
        config.invenio_instance_path / "assets" / "build" / "webpack.config.js"
    ).read_text()
    webpack_config = webpack_config.replace("dry: false", "dry: true")
    (
        config.invenio_instance_path / "assets" / "build" / "webpack.config.js"
    ).write_text(webpack_config)
