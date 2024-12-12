import json
import os.path
import re
import sys

import click

from delta.cli.utils import Utils, API, ReturnCode

RUN_STATUS = "Status"
RUN_DATE = "Creation Date"
RUN_ID = "Id"
RUN_AUTHOR = "Author"
RUN_MESSAGE = "Message"


@click.command(
    name='get',
    short_help='Gets detailed information on a DeltaTwin component execution')
@click.help_option("--help", "-h")
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
    '--output-name',
    '-o',
    type=str,
    default=None,
    help='Name of the output')
@click.option(
    '--file',
    '-F',
    type=str,
    default=None,
    help='Path of the file to save output. By default '
         'it is the basename of output in current directory')
@click.option(
    '--download',
    '-d',
    type=bool,
    required=False,
    is_flag=True,
    default=False)
@click.argument('run_id')
def get_deltatwin_execution(conf, run_id, format_output,
                            download,  output_name: str, file: str):
    """Get a run of a DeltaTwin component.

    RUN_ID: the id of the run to retrieve [MANDATORY]

    Example:

    deltatwin run get 5e8f6a4f-3a83-4f41-ae28-99ce831a9861

    deltatwin run get 5e8f6a4f-3a83-4f41-ae28-99ce831a9861
    --output-name out --download
    """
    if download:
        resp = API.download_run(conf, run_id, output_name)

        if file is None:
            d = resp.headers['content-disposition']
            file = re.findall("filename=(.+)", d)[0]
        elif os.path.isdir(file):
            d = resp.headers['content-disposition']
            file = os.path.join(file, re.findall("filename=(.+)", d)[0])

        try:
            with open(file, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    # if chunk:
                    f.write(chunk)
        except IsADirectoryError:
            click.echo(f"{Utils.log_error} The path {file} "
                       f"to download the output seems wrong")
            sys.exit(ReturnCode.INPUT_ERROR)

        click.echo(f"{Utils.log_info} Output \"{output_name}\" successfully "
                   f"downloaded in \"{file}\"")

    else:
        run = API.get_run(conf, run_id)
        run['generation_date'] = Utils.format_date(run['generation_date'])
        if Utils.output_as_json(format_output, run):
            click.echo(json.dumps(run, indent=4))
        else:
            Utils.display_run_detailed(run)
