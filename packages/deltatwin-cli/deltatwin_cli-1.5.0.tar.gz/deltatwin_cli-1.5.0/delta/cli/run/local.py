import asyncio
import datetime as dt
import json
import logging
import os
import re
import uuid
import sys

import requests
import shutil

import click
import docker.errors
import yaml

from delta.cli.login import delta_login
from delta.cli.utils import API, ReturnCode, Utils
from delta.drive.delta_drive import DeltaDrive
from delta.manifest.parser import Manifest, parse
from delta.run.job.docker_service import DockerJobService
from delta.run.orchestrator import (
    DeltaOrchestrator, DataParameterModel, PrimitiveParameterModel,
    RunContextModel
)
from delta.run.storage_manager import DeltaLocalStorageManager


class LocalDependencyManager:
    def __init__(self, config: str):
        self._config = config
        self._logger = logging.getLogger('DependencyManager')
        self._dir = os.path.join(os.path.dirname(config), 'deltatwins')

    def __fetch_deltatwin_file(self, deltatwin_id, deltatwin_version, file):
        api = Utils.get_service(self._config)
        token = Utils.get_token(self._config)

        url = (
            f"{api}/deltatwins/{deltatwin_id}/files/"
            f"{file}?version={deltatwin_version}"
        )
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
            stream=True
        )
        if response.status_code != 200:
            self._logger.error(
                f"Failed to fetch deltatwin file `{file}`: "
                f"{deltatwin_id} - {deltatwin_version}"
            )
            raise RuntimeError(f"{response.text} ({response.status_code})")

        filename = re.findall(
            r'filename="?([^"]+)',
            response.headers['Content-Disposition']
        )[0]
        destination = os.path.join(self._dir, deltatwin_id, deltatwin_version)
        os.makedirs(destination, exist_ok=True)
        chunk_size = 4 * 1024
        with open(os.path.join(destination, filename), 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                f.write(chunk)

    def __fetch_deltatwin_files(self, deltatwin_id, deltatwin_version):
        destination = os.path.join(self._dir, deltatwin_id, deltatwin_version)
        os.makedirs(destination, exist_ok=True)
        try:
            self.__fetch_deltatwin_file(
                deltatwin_id=deltatwin_id,
                deltatwin_version=deltatwin_version,
                file='manifest'
            )
            self.__fetch_deltatwin_file(
                deltatwin_id=deltatwin_id,
                deltatwin_version=deltatwin_version,
                file='workflow'
            )
        except RuntimeError as ex:
            shutil.rmtree(destination)
            raise ex

    def __download_deltatwin(
            self,
            deltatwin_id: str,
            deltatwin_version: str,
            visited: set[tuple[str, str]] = None
    ) -> None:
        dt_dir = os.path.join(self._dir, deltatwin_id, deltatwin_version)
        if not self.has_deltatwin(deltatwin_id, deltatwin_version):
            self.__fetch_deltatwin_files(deltatwin_id, deltatwin_version)

        if visited is None:
            visited = set()

        visiting = (deltatwin_id, deltatwin_version)
        if visiting in visited:
            return
        visited.add(visiting)

        manifest = parse(os.path.join(dt_dir, 'manifest.json'))
        harbor_url = API.get_harbor_url(self._config)
        harbor_usr, harbor_pwd = API.retrieve_harbor_creds(self._config)
        docker_cli = docker.from_env()
        docker_cli.login(
            registry=harbor_url,
            username=harbor_usr,
            password=harbor_pwd
        )
        for label in manifest.models.keys():
            self._logger.info(
                'Fetching model %s of deltatwin(id: %s, version: %s)',
                label, deltatwin_id, deltatwin_version
            )
            repo = (
                f"{API.get_harbor_url(self._config)}/{deltatwin_id}/"
                f"{label}:{deltatwin_version}"
            )
            try:
                try:
                    docker_cli.images.get(repo)
                except (docker.errors.ImageNotFound, docker.errors.APIError):
                    docker_cli.images.pull(repo)
            except (docker.errors.ImageNotFound, docker.errors.APIError) as ex:
                self._logger.error(
                    "Failed to fetch model %s of deltatwin"
                    "(id: %s, version: %s)",
                    label, deltatwin_id, deltatwin_version
                )
                raise RuntimeError(
                    "Failed to fetch dependency:"
                    f"{deltatwin_id}:{deltatwin_version}"
                ) from ex

        for label, dep in manifest.dependencies.items():
            self._logger.info(
                'Fetching dependency: %s(id: %s, version: %s)',
                label, dep.id, dep.version)
            self.__download_deltatwin(dep.id, dep.version, visited)

    def has_deltatwin(
            self,
            deltatwin_id: str,
            deltatwin_version: str
    ) -> bool:
        return os.path.isdir(
            os.path.join(self._dir, deltatwin_id, deltatwin_version)
        )

    def fetch_dependencies(
            self,
            deltatwin_id: str,
            deltatwin_version: str
    ) -> None:
        self.__download_deltatwin(deltatwin_id, deltatwin_version)

    def get_deltatwin_manifest(
            self,
            deltatwin_id: str,
            deltatwin_version: str
    ) -> Manifest:
        dt_dir = os.path.join(self._dir, deltatwin_id, deltatwin_version)
        return parse(os.path.join(dt_dir, 'manifest.json'))

    def get_deltatwin_workflow(
            self,
            deltatwin_id: str,
            deltatwin_version: str
    ) -> dict:
        dt_dir = os.path.join(self._dir, deltatwin_id, deltatwin_version)
        with open(os.path.join(dt_dir, 'workflow.yml')) as f:
            return yaml.safe_load(f)


@click.help_option("--help", "-h")
@click.command(
    name="start_local",
    short_help="Launch DeltaTwin run locally",
    help="Launch DeltaTwin run locally",
)
@click.option(
    "--conf", "-c",
    default=None,
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    help='Path to the conf file'
)
@click.option(
    "--input-file", "-I",
    default=None,
    required=True,
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    help='Inputs of run in json format, example: /mypath/inputs.json '
         'the json is defined like [{"name": "angle", "value": "45"},'
         '{"name": "image", "value": "http/myimg/$value"}]'
)
@click.option(
    "--deltatwin-dir",
    default=os.getcwd(),
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    help="Directory of deltatwin to run (default: current working directory)"
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="If enabled keep Docker containers, instead of deleting them"
)
@click.pass_context
def run_local(
        ctx: click.Context,
        conf: str | None,
        input_file: str,
        debug: bool,
        deltatwin_dir: str
) -> None:
    click.echo(f"{Utils.log_info} Refresh authentication (login command)")
    ctx.invoke(delta_login)
    config = Utils.retrieve_conf(conf)
    harbor_url = API.get_harbor_url(config)

    click.echo(f"{Utils.log_info} Loading deltatwin ")
    try:
        manifest = parse(os.path.join(deltatwin_dir, "manifest.json"))
        with open(os.path.join(deltatwin_dir, 'workflow.yml'), 'r') as wf:
            workflow = yaml.safe_load(wf)
    except FileNotFoundError:
        click.echo(
            f"{Utils.log_error} Failed to find workflow.yml in directory "
            f"{deltatwin_dir}"
        )
        sys.exit(ReturnCode.USAGE_ERROR)

    click.echo(f"{Utils.log_info} Loading dependencies")
    delta_home = os.path.dirname(config)
    storage = DeltaLocalStorageManager(base_dir=delta_home)
    dependency_mng = LocalDependencyManager(config)
    for label, dependency in manifest.dependencies.items():
        try:
            dependency_mng.fetch_dependencies(
                dependency.id, dependency.version
            )
        except RuntimeError:
            click.echo(
                f"{Utils.log_error} Failed to fetch dependency: "
                f"{dependency.id} - {dependency.version}"
            )
            sys.exit(ReturnCode.SERVICE_ERROR)

    click.echo(f"{Utils.log_info} Building local model images")
    version = "dev"
    drive = DeltaDrive()
    drive.repo_directory = deltatwin_dir
    try:
        drive.docker_build(registry=harbor_url, version=version)
    except docker.errors.DockerException as ex:
        click.echo(ex)
        click.echo(f"{Utils.log_error} Failed to build image")
        sys.exit(ReturnCode.USAGE_ERROR)

    # convert inputs
    click.echo(f"{Utils.log_info} Loading inputs")
    try:
        if input_file in (None, ''):
            click.echo(f"{Utils.log_error} Could not find inputs "
                       f"in file {input_file}")
            sys.exit(ReturnCode.USAGE_ERROR)
        else:
            with open(input_file, "r") as f:
                data = json.load(f)
                inputs = [convert_input(p, manifest) for p in data]
    except json.decoder.JSONDecodeError as ex:
        click.echo(f"{Utils.log_error} Invalid `input-file` JSON data")
        click.echo(f"DEBUG: Invalid `input-file` JSON data: {ex}")
        sys.exit(ReturnCode.INVALID_RUN_INPUT)
    except RuntimeError as ex:
        click.echo(f"{Utils.log_error} Failed to convert given inputs: {ex}")
        sys.exit(ReturnCode.INVALID_RUN_INPUT)

    # start orchestration
    executor = DockerJobService(registry=harbor_url, keep_container=debug)
    owner = Utils.read_config(config, "SERVICES").get('username', "John Doe")
    result = asyncio.run(
        orchestrate_local(
            manifest=manifest,
            workflow=workflow,
            inputs=inputs,
            storage=storage,
            executor=executor,
            owner=owner,
        )
    )
    Utils.display_run_short(result.model_dump())


def convert_input(
        param: dict, manifest: Manifest
) -> PrimitiveParameterModel | DataParameterModel:
    if "name" not in param:
        raise RuntimeError("Parameter missing key: name")
    if "value" not in param:
        raise RuntimeError("Parameter missing key: value")

    name, value = param["name"], param["value"]
    try:
        input_manifest = manifest.inputs[name]
    except KeyError:
        raise RuntimeError(f"Unknown input: {name}")

    _type = input_manifest.type
    match input_manifest.type:
        case "boolean":
            return PrimitiveParameterModel(
                name=name,
                type=_type,
                value=True if value.lower() == "true" else False
            )
        case "integer":
            return PrimitiveParameterModel(
                name=name,
                type=_type,
                value=int(value)
            )
        case "float":
            return PrimitiveParameterModel(
                name=name,
                type=_type,
                value=float(value)
            )
        case "string":
            return PrimitiveParameterModel(
                name=name,
                type=_type,
                value=str(value)
            )
        case "Data":
            return DataParameterModel(name=name, type="Data", url=value)
        case _:
            raise RuntimeError(f"Unknown input type: {input_manifest.type}")


async def orchestrate_local(
        manifest: Manifest,
        workflow: dict,
        inputs: list[PrimitiveParameterModel | DataParameterModel],
        storage: DeltaLocalStorageManager,
        executor: DockerJobService,
        owner: str,
) -> None:
    ctx = RunContextModel(
        id=str(uuid.uuid4()),
        deltatwin_id=manifest.name,
        deltatwin_version="dev",
        owner=owner,
        date_created=dt.datetime.now(dt.timezone.utc),
        inputs=inputs
    )

    async with executor:
        try:
            orchestrator = DeltaOrchestrator(
                manifest, workflow, ctx, storage, executor
            )
            run_ctx = await orchestrator.run()
            return run_ctx
        finally:
            executor.shutdown()
