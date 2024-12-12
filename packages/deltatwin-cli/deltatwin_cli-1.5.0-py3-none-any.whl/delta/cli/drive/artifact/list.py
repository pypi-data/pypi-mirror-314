import json

import click
from humanize import naturalsize

from delta.cli.utils import Utils, API
from rich.console import Console
from rich.table import Table


@click.help_option("--help", "-h")
@click.command(
    'list',
    short_help='List the artifacts for a DeltaTwin component')
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
    help='Format of the output json/text default is text')
@click.option(
    '--visibility',
    '-v',
    type=str,
    default=None,
    help='Set a filter to retrieve Artifact depending on its visibility')
@click.option(
    '--author',
    '-a',
    type=str,
    default=None,
    help='Set a filter to retrieve Artifact depending on is author')
@click.option(
    '--deltatwin-name',
    '-d',
    type=str,
    default=None,
    help='Set a filter to retrieve Artifact depending '
         'on is DeltaTwin component name')
def list_artifact(conf, format_output: str, visibility: str,
                  author: str, deltatwin_name: str) -> None:
    """List the artifacts of a DeltaTwin component

    **Example:** deltatwin drive artifact list
    """
    if visibility is None:
        artifacts = (API.list_artifact(conf, 'private', deltatwin_name) +
                     API.list_artifact(conf, 'public', deltatwin_name))
    else:
        artifacts = API.list_artifact(conf, visibility, deltatwin_name)

    artifacts = Utils.filter_artefacts(artifacts, author)

    data = []

    for art in artifacts:
        data.append(
            {
                'artefact_id': art['artefact_id'],
                'name': art['name'],
                'publication_date': Utils.format_date(
                    art['publication_date'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                'author': art['author'],
                'size': art['size'],
                'visibility': art['visibility'],
                'description': art['description'],
                'topics': art['topics'],
                'twin_name': f"{art['twin_name']}:{art['twin_version']}"
            }
        )

    if format_output is not None and format_output.lower() == 'json':
        click.echo(json.dumps(data, indent=4))
        return

    if isinstance(data, list):
        if len(data) == 0:
            click.echo(f"{Utils.log_info} No artifact found")

        table = Table(show_lines=True)
        table.add_column("Id", no_wrap=True)
        table.add_column('Name')
        table.add_column('Publication Date')
        table.add_column('Author')
        table.add_column('Size')
        table.add_column('Visibility')
        table.add_column('Description')
        table.add_column('Topics')
        table.add_column('DeltaTwin')

        for artifact in data:
            rows = (artifact['artefact_id'],
                    artifact['name'],
                    str(artifact['publication_date']),
                    str(artifact['author']),
                    naturalsize(artifact['size']),
                    str(artifact['visibility']),
                    str(artifact['description']),
                    str(", ".join(artifact['topics'])),
                    str(artifact['twin_name'])
                    )

            table.add_row(*rows)
        console = Console()
        console.print(table)
