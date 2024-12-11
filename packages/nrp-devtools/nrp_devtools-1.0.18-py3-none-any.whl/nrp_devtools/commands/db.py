from nrp_devtools.commands.check import check_failed
from nrp_devtools.commands.invenio import get_repository_info
from nrp_devtools.commands.utils import run_cmdline
from nrp_devtools.config import OARepoConfig


def check_db(config: OARepoConfig, context=None, will_fix=False, **kwargs):
    repository_info = get_repository_info(config, context)
    db_status = repository_info["db"]

    if db_status != "ok":
        check_failed(
            f"Database is not ready, it reports status {db_status}.",
            will_fix=will_fix,
        )


def fix_db(config: OARepoConfig, context=None, **kwargs):
    repository_info = get_repository_info(config, context)
    db_status = repository_info["db"]

    if db_status == "not_initialized":
        run_cmdline(config.invenio_command, "db", "create")
    elif db_status == "migration_pending":
        run_cmdline(config.invenio_command, "alembic", "upgrade", "heads")
    else:
        raise Exception(f'db error not handled: "{db_status}"')

    # make the repository info reinitialize during the next check
    context.pop("repository_info")
