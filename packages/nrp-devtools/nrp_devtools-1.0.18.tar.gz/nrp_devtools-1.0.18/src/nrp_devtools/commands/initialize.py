from pathlib import Path

from nrp_devtools.commands.utils import run_cookiecutter
from nrp_devtools.config import OARepoConfig
from nrp_devtools.x509 import generate_selfsigned_cert


def initialize_repository(config: OARepoConfig):
    run_cookiecutter(
        config.repository_dir.parent,
        template=Path(__file__).parent.parent / "templates" / "repository",
        extra_context={
            "repository_name": config.repository_dir.name,
            "shared_package": config.repository.shared_package,
            "repository_package": config.repository.repository_package,
            "repository_human_name": config.repository.repository_human_name,
            "ui_package": config.repository.ui_package,
            "model_package": config.repository.model_package,
            "oarepo_version": config.repository.oarepo_version,
        },
    )

    # generate the certificate
    cert, key = generate_selfsigned_cert("localhost", ["127.0.0.1"])
    (config.repository_dir / "docker" / "development.crt").write_bytes(cert)
    (config.repository_dir / "docker" / "development.key").write_bytes(key)

    # link the variables
    (config.repository_dir / "docker" / ".env").symlink_to(
        config.repository_dir / "variables"
    )

    # mark the nrp command executable
    (config.repository_dir / "nrp").chmod(0o755)

    # set up the i18n
    config.i18n.babel_source_paths = [
        config.repository.shared_package,
        config.repository.ui_package,
    ]
    config.i18n.i18next_source_paths = [config.repository.ui_package]
