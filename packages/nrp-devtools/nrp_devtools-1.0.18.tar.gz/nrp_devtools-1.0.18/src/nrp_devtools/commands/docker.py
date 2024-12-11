import re
import time
import traceback
from urllib.parse import urlparse

import click
import pika
import psycopg
import redis
from minio import Minio
from opensearchpy import OpenSearch

from nrp_devtools.commands.utils import run_cmdline
from nrp_devtools.config import OARepoConfig

from .check import check_failed
from .invenio import get_invenio_configuration, get_repository_info


def check_docker_env(config: OARepoConfig, will_fix=False, **kwargs):
    if not (config.repository_dir / "docker" / ".env").exists():
        check_failed(
            "Docker environment file is missing. Please run this command with --fix to fix the problem.",
            will_fix=will_fix,
        )


def fix_docker_env(config: OARepoConfig, **kwargs):
    (config.repository_dir / "docker" / ".env").symlink_to(
        config.repository_dir / "variables"
    )


def check_docker_callable(config: OARepoConfig, will_fix=False, **kwargs):
    try:
        run_cmdline("docker", "ps", grab_stdout=True, raise_exception=True)
    except:  # noqa
        check_failed(
            "Docker is not callable. Please install docker and make sure it is running.",
            will_fix=will_fix,
        )


def check_version(*args, expected_major, expected_minor=None, strict=False):
    try:
        result = run_cmdline(*args, grab_stdout=True, raise_exception=True)
    except:
        check_failed(f"Command {' '.join(args)} is not callable.")
    version_result = re.search(r".*?([0-9]+)\.([0-9]+)\.([0-9]+)", result)
    major = int(version_result.groups()[0])
    minor = int(version_result.groups()[1])
    if strict:
        if isinstance(expected_major, (list, tuple)):
            assert (
                major in expected_major
            ), f"Expected major version to be one of {expected_major}, found {major}"
        else:
            assert (
                major == expected_major
            ), f"Expected major version to be one {expected_major}, found {major}"
            if expected_minor:
                assert minor == expected_minor
    elif not (
        major > expected_major or (major == expected_major and minor >= expected_minor)
    ):
        raise Exception("Expected docker compose version ")


def check_docker_compose_version(config, expected_major, expected_minor):
    check_version(
        "docker",
        "compose",
        "version",
        expected_major=expected_major,
        expected_minor=expected_minor,
    )


def check_node_version(config, supported_versions):
    check_version("node", "--version", expected_major=supported_versions, strict=True)


def check_npm_version(config, supported_versions):
    check_version("npm", "--version", expected_major=supported_versions, strict=True)


def retry(fn, config, context, tries=10, timeout=1, verbose=False):
    click.secho(f"Calling {fn.__name__}", fg="yellow")
    for i in range(tries):
        try:
            fn(config, context)
            click.secho(f"  ... alive", fg="green")
            return
        except KeyboardInterrupt:
            raise
        except BaseException as e:
            # catch SystemExit as well
            if verbose:
                click.secho(traceback.format_exc(), fg="red")
            if i == tries - 1:
                click.secho(f" ... failed", fg="red")
                raise
            click.secho(
                f" ... not yet ready, sleeping for {int(timeout)} seconds",
                fg="yellow",
            )
            time.sleep(int(timeout))
            nt = timeout * 1.5
            if int(nt) == int(timeout):
                timeout = timeout + 1
            else:
                timeout = nt


def check_containers(
    config: OARepoConfig,
    *,
    context,
    fast_fail=False,
    verbose=False,
    will_fix=False,
    **kwargs,
):
    def test_docker_containers_accessible(*_, **__):
        # pass empty context to prevent caching of the repository info
        repository_info = get_repository_info(config, context={})
        if repository_info["db"] == "connection_error":
            check_failed(
                "Database container is not running or is not accessible.",
                will_fix=will_fix,
            )
        else:
            click.secho("    Database is alive", fg="green")
        if repository_info["opensearch"] == "connection_error":
            check_failed(
                "OpenSearch container is not running or is not accessible.",
                will_fix=will_fix,
            )
        else:
            click.secho("    OpenSearch is alive", fg="green")
        if repository_info["files"] == "connection_error":
            check_failed(
                "S3 container (minio) is not running or is not accessible.",
                will_fix=will_fix,
            )
        else:
            click.secho("    S3 is alive", fg="green")
        if repository_info["mq"] == "connection_error":
            check_failed(
                "Message queue container (rabbitmq) is not running or is not accessible.",
                will_fix=will_fix,
            )
        else:
            click.secho("    Message queue is alive", fg="green")
        if repository_info["cache"] == "connection_error":
            check_failed(
                "Cache container (redis) is not running or is not accessible.",
                will_fix=will_fix,
            )
        else:
            click.secho("    Cache is alive", fg="green")

    if fast_fail:
        test_docker_containers_accessible()
    else:
        retry(
            test_docker_containers_accessible,
            config,
            context,
            verbose=verbose,
        )


def fix_containers(config: OARepoConfig, *, context, **kwargs):
    run_cmdline(
        "docker",
        "compose",
        "up",
        "-d",
        "cache",
        "db",
        "mq",
        "search",
        "s3",
        cwd=config.repository_dir / "docker",
    )


def split_url(url):
    parsed_url = urlparse(url)
    return (
        parsed_url.hostname,
        parsed_url.port,
        parsed_url.username,
        parsed_url.password,
        parsed_url.path[1:],
    )


def check_docker_redis(config, context):
    (redis_url,) = get_invenio_configuration(config, context, "CACHE_REDIS_URL")
    host, port, username, password, db = split_url(redis_url)
    pool = redis.ConnectionPool(
        host=host, port=port, db=db, username=username, password=password
    )
    r = redis.Redis(connection_pool=pool)
    r.keys("blahblahblah")  # fails if there is no connection
    pool.disconnect()


def check_docker_db(config, context):
    host, port, user, password, dbname = split_url(
        get_invenio_configuration(
            config,
            context,
            "SQLALCHEMY_DATABASE_URI",
        )[0]
    )

    with psycopg.connect(
        dbname=dbname, host=host, port=port, user=user, password=password
    ) as conn:
        assert conn.execute("SELECT 1").fetchone()[0] == 1


def check_docker_mq(config, context):
    host, port, user, password, _ = split_url(
        get_invenio_configuration(
            config,
            context,
            "CELERY_BROKER_URL",
        )[0]
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=pika.credentials.PlainCredentials(user, password),
        )
    )
    channel = connection.channel()
    connection.process_data_events(2)
    assert connection.is_open
    connection.close()


def check_docker_s3(config, context):
    endpoint_url, access_key, secret_key = get_invenio_configuration(
        config, context, "S3_ENDPOINT_URL", "S3_ACCESS_KEY_ID", "S3_SECRET_ACCESS_KEY"
    )
    (host, port, *_) = split_url(endpoint_url)

    client = Minio(
        f"{host}:{port}",
        access_key=access_key,
        secret_key=secret_key,
        secure=False,
    )
    client.list_buckets()


def check_docker_search(config, context):
    (
        search_hosts,
        search_config,
        prefix,
    ) = get_invenio_configuration(
        config,
        context,
        "SEARCH_HOSTS",
        "SEARCH_CLIENT_CONFIG",
        "SEARCH_INDEX_PREFIX",
    )
    client = OpenSearch(
        hosts=[{"host": search_hosts[0]["host"], "port": search_hosts[0]["port"]}],
        use_ssl=search_config.get("use_ssl", False),
        verify_certs=search_config.get("verify_certs", False),
        ssl_assert_hostname=search_config.get("ssl_assert_hostname", False),
        ssl_show_warn=search_config.get("ssl_show_warn", False),
        ca_certs=search_config.get("ca_certs", None),
    )
    info = client.info(pretty=True)
