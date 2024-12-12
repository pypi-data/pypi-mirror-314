import click

from delta.cli.components.delete import delete_deltatwin_info
from delta.cli.components.get import get_deltatwin_info
from delta.cli.components.list import list_deltatwins
from delta.cli.components.build import build
from delta.cli.components.init import init
from delta.cli.components.publish import publish_dt


@click.help_option("--help", "-h")
@click.group(
    help='DeltaTwin component, '
         'is used to create and manage DeltaTwin projects.'
)
def component():
    pass


component.add_command(build)
component.add_command(delete_deltatwin_info)
component.add_command(get_deltatwin_info)
component.add_command(init)
component.add_command(list_deltatwins)
component.add_command(publish_dt)
