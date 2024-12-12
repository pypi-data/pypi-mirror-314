import sys

import click
from delta.core import DeltaCore
from delta.cli.utils import ReturnCode


@click.command(
    "build", short_help="Build the DeltaTwin image with a (user) provided tag"
)
@click.option(
    "--tag",
    "-t",
    type=str,
    default="latest",
    help="The (build) image tag name. Default value is 'latest'",
)
@click.option(
    "--registry",
    "-r",
    type=str,
    default="docker.io",
    help="The user defined registry. Default value is 'docker.io'",
)
@click.help_option("--help", "-h")
def build(tag, registry):
    """Build the DeltaTwin image with a (user) provided tag

    \b
    🛈 This command must be executed on the directory of the DeltaTwin

    \b
    Example:
        cd <delta_twin_directory>
        deltatwin component build --tag dev --registry registry_url
    """
    with DeltaCore() as core:
        try:
            core.drive_build(version=tag, registry=registry)
        except Exception as e:
            click.echo(f"Something went wrong when building image:\n\t{e}")
            sys.exit(ReturnCode.USAGE_ERROR)
