import re
from asyncio import Semaphore, gather
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiofiles
import click

from tinybird.client import AuthNoTokenException, TinyB
from tinybird.feedback_manager import FeedbackManager
from tinybird.tb.modules.datafile.common import get_name_version
from tinybird.tb.modules.datafile.format_datasource import format_datasource
from tinybird.tb.modules.datafile.format_pipe import format_pipe


async def folder_pull(
    client: TinyB,
    folder: str,
    auto: bool,
    match: Optional[str],
    force: bool,
    verbose: bool = True,
    progress_bar: bool = False,
    fmt: bool = False,
):
    pattern = re.compile(match) if match else None

    def _get_latest_versions(resources: List[str]):
        versions: Dict[str, Any] = {}

        for x in resources:
            t = get_name_version(x)
            t["original_name"] = x
            if t["version"] is None:
                t["version"] = -1
            name = t["name"]

            if name not in versions or name == x or versions[name]["version"] < t["version"]:
                versions[name] = t
        return versions

    def get_file_folder(extension: str):
        if not auto:
            return None
        if extension == "datasource":
            return "datasources"
        if extension == "pipe":
            return "pipes"
        if extension == "token":
            return "tokens"
        return None

    async def write_files(
        versions: Dict[str, Any],
        resources: List[str],
        extension: str,
        get_resource_function: str,
        progress_bar: bool = False,
        fmt: bool = False,
    ):
        async def write_resource(k: Dict[str, Any]):
            name = f"{k['name']}.{extension}"
            try:
                if pattern and not pattern.search(name):
                    if verbose:
                        click.echo(FeedbackManager.info_skipping_resource(resource=name))
                    return

                resource = await getattr(client, get_resource_function)(k["original_name"])
                resource_to_write = resource

                if fmt:
                    if extension == "datasource":
                        resource_to_write = await format_datasource(name, content=resource)
                    elif extension == "pipe":
                        resource_to_write = await format_pipe(name, content=resource)

                dest_folder = folder
                if "." in k["name"] and extension != "token":
                    dest_folder = Path(folder) / "vendor" / k["name"].split(".", 1)[0]
                    name = f"{k['name'].split('.', 1)[1]}.{extension}"

                file_folder = get_file_folder(extension)
                f = Path(dest_folder) / file_folder if file_folder is not None else Path(dest_folder)

                if not f.exists():
                    f.mkdir(parents=True)

                f = f / name
                resource_names = [x.split(".")[-1] for x in resources]

                if verbose:
                    click.echo(FeedbackManager.info_writing_resource(resource=f))
                if not f.exists() or force:
                    async with aiofiles.open(f, "w") as fd:
                        # versions are a client only thing so
                        # datafiles from the server do not contains information about versions
                        if k["version"] >= 0:
                            if fmt:
                                resource_to_write = "\n" + resource_to_write  # fmt strips the first line

                            resource_to_write = f"VERSION {k['version']}\n" + resource_to_write
                        if resource_to_write:
                            matches = re.findall(r"([^\s\.]*__v\d+)", resource_to_write)
                            for match in set(matches):
                                m = match.split("__v")[0]
                                if m in resources or m in resource_names:
                                    resource_to_write = resource_to_write.replace(match, m)
                            await fd.write(resource_to_write)
                else:
                    if verbose:
                        click.echo(FeedbackManager.info_skip_already_exists())
            except Exception as e:
                raise click.ClickException(FeedbackManager.error_exception(error=e))

        values = versions.values()

        if progress_bar:
            with click.progressbar(values, label=f"Pulling {extension}s") as values:  # type: ignore
                for k in values:
                    await write_resource(k)
        else:
            tasks = [write_resource(k) for k in values]
            await _gather_with_concurrency(5, *tasks)

    try:
        datasources = await client.datasources()
        remote_datasources = sorted([x["name"] for x in datasources])
        datasources_versions = _get_latest_versions(remote_datasources)

        pipes = await client.pipes()
        remote_pipes = sorted([x["name"] for x in pipes])
        pipes_versions = _get_latest_versions(remote_pipes)

        resources = list(datasources_versions.keys()) + list(pipes_versions.keys())

        await write_files(
            datasources_versions, resources, "datasource", "datasource_file", progress_bar=progress_bar, fmt=fmt
        )
        await write_files(pipes_versions, resources, "pipe", "pipe_file", progress_bar=progress_bar, fmt=fmt)

        return

    except AuthNoTokenException:
        raise
    except Exception as e:
        raise click.ClickException(FeedbackManager.error_pull(error=str(e)))


async def _gather_with_concurrency(n, *tasks):
    semaphore = Semaphore(n)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await gather(*(sem_task(task) for task in tasks))
