from urllib.parse import urlparse

from minio import Minio

from nrp_devtools.commands.check import check_failed
from nrp_devtools.commands.invenio import get_invenio_configuration, get_repository_info
from nrp_devtools.commands.utils import run_cmdline
from nrp_devtools.config import OARepoConfig


def check_s3_location_in_database(
    config: OARepoConfig, context=None, will_fix=False, **kwargs
):
    s3_location_status = get_repository_info(config, context)["files"]
    if s3_location_status == "default_location_missing":
        check_failed(
            f"S3 location is missing from the database.",
            will_fix=will_fix,
        )


DEFAULT_BUCKET_NAME = "default"


def fix_s3_location_in_database(config: OARepoConfig, context=None, **kwargs):
    s3_location_status = get_repository_info(config, context)["files"]
    if s3_location_status == "default_location_missing":
        run_cmdline(
            config.invenio_command,
            "files",
            "location",
            "default",
            f"s3://{DEFAULT_BUCKET_NAME}",
            "--default",
        )

    # make the repository info reinitialize during the next check
    context.pop("repository_info")


def check_s3_bucket_exists(
    config: OARepoConfig, context=None, will_fix=False, **kwargs
):
    s3_location_status = get_repository_info(config, context)["files"]
    if s3_location_status.startswith("bucket_does_not_exist:"):
        check_failed(
            f"S3 bucket {s3_location_status.split(':')[1]} does not exist.",
            will_fix=will_fix,
        )


def fix_s3_bucket_exists(config: OARepoConfig, context=None, **kwargs):
    s3_endpoint_url, access_key, secret_key = get_invenio_configuration(
        config,
        context,
        "S3_ENDPOINT_URL",
        "S3_ACCESS_KEY_ID",
        "S3_SECRET_ACCESS_KEY",
    )
    parsed_s3_endpoint_url = urlparse(s3_endpoint_url)
    host = parsed_s3_endpoint_url.hostname
    port = parsed_s3_endpoint_url.port

    client = Minio(
        f"{host}:{port}",
        access_key=access_key,
        secret_key=secret_key,
        secure=False,
    )

    bucket_name = "default"

    client.make_bucket(bucket_name)

    # make the repository info reinitialize during the next check
    context.pop("repository_info")
