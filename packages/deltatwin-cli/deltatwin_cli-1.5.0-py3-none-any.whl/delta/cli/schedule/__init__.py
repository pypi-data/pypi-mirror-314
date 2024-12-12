import click

from delta.cli.schedule.delete import delete_deltatwin_schedule
from delta.cli.schedule.get import get_deltatwin_schedule
from delta.cli.schedule.list import list_deltatwin_schedule
from delta.cli.schedule.pause import pause_deltatwin_schedule
from delta.cli.schedule.resume import resume_deltatwin_schedule
from delta.cli.schedule.add import add_deltatwin_schedule


@click.help_option("--help", "-h")
@click.group(
    help='DeltaTwin run at a certain date/period. '
         'DeltaTwin schedule allow the user, to schedule a certain date,'
         'or on a period the start of a run, to pause, delete or view'
         'the list of all schedule plan'
)
def schedule():
    pass


# Manage schedule
schedule.add_command(add_deltatwin_schedule)
schedule.add_command(list_deltatwin_schedule)
schedule.add_command(delete_deltatwin_schedule)
schedule.add_command(get_deltatwin_schedule)
schedule.add_command(resume_deltatwin_schedule)
schedule.add_command(pause_deltatwin_schedule)
