import os
import re
from pathlib import Path

import click

from nrp_devtools.commands.check import CheckFailedException
from nrp_devtools.commands.db import check_db, fix_db
from nrp_devtools.commands.invenio import get_invenio_configuration
from nrp_devtools.commands.utils import run_cmdline
from nrp_devtools.config import OARepoConfig


def build_alembic(config):
    click.secho(f"Generating alembic", fg="yellow")

    alembic_path = config.shared_dir / "alembic"
    branch = config.repository.repository_package
    setup_alembic(config, branch, alembic_path)

    click.secho(f"Alembic successfully generated", fg="green")


def setup_alembic(config: OARepoConfig, branch: str, alembic_path: Path):
    filecount = len(
        [x for x in alembic_path.iterdir() if x.is_file() and x.name.endswith(".py")]
    )

    if filecount < 2:
        intialize_alembic(config, branch, alembic_path)
    else:
        update_alembic(config, branch, alembic_path)


def update_alembic(config: OARepoConfig, branch, alembic_path):
    # alembic has been initialized, update heads and generate

    invenio_alembic_path = convert_to_invenio_alembic_path(config, alembic_path)

    files = [file_path.name for file_path in alembic_path.iterdir()]
    file_numbers = []
    for file in files:
        file_number_regex = re.findall(f"(?<={branch}_)\d+", file)
        if file_number_regex:
            file_numbers.append(int(file_number_regex[0]))
    new_file_number = max(file_numbers) + 1
    revision_message, file_revision_name_suffix = get_revision_names(
        "Nrp install revision."
    )
    run_cmdline(
        config.invenio_command, "alembic", "upgrade", "heads", cwd=config.repository_dir
    )

    new_revision = get_revision_number(
        run_cmdline(
            config.invenio_command,
            "alembic",
            "revision",
            revision_message,
            "-b",
            branch,
            "--path",
            invenio_alembic_path,
            grab_stdout=True,
            cwd=config.repository_dir,
        ),
        file_revision_name_suffix,
    )
    rewrite_revision_file(alembic_path, new_file_number, branch, new_revision)
    fix_sqlalchemy_utils(alembic_path)
    run_cmdline(
        config.invenio_command, "alembic", "upgrade", "heads", cwd=config.repository_dir
    )


def convert_to_invenio_alembic_path(config, alembic_path):
    (alembic_locations,) = get_invenio_configuration(config, {}, "ALEMBIC_LOCATIONS")
    resolved_alembic_path = alembic_path.resolve()
    for loc in alembic_locations:
        if Path(loc).resolve() == resolved_alembic_path:
            return loc
    raise ValueError(
        f"Could not find alembic path {alembic_path} in registered invenio alemibc locations: {alembic_locations}"
    )


def intialize_alembic(config, branch, alembic_path):
    initialize_db_if_not_initialized(config)

    # alembic has not been initialized yet ...
    run_cmdline(
        config.invenio_command,
        "alembic",
        "upgrade",
        "heads",
        cwd=config.repository_dir,
    )

    # create model branch
    revision_message, file_revision_name_suffix = get_revision_names(
        f"Create {branch} branch."
    )

    invenio_alembic_path = convert_to_invenio_alembic_path(config, alembic_path)

    new_revision = get_revision_number(
        run_cmdline(
            config.invenio_command,
            "alembic",
            "revision",
            revision_message,
            "-b",
            branch,
            "-p",
            "dbdbc1b19cf2",
            "--empty",
            "--path",
            invenio_alembic_path,
            cwd=config.repository_dir,
            grab_stdout=True,
        ),
        file_revision_name_suffix,
    )
    rewrite_revision_file(alembic_path, "1", branch, new_revision)
    fix_sqlalchemy_utils(alembic_path)
    run_cmdline(
        config.invenio_command, "alembic", "upgrade", "heads", cwd=config.repository_dir
    )

    revision_message, file_revision_name_suffix = get_revision_names(
        "Initial revision."
    )
    new_revision = get_revision_number(
        run_cmdline(
            config.invenio_command,
            "alembic",
            "revision",
            revision_message,
            "-b",
            branch,
            "--path",
            invenio_alembic_path,
            cwd=config.repository_dir,
            grab_stdout=True,
        ),
        file_revision_name_suffix,
    )
    rewrite_revision_file(alembic_path, "2", branch, new_revision)
    # the link to down-revision is created correctly after alembic upgrade heads
    # on the corrected file, explicit rewrite of down-revision is not needed
    fix_sqlalchemy_utils(alembic_path)
    run_cmdline(
        config.invenio_command, "alembic", "upgrade", "heads", cwd=config.repository_dir
    )


def fix_sqlalchemy_utils(alembic_path):
    for fn in alembic_path.iterdir():
        if not fn.name.endswith(".py"):
            continue
        data = fn.read_text()

        empty_migration = '''
def upgrade():
"""Upgrade database."""
# ### commands auto generated by Alembic - please adjust! ###
pass
# ### end Alembic commands ###'''

        if re.sub(r"\s", "", empty_migration) in re.sub(r"\s", "", data):
            click.secho(f"Found empty migration in file {fn}, deleting it", fg="yellow")
            fn.unlink()
            continue

        modified = False
        if "import sqlalchemy_utils" not in data:
            data = "import sqlalchemy_utils\n" + data
            modified = True
        if "import sqlalchemy_utils.types" not in data:
            data = "import sqlalchemy_utils.types\n" + data
            modified = True
        if modified:
            fn.write_text(data)


def get_revision_number(stdout_str, file_suffix):
    mtch = re.search(f"(\w{{12}}){file_suffix}", stdout_str)
    if not mtch:
        raise ValueError("Revision number was not found in revision create stdout")
    return mtch.group(1)


def get_revision_names(revision_message):
    file_name = revision_message[0].lower() + revision_message[1:]
    file_name = "_" + file_name.replace(" ", "_")
    if file_name[-1] == ".":
        file_name = file_name[:-1]

    file_name = file_name[:30]  # there seems to be maximum length for the file name
    idx = file_name.rfind("_")
    file_name = file_name[:idx]  # and all words after it are cut
    return revision_message, file_name


def rewrite_revision_file(
    alembic_path, new_id_number, revision_id_prefix, current_revision_id
):
    files = list(alembic_path.iterdir())
    files_with_this_revision_id = [
        file_name for file_name in files if current_revision_id in str(file_name)
    ]

    if not files_with_this_revision_id:
        raise ValueError(
            "Alembic file rewrite couldn't find the generated revision file"
        )

    if len(files_with_this_revision_id) > 1:
        raise ValueError("More alembic files with the same revision number found")

    target_file = str(files_with_this_revision_id[0])
    new_id = f"{revision_id_prefix}_{new_id_number}"
    with open(target_file, "r") as f:
        file_text = f.read()
        file_text = file_text.replace(
            f"revision = '{current_revision_id}'", f"revision = '{new_id}'"
        )
    with open(target_file.replace(current_revision_id, new_id), "w") as f:
        f.write(file_text)
    os.remove(target_file)


def initialize_db_if_not_initialized(config):
    try:
        check_db(config, {}, will_fix=True)
    except CheckFailedException:
        fix_db(config, {})
