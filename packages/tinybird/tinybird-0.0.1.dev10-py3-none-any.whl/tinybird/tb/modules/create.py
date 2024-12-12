import os
import subprocess
from os import getcwd
from pathlib import Path
from typing import Optional

import click
from click import Context

from tinybird.client import TinyB
from tinybird.feedback_manager import FeedbackManager
from tinybird.tb.modules.cicd import init_cicd
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import _generate_datafile, coro, generate_datafile
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.datafile.fixture import build_fixture_name, persist_fixture
from tinybird.tb.modules.exceptions import CLIException
from tinybird.tb.modules.llm import LLM
from tinybird.tb.modules.local import get_tinybird_local_client


@cli.command()
@click.option(
    "--data",
    type=click.Path(exists=True),
    default=None,
    help="Initial data to be used to create the project",
)
@click.option(
    "--prompt",
    type=str,
    default=None,
    help="Prompt to be used to create the project",
)
@click.option(
    "--folder",
    default=None,
    type=click.Path(exists=True, file_okay=False),
    help="Folder where datafiles will be placed",
)
@click.option("--rows", type=int, default=10, help="Number of events to send")
@click.pass_context
@coro
async def create(
    ctx: Context,
    data: Optional[str],
    prompt: Optional[str],
    folder: Optional[str],
    rows: int,
) -> None:
    """Initialize a new project."""
    folder = folder or getcwd()
    try:
        tb_client = await get_tinybird_local_client(os.path.abspath(folder))
        click.echo(FeedbackManager.gray(message="Creating new project structure..."))
        await project_create(tb_client, data, prompt, folder)
        click.echo(FeedbackManager.success(message="✓ Scaffolding completed!\n"))

        click.echo(FeedbackManager.gray(message="\nCreating CI/CD files for GitHub and GitLab..."))
        init_git(folder)
        await init_cicd(data_project_dir=os.path.relpath(folder))
        click.echo(FeedbackManager.success(message="✓ Done!\n"))

        click.echo(FeedbackManager.gray(message="Building fixtures..."))

        if data:
            ds_name = os.path.basename(data.split(".")[0])
            data_content = Path(data).read_text()
            datasource_path = Path(folder) / "datasources" / f"{ds_name}.datasource"
            fixture_name = build_fixture_name(datasource_path.absolute(), ds_name, datasource_path.read_text())
            click.echo(FeedbackManager.info(message=f"✓ /fixtures/{ds_name}"))
            persist_fixture(fixture_name, data_content)
        elif prompt:
            datasource_files = [f for f in os.listdir(Path(folder) / "datasources") if f.endswith(".datasource")]
            for datasource_file in datasource_files:
                datasource_path = Path(folder) / "datasources" / datasource_file
                llm_config = CLIConfig.get_llm_config()
                llm = LLM(key=llm_config["api_key"])
                datasource_name = datasource_path.stem
                datasource_content = datasource_path.read_text()
                has_json_path = "`json:" in datasource_content
                if has_json_path:
                    sql = await llm.generate_sql_sample_data(tb_client, datasource_name, datasource_content, rows)
                    result = await tb_client.query(f"{sql} FORMAT JSON")
                    data = result.get("data", [])
                    fixture_name = build_fixture_name(datasource_path.absolute(), datasource_name, datasource_content)
                    persist_fixture(fixture_name, data)
                    click.echo(FeedbackManager.info(message=f"✓ /fixtures/{datasource_name}"))

        click.echo(FeedbackManager.success(message="✓ Done!\n"))

        click.echo(FeedbackManager.success(message="✓ Tinybird local is ready!"))
    except Exception as e:
        click.echo(FeedbackManager.error(message=f"Error: {str(e)}"))


async def project_create(
    client: TinyB,
    data: Optional[str],
    prompt: Optional[str],
    folder: str,
):
    project_paths = ["datasources", "endpoints", "materializations", "copies", "sinks", "fixtures"]
    force = True
    for x in project_paths:
        try:
            f = Path(folder) / x
            f.mkdir()
        except FileExistsError:
            pass
        click.echo(FeedbackManager.info_path_created(path=x))

    if data:
        path = Path(folder) / data
        format = path.suffix.lstrip(".")
        try:
            await _generate_datafile(str(path), client, format=format, force=force)
        except Exception as e:
            click.echo(FeedbackManager.error(message=f"Ersssssror: {str(e)}"))
        name = data.split(".")[0]
        generate_pipe_file(
            f"{name}_endpoint",
            f"""
NODE endpoint
SQL >
    SELECT * from {name}
TYPE ENDPOINT
            """,
            folder,
        )
    elif prompt:
        try:
            llm_config = CLIConfig.get_llm_config()
            llm = LLM(key=llm_config["api_key"])
            result = await llm.create_project(prompt)
            for ds in result.datasources:
                content = ds.content.replace("```", "")
                generate_datafile(
                    content, filename=f"{ds.name}.datasource", data=None, _format="ndjson", force=force, folder=folder
                )

            for pipe in result.pipes:
                content = pipe.content.replace("```", "")
                generate_pipe_file(pipe.name, content, folder)
        except Exception as e:
            click.echo(FeedbackManager.error(message=f"Error: {str(e)}"))


def init_git(folder: str):
    try:
        path = Path(folder)
        gitignore_file = path / ".gitignore"
        git_folder = path / ".git"
        if not git_folder.exists():
            subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)

        if gitignore_file.exists():
            content = gitignore_file.read_text()
            if ".tinyb" not in content:
                gitignore_file.write_text(content + "\n.tinyb\n")
        else:
            gitignore_file.write_text(".tinyb\n")

        click.echo(FeedbackManager.info_file_created(file=".gitignore"))
    except Exception as e:
        raise CLIException(f"Error initializing Git: {e}")


def generate_pipe_file(name: str, content: str, folder: str):
    base = Path(folder) / "endpoints"
    if not base.exists():
        base = Path()
    f = base / (f"{name}.pipe")
    with open(f"{f}", "w") as file:
        file.write(content)
    click.echo(FeedbackManager.info_file_created(file=f.relative_to(folder)))
