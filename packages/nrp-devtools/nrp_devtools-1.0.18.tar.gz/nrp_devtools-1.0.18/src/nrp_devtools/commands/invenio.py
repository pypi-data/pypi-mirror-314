import json
import tempfile

from nrp_devtools.commands.utils import run_cmdline
from nrp_devtools.config import OARepoConfig

from .check import check_failed


def get_repository_info(config, context=None):
    if context is not None and "repository_info" in context:
        return context["repository_info"]

    with tempfile.NamedTemporaryFile(suffix=".json") as f:
        run_cmdline(
            config.invenio_command,
            "oarepo",
            "check",
            f.name,
            raise_exception=True,
            grab_stdout=True,
        )
        f.seek(0)
        repository_info = json.load(f)
    if context is not None:
        context["repository_info"] = repository_info
    return repository_info


def get_invenio_configuration(config, context, *args):
    def _get_config(config, context):
        if context is not None and "repository_configuration" in context:
            return context["repository_configuration"]

        with tempfile.NamedTemporaryFile(suffix=".json") as f:
            run_cmdline(
                config.invenio_command,
                "oarepo",
                "configuration",
                f.name,
                raise_exception=True,
                grab_stdout=True,
            )
            f.seek(0)
            configuration = json.load(f)
        if context is not None:
            context["repository_configuration"] = configuration
        return configuration

    configuration = _get_config(config, context)
    return [configuration[x] for x in args]


def check_invenio_cfg(config: OARepoConfig, will_fix=False, **kwargs):
    instance_dir = config.invenio_instance_path
    target_invenio_cfg = instance_dir / "invenio.cfg"
    target_variables = instance_dir / "variables"
    if not target_invenio_cfg.exists():
        check_failed(
            f"Site directory {instance_dir} does not contain invenio.cfg",
            will_fix=will_fix,
        )
    if not target_variables.exists():
        check_failed(
            f"Site directory {instance_dir} does not contain variables file",
            will_fix=will_fix,
        )


def install_invenio_cfg(config: OARepoConfig, **kwargs):
    instance_dir = config.invenio_instance_path
    instance_dir.mkdir(exist_ok=True, parents=True)

    target_invenio_cfg = instance_dir / "invenio.cfg"
    target_variables = instance_dir / "variables"

    if not target_invenio_cfg.exists():
        target_invenio_cfg.symlink_to(config.repository_dir / "invenio.cfg")
    if not target_variables.exists():
        target_variables.symlink_to(config.repository_dir / "variables")
