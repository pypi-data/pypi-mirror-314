import json

import click
from datetime import datetime, timedelta, timezone

from delta.cli.schedule.utils import display_schedule_detailed
from delta.cli.utils import Utils, API


@click.help_option("--help", "-h")
@click.command(
    'add',
    short_help='Add a new DeltaTwin component schedule execution')
@click.option(
    '--conf',
    '-c',
    type=str,
    default=None,
    help='Path to the conf file')
@click.option(
    '--input-file',
    '-I',
    type=str,
    default=None,
    help='Inputs of run in json format, example: /mypath/inputs.json '
         'the json is defined like [{"name": "angle", "value": "45"},'
         '{"name": "image", "value": "http/myimg/$value"}]')
@click.option(
    '--format-output',
    '-f',
    type=str,
    default=None,
    help='format of the output json/text default is text')
@click.option(
    '--category',
    '-C',
    type=click.Choice(['date', 'cron'], case_sensitive=False),
    help='type of schedule date or a periodic start')
@click.option(
    '--schedule',
    '-s',
    type=str,
    help='When to start the scheduled run.')
@click.option(
    '--name',
    '-n',
    type=str,
    required=True,
    help='name to identify the scheduled run.')
@click.option(
    '--input_run',
    '-i',
    type=(str, str),
    default=None,
    multiple=True,
    help='Define each input of a run, example: bandName B1')
@click.argument('twin_name')
def add_deltatwin_schedule(
        conf, twin_name, category, schedule,
        name, input_file, input_run, format_output
):
    """Add a new planned execution with
    the expected inputs. The DeltaTwin component execution
    can be set to be executed at a certain date using the date
    type of schedule, or it can be executed at a periodic
    start using the type cron.

    To schedule a cron execution you can for exemple set "5 4 * * *"
    every 4 hours and 5 minutes.

    The format "* * * * *" corresponds to
    "minute, hour, day (month), month, day (week)"

    To set a specific date for the execution of the DeltaTwin component,
    the format is "YYYY-MM-DD HH:MM:SS"

    TWIN_NAME : Name of the DeltaTwin component [MANDATORY]
    """

    run = API.start_scheduled_run(
        conf,
        twin_name,
        input_file,
        input_run,
        category,
        schedule,
        name
    )
    if Utils.output_as_json(format_output, run):
        click.echo(json.dumps(run, indent=4))
    else:
        display_schedule_detailed(run)
