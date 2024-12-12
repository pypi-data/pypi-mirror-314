import json
import sys

import click

from rich.console import Console
from rich.table import Table


from delta.cli.utils import (
    Utils, API, ReturnCode,
    RUN_STATUS, RUN_AUTHOR, RUN_DATE, RUN_ID
)

DEFAULT_LIMIT = 15


def format_runs(runs: list):
    new_runs = []
    for run in runs:
        new_runs.append(
            {
                'id': run['run_id'],
                'generation_date': Utils.format_date(run['generation_date']),
                'author': run['author'],
                'status': run['status']
            }
        )
    return new_runs


@click.help_option("--help", "-h")
@click.command(
    name='list',
    short_help='List run history')
@click.option(
    '--conf',
    '-c',
    type=str,
    default=None,
    help='Path to the conf file')
@click.option(
    '--format-output',
    '-f',
    type=str,
    default=None,
    help='Format of the output (json/text). Default is text')
@click.option(
    '--limit',
    '-l',
    type=int,
    help=f'Maximal number of run entries to return default : {DEFAULT_LIMIT}',
    default=DEFAULT_LIMIT)
@click.option(
    '--offset',
    '-o',
    type=int,
    help='Number of runs entries to "skip" default 0 (no offset)',
    default=0)
@click.option(
    '--status',
    '-s',
    type=str,
    help='Filter runs by a status: '
         '"CREATED", "RUNNING", "SUCCEEDED", "ERROR"')
@click.argument('twin_name')
def list_deltatwin_executions(conf, twin_name, format_output: str,
                              limit: int, offset: int,
                              status: str = None) -> None:
    """List DeltaTwin component run history.
    TWIN_NAME : Name of the DeltaTwin component [MANDATORY]
    """
    if limit <= 0:
        click.echo(f'{Utils.log_error} Limit must be greater than 0')
        sys.exit(ReturnCode.INPUT_ERROR)

    runs = API.list_runs(conf, twin_name, status, limit, offset)

    runs = format_runs(runs)

    if Utils.output_as_json(format_output, runs):
        click.echo(json.dumps(runs, indent=4))
        return

    if isinstance(runs, list):
        if len(runs) == 0:
            click.echo(f"{Utils.log_info} No run found.")
            return
        table = Table()
        table.add_column(RUN_ID, no_wrap=True)
        table.add_column(RUN_DATE)
        table.add_column(RUN_AUTHOR)
        table.add_column(RUN_STATUS)

        # final_data = data[~np.isnan(data).any(axis=1), :]
        final_data = runs
        for run in final_data:
            status = run['status']
            run_id = run['id']

            color = Utils.get_status_color(status)

            table.add_row(
                str(run_id), run['generation_date'],
                run['author'],
                f"[{color}]{status}[/{color}]")

        console = Console()
        console.print(table)
