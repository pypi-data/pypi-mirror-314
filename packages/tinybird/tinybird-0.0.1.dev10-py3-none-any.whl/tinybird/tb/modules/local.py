import hashlib
import os
import time
from typing import Optional

import click
import requests

import docker
from tinybird.feedback_manager import FeedbackManager
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import (
    coro,
)
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.exceptions import CLIException

# TODO: Use the official Tinybird image once it's available 'tinybirdco/tinybird-local:latest'
TB_IMAGE_NAME = "registry.gitlab.com/tinybird/analytics/tinybird-local-jammy-3.11:latest"
TB_CONTAINER_NAME = "tinybird-local"
TB_LOCAL_PORT = int(os.getenv("TB_LOCAL_PORT", 80))
TB_LOCAL_HOST = f"http://localhost:{TB_LOCAL_PORT}"


def start_tinybird_local(
    docker_client,
):
    """Start the Tinybird container."""
    pull_show_prompt = False
    pull_required = False
    try:
        local_image = docker_client.images.get(TB_IMAGE_NAME)
        local_image_id = local_image.attrs["RepoDigests"][0].split("@")[1]
        remote_image = docker_client.images.get_registry_data(TB_IMAGE_NAME)
        pull_show_prompt = local_image_id != remote_image.id
    except Exception:
        pull_show_prompt = False
        pull_required = True

    if (
        pull_show_prompt
        and click.prompt(FeedbackManager.info(message="** New version detected, download? [y/N]")).lower() == "y"
    ):
        click.echo(FeedbackManager.info(message="** Downloading latest version of Tinybird local..."))
        pull_required = True

    if pull_required:
        docker_client.images.pull(TB_IMAGE_NAME, platform="linux/amd64")

    container = None
    containers = docker_client.containers.list(all=True, filters={"name": TB_CONTAINER_NAME})
    if containers:
        container = containers[0]

    if container and not pull_required:
        # Container `start` is idempotent. It's safe to call it even if the container is already running.
        container.start()
    else:
        if container:
            container.remove(force=True)

        container = docker_client.containers.run(
            TB_IMAGE_NAME,
            name=TB_CONTAINER_NAME,
            detach=True,
            ports={"80/tcp": TB_LOCAL_PORT},
            remove=False,
            platform="linux/amd64",
        )

    click.echo(FeedbackManager.info(message="** Waiting for Tinybird local to be ready..."))
    for attempt in range(10):
        try:
            run = container.exec_run("tb --no-version-warning sql 'SELECT 1 AS healthcheck' --format json").output
            # dont parse the json as docker sometimes returns warning messages
            # todo: rafa, make this rigth
            if b'"healthcheck": 1' in run:
                break
            raise RuntimeError("Unexpected response from Tinybird")
        except Exception:
            if attempt == 9:  # Last attempt
                raise CLIException("Tinybird local not ready yet. Please try again in a few seconds.")
            time.sleep(5)  # Wait 5 seconds before retrying

    click.echo(FeedbackManager.success(message="✓ All set!\n"))


def get_docker_client():
    """Check if Docker is installed and running."""
    try:
        client = docker.from_env()
        client.ping()
        return client
    except Exception:
        raise CLIException("Docker is not running or installed. Please ensure Docker is installed and running.")


def stop_tinybird_local(docker_client):
    """Stop the Tinybird container."""
    try:
        container = docker_client.containers.get(TB_CONTAINER_NAME)
        container.stop()
    except Exception:
        pass


def remove_tinybird_local(docker_client):
    """Remove the Tinybird container."""
    try:
        container = docker_client.containers.get(TB_CONTAINER_NAME)
        container.remove(force=True)
    except Exception:
        pass


async def get_tinybird_local_client(path: Optional[str] = None):
    """Get a Tinybird client connected to the local environment."""
    config = CLIConfig.get_project_config()
    try:
        # ruff: noqa: ASYNC210
        tokens = requests.get(f"{TB_LOCAL_HOST}/tokens").json()
    except Exception:
        raise CLIException("Tinybird local is not running. Please run `tb local start` first.")

    user_token = tokens["user_token"]
    token = tokens["workspace_admin_token"]
    # Create a new workspace if path is provided. This is used to isolate the build in a different workspace.
    if path:
        folder_hash = hashlib.sha256(path.encode()).hexdigest()
        user_client = config.get_client(host=TB_LOCAL_HOST, token=user_token)

        ws_name = f"Tinybird_Local_Build_{folder_hash}"

        user_workspaces = await user_client.user_workspaces()
        ws = next((ws for ws in user_workspaces["workspaces"] if ws["name"] == ws_name), None)
        if not ws:
            await user_client.create_workspace(ws_name, template=None)
            user_workspaces = await user_client.user_workspaces()
            ws = next((ws for ws in user_workspaces["workspaces"] if ws["name"] == ws_name), None)

        token = ws["token"]

    config.set_token(token)
    config.set_host(TB_LOCAL_HOST)
    config.set_user_token(user_token)
    config.persist_to_file()
    return config.get_client(host=TB_LOCAL_HOST, token=token)


@cli.group()
@click.pass_context
def local(ctx):
    """Local commands"""


@local.command()
@coro
async def stop() -> None:
    """Stop Tinybird local"""
    click.echo(FeedbackManager.info(message="Shutting down Tinybird local..."))
    docker_client = get_docker_client()
    stop_tinybird_local(docker_client)
    click.echo(FeedbackManager.success(message="Tinybird local stopped"))


@local.command()
@coro
async def remove() -> None:
    """Remove Tinybird local"""
    click.echo(FeedbackManager.info(message="Removing Tinybird local..."))
    docker_client = get_docker_client()
    remove_tinybird_local(docker_client)
    click.echo(FeedbackManager.success(message="Tinybird local removed"))


@local.command()
@coro
async def start() -> None:
    """Start Tinybird local"""
    click.echo(FeedbackManager.info(message="Starting Tinybird local..."))
    docker_client = get_docker_client()
    start_tinybird_local(docker_client)
    click.echo(FeedbackManager.success(message="Tinybird local started"))


@local.command()
@coro
async def restart() -> None:
    """Restart Tinybird local"""
    click.echo(FeedbackManager.info(message="Restarting Tinybird local..."))
    docker_client = get_docker_client()
    remove_tinybird_local(docker_client)
    start_tinybird_local(docker_client)
    click.echo(FeedbackManager.success(message="Tinybird local restarted"))
