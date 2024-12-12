import os
from pathlib import Path

import click

from tinybird.feedback_manager import FeedbackManager
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import CLIException, coro
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.datafile.fixture import build_fixture_name, persist_fixture
from tinybird.tb.modules.llm import LLM
from tinybird.tb.modules.local import get_tinybird_local_client


@cli.command()
@click.argument("datasource", type=str)
@click.option("--rows", type=int, default=10, help="Number of events to send")
@click.option("--context", type=str, default="", help="Extra context to use for data generation")
@click.option("--folder", type=str, default=".", help="Folder where datafiles will be placed")
@coro
async def mock(datasource: str, rows: int, context: str, folder: str) -> None:
    """Load sample data into a Data Source.

    Args:
        ctx: Click context object
        datasource_file: Path to the datasource file to load sample data into
    """

    try:
        datasource_path = Path(datasource)
        datasource_name = datasource
        if datasource_path.suffix == ".datasource":
            datasource_name = datasource_path.stem
        else:
            datasource_path = Path("datasources", f"{datasource}.datasource")

        datasource_path = Path(folder) / datasource_path

        click.echo(FeedbackManager.gray(message=f"Creating fixture for {datasource_name}..."))
        datasource_content = datasource_path.read_text()
        llm_config = CLIConfig.get_llm_config()
        llm = LLM(key=llm_config["api_key"])
        tb_client = await get_tinybird_local_client(os.path.abspath(folder))
        sql = await llm.generate_sql_sample_data(tb_client, datasource_content, row_count=rows, context=context)
        result = await tb_client.query(f"{sql} FORMAT JSON")
        data = result.get("data", [])[:rows]
        fixture_name = build_fixture_name(datasource_path.absolute(), datasource_name, datasource_content)
        persist_fixture(fixture_name, data)
        click.echo(FeedbackManager.success(message="✓ Done!"))

    except Exception as e:
        raise CLIException(FeedbackManager.error(message=str(e)))
