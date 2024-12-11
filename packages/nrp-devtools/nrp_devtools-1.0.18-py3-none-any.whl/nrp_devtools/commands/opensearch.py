from nrp_devtools.commands.check import check_failed
from nrp_devtools.commands.invenio import get_repository_info
from nrp_devtools.commands.utils import run_cmdline
from nrp_devtools.config import OARepoConfig


def check_search(config: OARepoConfig, context=None, will_fix=False, **kwargs):
    opensearch_status = get_repository_info(config, context)["opensearch"]
    if opensearch_status != "ok":
        check_failed(
            f"Search is not ready, it reports status {opensearch_status}.",
            will_fix=will_fix,
        )


def fix_search(config: OARepoConfig, context=None, **kwargs):
    opensearch_status = get_repository_info(config, context)["opensearch"]
    if opensearch_status != "ok":
        run_cmdline(config.invenio_command, "oarepo", "index", "init")
        run_cmdline(config.invenio_command, "oarepo", "cf", "init")

    # make the repository info reinitialize during the next check
    context.pop("repository_info")


def fix_custom_fields(config: OARepoConfig, context=None, **kwargs):
    run_cmdline(config.invenio_command, "oarepo", "cf", "init")

    # make the repository info reinitialize during the next check
    context.pop("repository_info")
