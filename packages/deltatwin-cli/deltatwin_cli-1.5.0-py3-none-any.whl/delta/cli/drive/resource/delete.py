import sys

import click
from delta.core import DeltaCore

from delta.cli.utils import Utils, ReturnCode


@click.command(
    'delete',
    short_help='Delete a resource from the working DeltaTwin component'
)
@click.argument('name')
@click.help_option("--help", "-h")
def delete_resource(name):
    """Delete a resource from the DeltaTwin component resources list.

    NAME: by which the resource is referenced. [MANDATORY]
    """

    try:
        with DeltaCore() as core:
            core.drive_delete_resource(name=name)
    except FileNotFoundError:
        click.echo(f"{Utils.log_error} No manifest.json found")
        sys.exit(ReturnCode.USAGE_ERROR)
