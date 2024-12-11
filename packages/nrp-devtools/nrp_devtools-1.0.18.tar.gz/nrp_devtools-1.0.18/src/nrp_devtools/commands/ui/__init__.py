import json

from ...config import OARepoConfig
from ..check import check_failed
from .assets import collect_assets, install_npm_packages
from .build import build_production_ui
from .less import register_less_components


def check_ui(config: OARepoConfig, will_fix=False, **kwargs):
    # check that there is a manifest.json there
    manifest = config.invenio_instance_path / "static" / "dist" / "manifest.json"
    if not manifest.exists():
        check_failed(
            f"manifest.json file is missing.",
            will_fix=will_fix,
        )

    try:
        json_data = json.loads(manifest.read_text())
        if json_data.get("status") != "done":
            check_failed(
                f"manifest.json file is not ready. "
                f"Either a build is in progress or it failed.",
                will_fix=will_fix,
            )
    except:  # noqa
        check_failed(
            f"manifest.json file is not valid json file.",
            will_fix=will_fix,
        )


def fix_ui(config: OARepoConfig, **kwargs):
    collect_assets(config)
    install_npm_packages(config)
    build_production_ui(config)


__all__ = [
    "register_less_components",
    "build_production_ui",
    "collect_assets",
    "install_npm_packages",
]
