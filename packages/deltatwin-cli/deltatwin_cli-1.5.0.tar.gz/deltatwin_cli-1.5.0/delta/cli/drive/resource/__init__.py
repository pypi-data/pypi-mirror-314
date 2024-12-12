import click

from delta.cli.drive.resource.add import add_resource
from delta.cli.drive.resource.delete import delete_resource
from delta.cli.drive.resource.list import list_resource
from delta.cli.drive.resource.sync import sync


@click.help_option("--help", "-h")
@click.group(help='DeltaTwin drive resource is dedicated '
                  'to handle DeltaTwin project resources. '
                  'It allows the user, to add resources and give '
                  'the option to download the given resource, '
                  'to delete resources and to list all '
                  'the resources of a DeltaTwin.',
             short_help='DeltaTwin drive resource is dedicated to manage '
                        'DeltaTwin project resources.'
             )
def resource():
    pass


resource.add_command(add_resource)
resource.add_command(delete_resource)
resource.add_command(list_resource)
resource.add_command(sync)
