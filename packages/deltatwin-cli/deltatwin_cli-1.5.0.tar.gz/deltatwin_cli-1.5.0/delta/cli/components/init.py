import click
from delta.core.delta_core import DeltaCore

from delta.cli.utils import Utils


@click.command(
    'init',
    short_help='Create locally an empty DeltaTwin repository')
@click.argument('directory',
                type=str)
@click.help_option("--help", "-h")
def init(directory):
    """Create locally an empty DeltaTwin repository.

    The DIRECTORY automatically contains subdirectories and files
    used to manage a DeltaTwin.

    Typically, there are resources, artifacts, sources and models folders.
    It also contains the manifest file, which contains the DeltaTwin
    description and workflow file that describes the sequence of steps
    to proceed during the run process.

    \b
    MANDATORY ARGUMENT:
    \b
    DIRECTORY : path to the folder containing the DeltaTwin components
    """
    with DeltaCore() as core:
        core.drive_init(directory)
    click.echo(f"{Utils.log_info} DeltaTwin {directory} created")
