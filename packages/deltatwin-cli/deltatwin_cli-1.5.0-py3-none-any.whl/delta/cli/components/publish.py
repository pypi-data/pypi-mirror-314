import hashlib
import json
import os.path
import sys

import click
import docker
from delta.core import DeltaCore
from delta.manifest.manifest import check_manifest
from packaging.version import parse, InvalidVersion
from rich.live import Live
from rich.text import Text

import delta
from delta.cli.utils import API, Utils, ReturnCode


@click.command(
    'publish',
    short_help='Publish a DeltaTwin® component to the store')
@click.option(
    '--visibility',
    '-v',
    type=click.Choice(['public', 'private']),
    default='private',
    help='Set the visibility of the DeltaTwin®, by default is private.')
@click.option(
    '--topic',
    '-t',
    type=str,
    default=None,
    multiple=True,
    help='Define each topic of the DeltaTwin (multiple topics can be defined)')
@click.option(
    '--change-log',
    '-C',
    type=str,
    default='',
    help='Describe the change log of the DeltaTwin')
@click.option(
    '--conf',
    '-c',
    type=str,
    default=None,
    help='Path to the conf file')
@click.argument('version')
@click.help_option("--help", "-h")
def publish_dt(version,
               visibility,
               topic,
               change_log,
               conf):
    """Publish a new version of a DeltaTwin to the platform.

    \b
    NOTES:
    \b
    🛈 Access to this functionality is restricted. Please contact DestinE
    Platform Support.
    \b
    🛈 This command must be executed on the directory of the DeltaTwin

    \b
    MANDATORY ARGUMENT:
    VERSION: identifier of the published DeltaTwin.

    The canonical public version identifiers
    MUST comply with the following scheme:
    [N!]N(.N)*[{a|b|rc}N][.postN][.devN]
    """
    if API.check_user_role(conf):
        path_deltatwin = os.getcwd()
        try:
            manifest = delta.manifest.parser.parse('manifest.json')
        except FileNotFoundError:
            click.echo(f"{Utils.log_error} "
                       f"Check if the manifest.json file exists.")
            sys.exit(ReturnCode.USAGE_ERROR)
        deltatwin_name = manifest.name

        if not API.check_dt_exists(conf, deltatwin_name):
            data = prepare_publish(
                conf=conf,
                version=version,
                deltatwin_name=deltatwin_name,
                visibility=visibility,
                topic=topic,
                change_log=change_log,
                path_deltatwin=path_deltatwin
            )
            API.publish_dt(conf, data)
        else:
            # Try to retrieve visibility of DT
            # We use it when creating project for the registry
            param = {}
            deltatwin = API.get_dt(conf, manifest.name, param)
            visibility = deltatwin.get("visibility", None)
            if visibility is None:
                click.echo(f"Cannot retrieve visibility of {manifest.name}.")
                click.echo(f"Check if {manifest.name} exists.")
                sys.exit(ReturnCode.USAGE_ERROR)
            data = prepare_version(
                conf=conf,
                version=version,
                deltatwin_name=deltatwin_name,
                path_deltatwin=path_deltatwin,
                change_log=change_log,
                visibility=visibility
            )
            API.publish_version_dt(conf, deltatwin_name, data=data)
        click.echo(
            f'{Utils.log_info} The DeltaTwin '
            f'{deltatwin_name}-{version}, has been released.')
        # quand o arrive ici, ça implique que:
        # 1- le deltatwin est publié
        # 2- manifest.json et workflow.yml existent
        # bien dans le dossier deltatwin
        # publish manifest.json
        API.publish_dt_file(conf=conf,
                            data={
                                "Name": "manifest.json",
                                "deltaTwinName": deltatwin_name,
                                "deltaTwinVersion": version,
                                "Checksum": hashlib.md5(
                                    open('manifest.json',
                                         'rb').read()).hexdigest()
                            },
                            file_to_publish="manifest.json")
        # publish workflow.yml
        API.publish_dt_file(conf=conf,
                            data={
                                "Name": "workflow.yml",
                                "deltaTwinName": deltatwin_name,
                                "deltaTwinVersion": version,
                                "Checksum": hashlib.md5(
                                    open('workflow.yml',
                                         'rb').read()).hexdigest()
                            },
                            file_to_publish="workflow.yml")
        click.echo(
            f'{Utils.log_info} The DeltaTwin '
            f'{manifest.name}-{version}, workflow and manifest'
            f'have been successfully published.')


def prepare_publish(conf,
                    version,
                    deltatwin_name,
                    visibility,
                    topic,
                    change_log,
                    path_deltatwin) -> dict:
    topics = []
    for tag_name in topic:
        topics.append(tag_name)

    prepared_version = prepare_version(
        conf=conf,
        version=version,
        deltatwin_name=deltatwin_name,
        path_deltatwin=path_deltatwin,
        change_log=change_log,
        visibility=visibility,
    )

    return {
        "visibility": visibility,
        "topics": topics,
        **prepared_version
    }


def prepare_version(conf,
                    version,
                    deltatwin_name,
                    path_deltatwin,
                    change_log,
                    visibility) -> dict:
    try:
        version = parse(version)
    except InvalidVersion:
        click.echo(f'{Utils.log_error} Invalid version: {version}')
        sys.exit(ReturnCode.USAGE_ERROR)

    try:
        with open(os.path.join(
            path_deltatwin,
            'manifest.json'
        ), 'r') as manifest:
            manifest_data = json.load(manifest)
            if not check_manifest(manifest_data):
                click.echo(f"{Utils.log_error} Wrong manifest.json")
                sys.exit(ReturnCode.USAGE_ERROR)
    except FileNotFoundError:
        click.echo(f"{Utils.log_error} No manifest.json found")
        sys.exit(ReturnCode.USAGE_ERROR)

    if not os.path.exists(os.path.join(path_deltatwin, 'workflow.yml')):
        click.echo(f"{Utils.log_error} No workflow.yml found")
        sys.exit(ReturnCode.USAGE_ERROR)

    # Check Delta Twin exists with this version
    if API.check_dt_exists(
        conf=conf,
        dt_name=deltatwin_name,
        version=version
    ):
        click.echo(f"The DeltaTwin {deltatwin_name} "
                   f"with the version {version} already exists.")
        sys.exit(ReturnCode.USAGE_ERROR)

    prepare_publish_to_harbor(
        conf,
        version=str(version),
        public=True if visibility == "public" else False,
    )

    return {
        "version": str(version),
        "changelog": change_log,
        "manifest": manifest_data
    }


def _push_image_to_registry(image_name: str,
                            version: str,
                            docker_cli):
    try:
        resp = docker_cli.api.push(
            image_name,
            tag=version,
            stream=True,
            decode=True
        )

        docker_id = {}

        def get_lines(d: dict):
            lines = [f"{k} : {v}" for k, v in d.items()]
            texts = Text('\n'.join(lines))
            return texts

        with Live(get_lines(docker_id)) as live:
            for line in resp:
                if line.get('id') is not None:
                    docker_id[line['id']] = line['status']
                live.update(get_lines(docker_id))
    except Exception:
        click.echo(f"Something wrong when pushing {image_name}:{version}")
        sys.exit(ReturnCode.USAGE_ERROR)


def prepare_publish_to_harbor(conf,
                              version: str,
                              public: bool):
    username, secret = API.retrieve_harbor_creds(conf)
    registry = API.get_harbor_url(path=conf)
    if registry is None:
        click.echo("Something wrong when retrieving registry.")
        sys.exit(ReturnCode.USAGE_ERROR)

    manifest = delta.manifest.parser.parse('manifest.json')
    with DeltaCore() as core:
        core.drive_build(version=version,
                         registry=registry)
    image_name = None
    project_name = f"{manifest.name}"
    if project_name is None or not project_name:
        click.echo("Project name cannot be None or empty")
        click.echo("Set a name in your manifest")
        sys.exit(ReturnCode.USAGE_ERROR)

    docker_cli = docker.from_env()
    click.echo("Login to the registry...")
    try:
        docker_cli.login(username=username,
                         password=secret,
                         registry=registry)
    except Exception:
        click.echo("Error when trying to log in to the registry")
        sys.exit(ReturnCode.USAGE_ERROR)

    click.echo(f"Creating project {project_name}...")
    status = API.create_project_harbor(conf=conf,
                                       project_name=project_name,
                                       public=public)
    if status == 201:
        click.echo(f"Project {project_name} has been created")
    elif status == 409:
        click.echo(f"Project {project_name} already exists")
    else:
        click.echo(f"Something wrong when creating project {project_name}\n"
                   f"status=({status})")
        sys.exit(ReturnCode.USAGE_ERROR)

    for name, _ in manifest.models.items():
        if name is None:
            click.echo("Model name cannot be None")
            sys.exit(ReturnCode.USAGE_ERROR)
        image_name = f"{registry}/{project_name}/{name}"
        _push_image_to_registry(
            image_name=image_name,
            version=version,
            docker_cli=docker_cli
        )
        click.echo(f"{project_name}/{name} has been pushed.")
        docker_cli.images.remove(image=f"{image_name}:{version}", force=True)
    docker_cli.close()
