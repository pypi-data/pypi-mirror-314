from functools import partial

import click

from ..commands.check_old import check_imagemagick_callable
from ..commands.db import check_db, fix_db
from ..commands.docker import (
    check_containers,
    check_docker_callable,
    check_docker_compose_version,
    check_docker_env,
    check_node_version,
    check_npm_version,
    fix_containers,
    fix_docker_env,
)
from ..commands.invenio import check_invenio_cfg, install_invenio_cfg
from ..commands.opensearch import check_search, fix_custom_fields, fix_search
from ..commands.resolver import get_resolver
from ..commands.s3 import (
    check_s3_bucket_exists,
    check_s3_location_in_database,
    fix_s3_bucket_exists,
    fix_s3_location_in_database,
)
from ..commands.ui import check_ui, fix_ui
from ..commands.utils import make_step, no_args, run_fixup
from ..config import OARepoConfig
from .base import command_sequence, nrp_command
from ..pypi_proxy.proxy import start_pypi_proxy


@nrp_command.command(name="check")
@click.option("--fix", is_flag=True, default=False)
@click.option("--local-packages", "-e", multiple=True)
@command_sequence()
def check_command(*, config: OARepoConfig, local_packages=None, fix=False, **kwargs):
    "Checks prerequisites for running the repository, initializes a build environment and rebuilds the repository."
    context = {}
    return check_commands(context, config, local_packages, fix)


def check_commands(context, config, local_packages, fix):
    resolver = get_resolver(config)
    if fix:
        start_pypi_proxy(config.pypi_proxy_target)
    return (
        #
        # infrastructure checks
        #
        no_args(partial(click.secho, "Checking repository requirements", fg="yellow")),
        run_fixup(check_docker_env, fix_docker_env, fix=fix),
        check_docker_callable,
        make_step(check_docker_compose_version, expected_major=1, expected_minor=17),
        make_step(check_node_version, supported_versions=(14, 16, 20, 21)),
        make_step(check_npm_version, supported_versions=(6, 7, 8, 10)),
        check_imagemagick_callable,
        #
        # virtualenv exists
        #
        run_fixup(lambda config, **kwargs: resolver.check_virtualenv(**kwargs),
                  lambda config, **kwargs: resolver.fix_virtualenv(**kwargs), fix=fix),
        #
        # requirements have been built
        #
        run_fixup(lambda config, **kwargs: resolver.check_requirements(**kwargs),
                  lambda config, **kwargs: resolver.build_requirements(**kwargs), fix=fix),
        #
        # invenio.cfg and variables are inside virtual environment
        #
        run_fixup(check_invenio_cfg, install_invenio_cfg, fix=fix),
        #
        # can run invenio command
        #
        run_fixup(lambda config, **kwargs: resolver.check_invenio_callable(**kwargs),
                  lambda config, **kwargs: resolver.install_python_repository(**kwargs), fix=fix),
        #
        # any local packages are installed inside the virtual environment
        #
        make_step(lambda config, **kwargs: resolver.install_local_packages(**kwargs), local_packages=local_packages),
        #
        # check that docker containers are running
        #
        run_fixup(check_containers, fix_containers, context=context, fix=fix),
        #
        # check that ui is compiled
        #
        run_fixup(check_ui, fix_ui, fix=fix),
        #
        # check that database is initialized
        #
        run_fixup(check_db, fix_db, context=context, fix=fix),
        #
        # check that opensearch is initialized and contains all indices and custom fields
        #
        run_fixup(check_search, fix_search, context=context, fix=fix),
        #
        # check that s3 location inside invenio is initialized
        #
        run_fixup(
            check_s3_location_in_database,
            fix_s3_location_in_database,
            fix=fix,
            context=context,
        ),
        #
        # check that s3 bucket exists
        #
        run_fixup(
            check_s3_bucket_exists, fix_s3_bucket_exists, fix=fix, context=context
        ),
        #
        # check that custom fields have been put to opensearch.
        # currently there is no way of checking that, so will always fix it
        # (does noop if already fixed)
        #
        make_step(fix_custom_fields, context=context),
        #
        # check that fixtures are loaded into the database
        # TODO: can not do this now as the fixtures do not have a way of getting
        # their identifier. This might be fixed in the future.
        #
        # make_step(check_fixtures, context=context, fix=fix),
        no_args(partial(click.secho, "Repository ready to be run", fg="yellow")),
    )
