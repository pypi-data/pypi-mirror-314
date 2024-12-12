import json
import sys

import click
from delta.core import DeltaCore
from rich.table import Table
from rich.console import Console

from delta.cli.utils import Utils, ReturnCode

RESOURCE_NAME = "Name"
RESOURCE_PATH = "PATH"


@click.command(
    'list',
    short_help='List all the resources from the working DeltaTwin component.'
)
@click.option(
    '--format-output',
    '-f',
    type=str,
    default=None,
    help='Format of the output json/text default is text')
@click.help_option("--help", "-h")
def list_resource(format_output):
    """
    List the resources from the working DeltaTwin.
    """
    try:
        with DeltaCore() as core:
            data = core.drive_get_resources()
    except FileNotFoundError:
        click.echo(f"{Utils.log_error} No manifest.json found")
        sys.exit(ReturnCode.USAGE_ERROR)

    if data is None:
        data = []

    if format_output is not None and format_output.lower() == 'json':
        click.echo(json.dumps(data, indent=4))
    else:
        if isinstance(data, list):
            table = Table()
            table.add_column(RESOURCE_NAME)
            table.add_column(RESOURCE_PATH)

            for item in data:
                table.add_row(
                    item['name'],
                    item['source_url'])

            console = Console()
            console.print(table)
