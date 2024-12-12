import sys

import click
from delta.core import DeltaCore

from delta.cli.utils import Utils, ReturnCode


@click.command(
    'add',
    short_help='Add a resource to the working DeltaTwin component'
)
@click.help_option("--help", "-h")
@click.option("--download", "-d",
              is_flag=True, default=False,
              help="If present the resources will be download and"
                   "put in the resources folder")
@click.argument('path')
@click.argument('filename')
def add_resource(path, filename, download):
    """Add a resource to the DeltaTwin component resources list,
    if the download
    option is present. This command will
    download the resource and put it
    in the resources folder, and add an entry in the
    resources section of the *manifest.json* file.

    PATH: fullpath, url or directory of the resources. [MANDATORY]

    FILENAME: by which the resource is referenced. [MANDATORY]
    """
    try:
        with DeltaCore() as core:
            core.drive_add_resource(path=path,
                                    name=filename, download=download)
    except FileNotFoundError:
        click.echo(f"{Utils.log_error} No manifest.json found")
        sys.exit(ReturnCode.USAGE_ERROR)
