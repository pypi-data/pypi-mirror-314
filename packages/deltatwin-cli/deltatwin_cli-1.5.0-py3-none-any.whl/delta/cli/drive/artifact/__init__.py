import click

from delta.cli.drive.artifact.delete import delete_artifact
from delta.cli.drive.artifact.list import list_artifact
from delta.cli.drive.artifact.get import get_artifact
from delta.cli.drive.artifact.add import add_artifact


@click.help_option("--help", "-h")
@click.group(
    help='DeltaTwin artifact stores output Data of Delta component runs.'
)
def artifact():
    pass


artifact.add_command(list_artifact)
artifact.add_command(get_artifact)
artifact.add_command(add_artifact)
artifact.add_command(delete_artifact)
