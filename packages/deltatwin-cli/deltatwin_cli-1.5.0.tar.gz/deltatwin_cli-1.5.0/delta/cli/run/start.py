import json

import click

from delta.cli.utils import Utils, API


def format_run(run: dict):
    return {
        'run_id': run['run_id'],
        'author': run['author'],
        'generation_date': Utils.format_date(
            run['generation_date'],
            "%Y-%m-%dT%H:%M:%S.%fZ"
        ),
        'status': run['status'],
        'inputs': run['inputs'],
        'outputs': run['outputs']
    }


@click.help_option("--help", "-h")
@click.command(
    'start',
    short_help='Start the DeltaTwin component execution')
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
    '--input_run',
    '-i',
    type=(str, str),
    default=None,
    multiple=True,
    help='Define each input of a run, example: bandName B1')
@click.option('--version', '-v', type=str, default=None,
              help='Specify the version of the DeltaTwin component, if '
                   'none given the latest version will be started.'
              )
@click.argument('twin_name')
def start(conf, twin_name, input_file, format_output, input_run, version):
    """Start the DeltaTwin component execution with the expected inputs.
    TWIN_NAME : Name of the DeltaTwin component [MANDATORY]
    """

    run = API.start_run(conf, twin_name, input_file, input_run, version)
    run = format_run(run)
    if Utils.output_as_json(format_output, run):
        click.echo(json.dumps(run, indent=4))
    else:
        Utils.display_run_detailed(run)
