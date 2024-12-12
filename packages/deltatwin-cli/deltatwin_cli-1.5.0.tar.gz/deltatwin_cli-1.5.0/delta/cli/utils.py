import configparser
import json
import os
import re
import sys
import time
from datetime import datetime
from typing import Callable, Any, Union

from humanize import naturalsize
from packaging.version import parse, InvalidVersion
import plotext as plt

import click
import requests
from requests.exceptions import ConnectionError, InvalidSchema, JSONDecodeError
from rich.console import Console
from rich.table import Table
import rich.box as box
from rich.padding import Padding

RUN_STATUS = "Status"
RUN_DATE = "Creation Date"
RUN_ID = "Id"
RUN_AUTHOR = "Author"
RUN_MESSAGE = "Message"


class Utils:
    log_info = click.style('INFO:', fg='green')
    log_error = click.style('ERROR:', fg='red')

    @staticmethod
    def is_valid_url(url: str):
        pattern = r'^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$'
        return bool(re.match(pattern, url))

    @staticmethod
    def retrieve_conf(conf):
        if conf is None:
            conf = os.path.expanduser('~') + '/.deltatwin/conf.ini'

        return conf

    @staticmethod
    def retrieve_token(conf):
        try:
            token = Utils.get_token(conf)
        except KeyError:
            if os.path.isfile(conf):
                API.refresh_token(conf)
                token = Utils.get_token(conf)
            else:
                click.echo(f"{Utils.log_error} No token find please use "
                           f"deltatwin login before using this command.")
                sys.exit(ReturnCode.USAGE_ERROR)
        return token

    @staticmethod
    def retrieve_harbor_token(path) -> tuple[str, str]:
        try:
            conf = Utils.read_config(path, 'SERVICES')
            return conf["harbor_access_token"], conf["harbor_refresh_token"]
        except Exception:
            return None, None

    @staticmethod
    def get_error_msg(response):
        try:
            msg = response.json()
        except JSONDecodeError:
            return None
        if 'error' in msg:
            msg = msg['error']
        elif 'detail' in msg:
            msg = msg['detail']
        return msg

    @staticmethod
    def check_status(response):
        if 400 > response.status_code >= 300:
            msg = Utils.get_error_msg(response)
            if msg is not None:
                click.echo(f"{Utils.log_error} {response.reason} "
                           f"at {response.request.url}, {msg}.")
            else:
                click.echo(f"{Utils.log_error} {response.reason} "
                           f"at {response.request.url}")
            sys.exit(ReturnCode.RESOURCE_NOT_FOUND)
        if 500 > response.status_code >= 400:
            msg = Utils.get_error_msg(response)
            if msg is not None:
                click.echo(f"{Utils.log_error} {response.reason} "
                           f"at {response.request.url}, {msg}.")
            else:
                click.echo(f"{Utils.log_error} {response.reason} "
                           f"at {response.request.url}")
            sys.exit(ReturnCode.UNAUTHORIZED)
        if response.status_code >= 500:
            click.echo(f"{Utils.log_error} {response.reason} "
                       f"at {response.request.url}.")
            sys.exit(ReturnCode.SERVICE_ERROR)

    @staticmethod
    def output_as_json(output_format, data):
        if output_format is not None and output_format.lower() == 'json':
            try:
                json.loads(json.dumps(data))
            except ValueError:
                return False
            return True
        return False

    @staticmethod
    def read_config(path: str, context: str = None):
        cfg = configparser.ConfigParser()

        if os.path.isfile(path):
            cfg.read(path)

        if context is not None:
            return dict(cfg[context])
        return cfg

    @staticmethod
    def save_config(path: str, context: str, config: dict):
        cfg = configparser.ConfigParser()

        cfg[context] = config

        with open(path, 'w') as configfile:  # save
            cfg.write(configfile)

    @staticmethod
    def get_token(path: str):
        return Utils.read_config(path, 'SERVICES')['token']

    @staticmethod
    def get_service(path: str):
        url = Utils.read_config(path, 'SERVICES')['api']
        return url[:-1] if url.endswith('/') else url

    @staticmethod
    def datetime_from_utc_to_local(utc_datetime):
        now_timestamp = time.time()
        offset = (datetime.fromtimestamp(now_timestamp)
                  - datetime.utcfromtimestamp(now_timestamp))
        return utc_datetime + offset

    @staticmethod
    def format_date(date: Union[str, datetime],
                    format: str = "%Y-%m-%dT%H:%M:%S.%f"
                    ) -> str:
        # Parse la chaîne de date dans un objet datetime
        if type(date) is str:
            date = Utils.datetime_from_utc_to_local(datetime.strptime(
                date, format)
            )

        # Formater l'objet datetime dans le format souhaité
        return date.strftime("%b %d, %Y, %I:%M:%S %p")

    @staticmethod
    def retrieve_metric_s3(metrics) -> dict:
        data = {}
        for metric in metrics:
            if metric['type'] == 's3':
                data['category'] = 'artifacts'
                data['storage_used'] = metric['occupied_size']
                data['total_objects'] = metric['total_objects']
                data['last_metric_update'] = Utils.format_date(
                    metric['metric_date'])
                return data

        data['storage_used'] = 0
        data['total_objects'] = 0
        data['last_metric_update'] = Utils.format_date(datetime.now())
        return data

    @staticmethod
    def retrieve_history_s3(metrics) -> list:
        data = []
        for metric in metrics:
            d = {}
            if metric['type'] == 's3':
                d['category'] = 'artifacts'
                d['storage_used'] = metric['occupied_size']
                d['total_objects'] = metric['total_objects']
                d['last_metric_update'] = Utils.format_date(
                    metric['metric_date'])
                data.append(d)
        if len(data) == 0:
            data.append(
                {
                    'storage_used': 0,
                    'total_objects': 0,
                    'last_metric_update': Utils.format_date(datetime.now())
                }
            )
        return data

    @staticmethod
    def format_output_json(data):
        click.echo(json.dumps(data, indent=4))

    @staticmethod
    def format_output_text_s3(data):
        if isinstance(data, list):
            if len(data) == 0:
                click.echo(f"{Utils.log_info} No artifact found")

        table = Table()
        table.add_column('Storage used')
        table.add_column('Number of Elements')
        table.add_column('Last metric update')

        rows = (str(naturalsize(data['storage_used'])),
                str(data['total_objects']),
                str(data['last_metric_update'])
                )
        table.add_row(*rows)
        console = Console()
        console.print(table)

    @staticmethod
    def format_output_text_history_s3(data):
        if isinstance(data, list):
            if len(data) == 0:
                click.echo(f"{Utils.log_info} No artifact found")

        table = Table()
        table.add_column('Storage used')
        table.add_column('Number of Elements')
        table.add_column('Last metric update (UTC)')

        for d in data:
            rows = (str(naturalsize(d['storage_used'])),
                    str(d['total_objects']),
                    str(d['last_metric_update'])
                    )
            table.add_row(*rows)
        console = Console()
        console.print(table)

    @staticmethod
    def prepare_graph_harbor(datas):
        name = []
        size = []
        for data in datas:
            name.append(data['deltatwin_name'])
            size.append(int(data['size']))
        return name, size

    @staticmethod
    def retrieve_metric_harbor(metrics) -> any:
        datas = []
        total = 0
        for metric in metrics:
            if metric['type'] == 'harbor':
                data = {
                    'category': 'harbor',
                    'deltatwin_name': metric['project_name'],
                    'size': metric['size'],
                    'last_metric_update': Utils.format_date(
                        metric['metric_date'])
                }
                datas.append(data)
                total += metric['size']
        if len(datas) == 0:
            data = {
                'category': 'harbor',
                'deltatwin_name': None,
                'size': 0,
                'last_metric_update': Utils.format_date(datetime.now())
            }
            datas.append(data)
        return datas, total

    @staticmethod
    def format_output_json_harbor(datas, total):
        datas.append({'Total_size ': total})
        click.echo(json.dumps(datas, indent=4))

    @staticmethod
    def format_output_graph_harbor(datas, total):
        console = Console(highlight=False)
        twin_name, twine_size = Utils.prepare_graph_harbor(datas)
        Utils.display_line(
            console,
            'Total occupied space',
            f" {naturalsize(total)}")

        plt.simple_bar(
            twin_name, twine_size,
            width=100,
            title='Occupied space by Deltatwin (Bytes)')
        plt.show()

    @staticmethod
    def format_output_text_harbor(datas, total):
        console = Console(highlight=False)
        Utils.display_line(
            console,
            'Total occupied space',
            f" {naturalsize(total)}")

        table = Table()
        table.add_column('DeltaTwin Name')
        table.add_column('Size')
        table.add_column('Last metric update (UTC)')

        for data in datas:
            rows = (str(data['deltatwin_name']),
                    str(naturalsize(data['size'])),
                    str(data['last_metric_update'])
                    )
            table.add_row(*rows)
        console = Console()
        console.print(table)

    @staticmethod
    def display_line(console, name, value):
        console.print(name, f"[bold]{value}[/bold]", sep=":")

    @staticmethod
    def display_run_detailed(run):
        console = Console(highlight=False)

        Utils.display_line(console, RUN_ID, run.get("run_id"))
        Utils.display_line(console, RUN_AUTHOR, run.get("author"))
        Utils.display_line(console, RUN_DATE, run.get("generation_date"))
        Utils.display_run_short(run)

    @staticmethod
    def display_run_short(run):
        status = run.get("status")
        color = Utils.get_status_color(status)
        console = Console(highlight=False)

        Utils.display_line(console, RUN_STATUS, f"[{color}]{status}[/{color}]")
        if status == "error":
            Utils.display_line(console, RUN_MESSAGE, run.get("message"))
        Utils.display_table_parameter(console, "Input", run.get("inputs"))

        Utils.display_table_parameter(console, "Output", run.get("outputs"))

    @staticmethod
    def get_status_color(status):
        color = "white"
        match status:
            case "success":
                color = "green"
            case "error":
                color = "red"
            case "running":
                color = "blue"
            case "cancelled":
                color = "magenta"
        return color

    @staticmethod
    def display_table_schedule_parameter(console, prefix, datas):
        console.print(f"{prefix}s:")

        table = Table(show_edge=False, box=box.ASCII)
        table.add_column(prefix + " name")
        table.add_column("Type")
        table.add_column("Value/Basename")
        if datas is not None:
            for data in datas:
                value = ""
                if ("value" in datas[data].keys() and
                        datas[data].get("value") is not None):
                    value = datas[data].get("value")
                elif (
                        "basename" in datas[data].keys() and
                        datas[data].get("basename") is not None
                ):
                    value = datas[data].get("basename")
                elif "url" in datas[data].keys():
                    value = datas[data].get("url")
                table.add_row(
                    data,
                    datas[data].get("param_type"),
                    str(value)
                )
        console.print(Padding(table, (0, 4)))

    @staticmethod
    def display_table_parameter(console, prefix, datas):
        console.print(f"{prefix}s:")

        table = Table(show_edge=False, box=box.ASCII)
        table.add_column(prefix + " name")
        table.add_column("Type")
        table.add_column("Value/Basename")
        if datas is not None:
            for data in datas:
                value = ""
                if ("value" in data.keys() and
                        data.get("value") is not None):
                    value = data.get("value")
                elif (
                        "basename" in data.keys() and
                        data.get("basename") is not None
                ):
                    value = data.get("basename")
                elif "url" in data.keys():
                    value = data.get("url")
                table.add_row(
                    data.get("name"),
                    data.get("param_type"),
                    str(value)
                )
        console.print(Padding(table, (0, 4)))

    @staticmethod
    def filter_artefacts(data, author=None):
        results = []
        for artefact in data:
            if author is None or artefact['author'] == author:
                results.append(artefact)
        return results

    @staticmethod
    def filter_dts(data, owner=None):
        results = []
        for dt in data:
            if owner is None or dt['owner'] == owner:
                results.append(dt)
        return results

    @staticmethod
    def date_matches(date_to_check: str, input_date: str) -> bool:
        try:
            date_to_check_dt = datetime.strptime(date_to_check, "%Y-%m-%d")

            if len(input_date) == 4:
                year = int(input_date)
                return date_to_check_dt.year == year

            elif len(input_date) == 7:
                year, month = map(int, input_date.split('-'))
                return (date_to_check_dt.year == year and
                        date_to_check_dt.month == month)

            elif len(input_date) == 10:
                date_input_dt = datetime.strptime(input_date, "%Y-%m-%d")
                return date_to_check_dt == date_input_dt

            else:
                return False

        except ValueError:
            return False

    @staticmethod
    def prepare_dt(dts):
        return [
            {
                'name': dt['name'],
                'short_description': dt.get(
                    'short_description',
                    'No short descritpion provided to see '
                    'description please use [deltatwin components get].'
                ),
                'publication_date': dt['publication_date'],
                'license': dt['license']['name'],
                'topics': dt['topics'],
                'owner': dt['owner'],
                'visibility': dt['visibility']
            } for dt in dts
        ]


class API:
    @staticmethod
    def log_to_api(api: str, username: str, password: str):
        myobj = {
            'username': username,
            'password': password

        }

        try:
            resp = requests.post(
                url=f"{api}/connect",
                json=myobj
            )
        except (ConnectionError, InvalidSchema):
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {api}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(resp)

        return json.loads(resp.text)

    @staticmethod
    def check_user_role(conf: str):

        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        url = f'{Utils.get_service(conf)}/check_user_role'

        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service "
                       f"{Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)
        return True

        if 500 > r.status_code >= 400:
            click.echo(f"{Utils.log_error} {json.loads(r.text)['error']}")
            sys.exit(ReturnCode.UNAUTHORIZED)

        return True

    @staticmethod
    def query_token(api: str, token: str, harbor_token: str):
        myobj = {
            'refresh_token': token
        }

        harbor_headers = {
            "refresh_token": harbor_token
        }

        try:
            resp = requests.post(
                url=f"{api}/refresh",
                json=myobj
            )

            harbor_resp = requests.post(
                url=f"{api}/harbor_refresh_token",
                json=harbor_headers
            )
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service "
                       f"{api}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(resp)
        Utils.check_status(harbor_resp)

        data = resp.json()
        data["harbor"] = harbor_resp.json()
        return data

    # Decorator to check if token still valid
    @staticmethod
    def check_token(func: Callable[[str, tuple, dict[str, Any]], Any]) \
            -> Callable[[str, tuple, dict[str, Any]], Any]:
        def check_token_decorator(conf, *args, **kwargs):
            conf = Utils.retrieve_conf(conf)
            try:
                config = Utils.read_config(conf, 'SERVICES')

                if 'token' in config:
                    token_creation_date = datetime.strptime(
                        config['token_created'],
                        '%Y-%m-%d %H:%M:%S'
                    )
                    now = datetime.now()

                    if (
                            (now - token_creation_date).total_seconds() >
                            float(config['expires_in'])
                    ):
                        API.refresh_token(conf)
                return func(conf, *args, **kwargs)
            except KeyError:
                click.echo(f"{Utils.log_error} No config find please use "
                           "deltatwin login before using this command.")
                sys.exit(ReturnCode.USAGE_ERROR)

        return check_token_decorator

    @staticmethod
    def refresh_token(conf: str):
        created = datetime.now()
        try:
            config = Utils.read_config(conf, 'SERVICES')

            # Check if refresh token in conf
            if 'refresh_token' in config:
                date = datetime.strptime(
                    config['token_created'], '%Y-%m-%d %H:%M:%S')
                now = datetime.now()

                # check if refresh token is still valid
                if (now - date).total_seconds() < float(
                        config['refresh_expires_in']):
                    data = API.query_token(config['api'],
                                           config['refresh_token'],
                                           config['harbor_refresh_token'])
                else:
                    data = API.log_to_api(
                        config['api'],
                        config['username'],
                        config['password'])
                    click.echo(
                        f'{Utils.log_info} Refresh token '
                        f'expired log again to the service')
            else:
                data = API.log_to_api(
                    config['api'],
                    config["username"],
                    config["password"]
                )

                click.echo(f"{Utils.log_info}"
                           f" Log to the service {config['api']}")

        except KeyError:
            click.echo(f"{Utils.log_error} No config find please use "
                       f"deltatwin login before using this command.")
            sys.exit(ReturnCode.USAGE_ERROR)

        created = created.strftime("%Y-%m-%d %H:%M:%S")
        config['token_created'] = created
        config['token'] = data['access_token']
        config['expires_in'] = data["expires_in"]
        config['refresh_expires_in'] = data["refresh_expires_in"]
        config['refresh_token'] = data["refresh_token"]

        # Register config harbor informations
        config['harbor_access_token'] = data['harbor']['harbor_access_token']
        config['harbor_refresh_token'] = data['harbor']['harbor_refresh_token']

        Utils.save_config(conf, 'SERVICES', config)

    @staticmethod
    def force_login(conf: str):
        created = datetime.now()

        config = Utils.read_config(conf, 'SERVICES')

        data = API.log_to_api(
            config['api'],
            config["username"],
            config["password"]
        )

        created = created.strftime("%Y-%m-%d %H:%M:%S")
        config['token_created'] = created
        config['token'] = data['access_token']
        config['expires_in'] = data["expires_in"]
        config['refresh_expires_in'] = data["refresh_expires_in"]
        config['refresh_token'] = data["refresh_token"]

        # Register config harbor informations
        config['harbor_access_token'] = data['harbor']['harbor_access_token']
        config['harbor_refresh_token'] = data['harbor']['harbor_refresh_token']

        Utils.save_config(conf, 'SERVICES', config)

    @staticmethod
    def get_harbor_url(path: str):
        conf = Utils.retrieve_conf(path)
        token = Utils.retrieve_token(conf)

        url = f'{Utils.get_service(conf)}/harbor_get_url'
        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service "
                       f"{Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()['harbor_url']

    @check_token
    @staticmethod
    def get_twin_id_by_run_id(conf: str, run_id: str):

        token = Utils.retrieve_token(conf)

        url = f'{Utils.get_service(conf)}/runs/{run_id}'

        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service "
                       f"{Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)
        Utils.check_status(r)

        return r.json()['dtwin_id']

    @check_token
    @staticmethod
    def create_artifact(conf, run_id, output_name, name, description,
                        visibility, tags):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        twin_id = API.get_twin_id_by_run_id(conf, run_id)

        url = (f'{Utils.get_service(conf)}/deltatwins/'
               f'{twin_id}/runs/{run_id}/{output_name}/artifact')
        try:
            r = requests.post(
                url,
                headers={'Authorization': f'Bearer {token}'},
                json={"name": name, "description": description,
                      'visibility': visibility,
                      "tags": str(tags)}  # TODO pass [] when api was ready.
            )
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service "
                       f"{Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

    @check_token
    @staticmethod
    def download_artifact(conf, artifact_id):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        url = (f'{Utils.get_service(conf)}/artifacts/{artifact_id}/download')
        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service "
                       f"{Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r

    @check_token
    @staticmethod
    def list_artifact(conf, visibility, dtwin_name):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)
        params = {}
        if visibility is not None:
            params["visibility"] = visibility

        if dtwin_name is not None:
            params["dtwin_name"] = dtwin_name

        url = f'{Utils.get_service(conf)}/artifacts'

        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'}, params=params)
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service "
                       f"{Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()

    @check_token
    @staticmethod
    def download_run(conf, run_id, output_name):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        twin_id = API.get_twin_id_by_run_id(conf, run_id)

        url = (f'{Utils.get_service(conf)}/deltatwins/'
               f'{twin_id}/runs/{run_id}/{output_name}/download')

        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r

    @check_token
    @staticmethod
    def get_run(conf, run_id):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)
        url = f'{Utils.get_service(conf)}/runs/{run_id}'

        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()

    @check_token
    @staticmethod
    def delete_run(conf, run_id):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)
        url = f'{Utils.get_service(conf)}/runs/{run_id}'

        try:
            r = requests.delete(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

    @check_token
    @staticmethod
    def list_runs(conf, twin_name, status, limit, offset):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        url = f'{Utils.get_service(conf)}/deltatwins/{twin_name}/runs'

        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'},
                params={"status": status,
                        "limit": limit, "offset": offset})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()

    @check_token
    @staticmethod
    def start_run(conf, twin_name, input_file, input_run, version):
        conf = Utils.retrieve_conf(conf)
        params = {}

        if version is not None:
            params["version"] = version

        token = Utils.retrieve_token(conf)
        inputs_json = []

        if input_run is not None and len(input_run) > 0:
            if input_file is not None:
                raise click.UsageError("the options inputs-file and inputs "
                                       "are mutually exclusive")
            for input_arg in input_run:
                inputs_json.append(
                    {'name': input_arg[0], 'value': input_arg[1]})
        if input_file is not None:
            file_inputs = open(input_file)
            inputs_json = json.load(file_inputs)

        url = f'{Utils.get_service(conf)}/deltatwins/{twin_name}/runs'
        try:
            r = requests.post(
                url,
                headers={'Authorization': f'Bearer {token}'}, json=inputs_json,
                params=params)
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()

    @check_token
    @staticmethod
    def start_scheduled_run(conf, twin_name, input_file,
                            input_run, type, schedule, name):
        conf = Utils.retrieve_conf(conf)
        token = Utils.retrieve_token(conf)
        inputs_json = []

        if input_run is not None and len(input_run) > 0:
            if input_file is not None:
                raise click.UsageError("the options inputs-file and inputs "
                                       "are mutually exclusive")
            for input_arg in input_run:
                inputs_json.append(
                    {'name': input_arg[0], 'value': input_arg[1]})
        if input_file is not None:
            file_inputs = open(input_file)
            inputs_json = json.load(file_inputs)

        url = f'{Utils.get_service(conf)}/deltatwins/{twin_name}/schedule'
        data = {
            "type": type,
            "schedule_name": name,
            "schedule": schedule,
            "inputs": inputs_json
        }
        try:
            r = requests.post(
                url,
                headers={'Authorization': f'Bearer {token}'}, json=data)
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()

    @check_token
    @staticmethod
    def list_scheduled_run(conf, twin_name, author):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)
        params = {}
        if author is not None:
            params['owner'] = author
        if twin_name is not None:
            params['deltatwin_name'] = twin_name

        url = f'{Utils.get_service(conf)}/schedules'

        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'}, params=params)
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()

    @check_token
    @staticmethod
    def delete_scheduled_run(conf, schedule_id):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        url = f'{Utils.get_service(conf)}/schedules/{schedule_id}'

        try:
            r = requests.delete(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

    @check_token
    @staticmethod
    def get_scheduled_run(conf, schedule_id):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        url = f'{Utils.get_service(conf)}/schedules/{schedule_id}'

        try:
            r = requests.get(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()

    @check_token
    @staticmethod
    def resume_scheduled_run(conf, schedule_id):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        url = f'{Utils.get_service(conf)}/schedules/{schedule_id}/resume'

        try:
            r = requests.put(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()

    @check_token
    @staticmethod
    def pause_scheduled_run(conf, schedule_id):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        url = f'{Utils.get_service(conf)}/schedules/{schedule_id}/pause'

        try:
            r = requests.put(
                url,
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

        return r.json()

    @check_token
    @staticmethod
    def delete_artifact(conf, artifact_id):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            r = requests.delete(
                f'{Utils.get_service(conf)}/artifacts/{artifact_id}',
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(r)

    @check_token
    @staticmethod
    def get_artifact(conf, artifact_id):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            r = requests.get(
                f'{Utils.get_service(conf)}/artifacts/{artifact_id}',
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)
        Utils.check_status(r)

        return r.json()

    @check_token
    @staticmethod
    def get_dt(conf, dt_name, param):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            dt_info_response = requests.get(
                f'{Utils.get_service(conf)}/deltatwins/{dt_name}',
                headers={'Authorization': f'Bearer {token}'},
                params=param)
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(dt_info_response)

        return dt_info_response.json()

    @check_token
    @staticmethod
    def delete_dt(conf, dt_name):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            dt_info_response = requests.delete(
                f'{Utils.get_service(conf)}/deltatwins/{dt_name}',
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(dt_info_response)
        click.echo(f"{Utils.log_info} DeltaTwin {dt_name} deleted")

    @check_token
    @staticmethod
    def delete_dt_version(conf, dt_name, version):
        try:
            version = parse(version)
        except InvalidVersion:
            click.echo(f'{Utils.log_error} Invalid version: {version}')
            sys.exit(ReturnCode.USAGE_ERROR)

        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            dt_info_response = requests.delete(
                f'{Utils.get_service(conf)}/deltatwins/'
                f'{dt_name}/versions/{version}',
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" at {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(dt_info_response)
        click.echo(f"{Utils.log_info} Deltatwin {dt_name}:{version} deleted")

    @check_token
    @staticmethod
    def get_dt_manifest(conf, dt_name):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            dt_info_response = requests.get(
                f'{Utils.get_service(conf)}/deltatwins/'
                f'{dt_name}/files/manifest',
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(dt_info_response)

        return dt_info_response.json()

    @check_token
    @staticmethod
    def publish_dt(conf, data):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            resp = requests.post(
                f'{Utils.get_service(conf)}/deltatwins',
                headers={'Authorization': f'Bearer {token}'},
                json=data
            )
        except (ConnectionError, InvalidSchema):
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(resp)

    @check_token
    @staticmethod
    def publish_version_dt(conf, dt_name, data):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            resp = requests.post(
                f'{Utils.get_service(conf)}/deltatwins/{dt_name}',
                headers={'Authorization': f'Bearer {token}'},
                json=data
            )
        except (ConnectionError, InvalidSchema):
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(resp)

    @check_token
    @staticmethod
    def publish_dt_file(conf, data, file_to_publish):
        """
        Cett fonction renvoie une requete HTTP POST vers delta-api.
        La requete permet d'associer des fichiers à des deltatwin components
        Args:
            conf: la configuration des accès aux différents services autour
            data: les données pour savoir quel fichier associer à quel cmponent
            file_to_publish: le chemin du fichier à associer

        Returns:
            Aucun retour, mais on affiche les logs des appels sous-jacents
        """
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            # convertie depuis Postman
            resp = requests.post(
                url=f'{Utils.get_service(conf)}/deltatwins/'
                    f'{data["deltaTwinName"]}/files',
                headers={
                    'Authorization': f'Bearer {token}',
                    **data
                },
                files=[
                    ('file', ('file', open(file_to_publish, 'rb'),
                              'application/octet-stream'))
                ])
        except (ConnectionError, InvalidSchema):
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(resp)

    @check_token
    @staticmethod
    def check_dt_exists(conf, dt_name: str, version: str = None) -> bool:
        conf = Utils.retrieve_conf(conf)
        params = {}
        token = Utils.retrieve_token(conf)

        if version is not None:
            params['version'] = version

        version_resp = requests.get(
            f'{Utils.get_service(conf)}/deltatwins/{dt_name}',
            params=params,
            headers={'Authorization': f'Bearer {token}'})

        return version_resp.status_code == 200

    @check_token
    @staticmethod
    def get_dt_version(conf, dt_name):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            version_resp = requests.get(
                f'{Utils.get_service(conf)}/deltatwins/{dt_name}/versions',
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(version_resp)

        return version_resp.json()

    @check_token
    @staticmethod
    def get_dts(conf, visibility):
        conf = Utils.retrieve_conf(conf)
        params = {}
        if visibility is not None:
            params['visibility'] = visibility
        token = Utils.retrieve_token(conf)

        try:
            dt = requests.get(
                f'{Utils.get_service(conf)}/deltatwins',
                headers={'Authorization': f'Bearer {token}'},
                params=params, stream=True)
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)

        Utils.check_status(dt)

        return dt.json()

    @check_token
    @staticmethod
    def retrieve_harbor_creds(conf) -> tuple[str, str]:
        conf = Utils.retrieve_conf(conf)
        token = Utils.retrieve_token(conf)
        access_token, _ = Utils.retrieve_harbor_token(path=conf)

        headers = {
            'Authorization': f'Bearer {token}',
            'Harbor-Auth': f'{access_token}'
        }

        try:
            credentials_resp = requests.get(
                f'{Utils.get_service(conf)}/harbor_credentials',
                headers=headers)
            Utils.check_status(credentials_resp)
            data = credentials_resp.json()

            return data["harbor_username"], data["harbor_secret"]
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)
        except Exception:
            click.echo("Error")
            sys.exit(ReturnCode.USAGE_ERROR)

    @check_token
    @staticmethod
    def create_project_harbor(conf,
                              project_name: str,
                              public: bool) -> tuple[str, str]:
        conf = Utils.retrieve_conf(conf)
        token = Utils.retrieve_token(conf)
        access_token, _ = Utils.retrieve_harbor_token(path=conf)

        headers = {
            'Authorization': f'Bearer {token}',
            'Harbor-Auth': f'{access_token}'
        }

        data = {
            "project_name": project_name,
            "public": public
        }
        create_project_resp = requests.post(
            f'{Utils.get_service(conf)}/harbor_create_project',
            headers=headers,
            data=json.dumps(data)
        )
        return create_project_resp.status_code

    @check_token
    @staticmethod
    def get_metric(conf):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            r = requests.get(
                f'{Utils.get_service(conf)}/metrics',
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)
        Utils.check_status(r)

        return r.json()

    @check_token
    @staticmethod
    def get_metric_history(conf):
        conf = Utils.retrieve_conf(conf)

        token = Utils.retrieve_token(conf)

        try:
            r = requests.get(
                f'{Utils.get_service(conf)}/metrics/history',
                headers={'Authorization': f'Bearer {token}'})
        except ConnectionError:
            click.echo(f"{Utils.log_error} Connection error to the service"
                       f" {Utils.get_service(conf)}")
            sys.exit(ReturnCode.SERVICE_NOT_FOUND)
        Utils.check_status(r)

        return r.json()


class ReturnCode:
    INPUT_ERROR = 1  # , "Input Error"
    UNAUTHORIZED = 2  # , "Unauthorized"
    SERVICE_ERROR = 3  # , "Service error"
    SERVICE_NOT_FOUND = 4  # , "Service not found"
    RESOURCE_NOT_FOUND = 5  # , "Resource not found"
    USAGE_ERROR = 6  # , "Usage Error"

    INVALID_RUN_INPUT = 7  # , "Invalid run input"
    REQUIRED_INPUT_MISSING = 8  # , "Required input missing"
