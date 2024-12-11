import datetime
import os
import os.path
import re
import sys
import urllib
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union

import click
from toposort import toposort

from tinybird.client import TinyB
from tinybird.feedback_manager import FeedbackManager
from tinybird.sql import parse_table_structure, schema_to_sql_columns
from tinybird.sql_template import get_used_tables_in_template, render_sql_template
from tinybird.tb.modules.common import get_ca_pem_content
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.datafile.build_common import update_tags_in_resource
from tinybird.tb.modules.datafile.build_datasource import is_datasource, new_ds
from tinybird.tb.modules.datafile.build_pipe import (
    get_target_materialized_data_source_name,
    is_endpoint,
    is_endpoint_with_no_dependencies,
    is_materialized,
    new_pipe,
)
from tinybird.tb.modules.datafile.common import (
    DEFAULT_CRON_PERIOD,
    INTERNAL_TABLES,
    ON_DEMAND,
    PREVIEW_CONNECTOR_SERVICES,
    TB_LOCAL_WORKSPACE_NAME,
    CopyModes,
    CopyParameters,
    DataFileExtensions,
    ExportReplacements,
    ImportReplacements,
    PipeNodeTypes,
    find_file_by_name,
    get_name_version,
    get_project_filenames,
    pp,
)
from tinybird.tb.modules.datafile.exceptions import AlreadyExistsException, IncludeFileNotFoundException
from tinybird.tb.modules.datafile.parse_datasource import parse_datasource
from tinybird.tb.modules.datafile.parse_pipe import parse_pipe


async def folder_build(
    tb_client: TinyB,
    filenames: Optional[List[str]] = None,
    folder: str = ".",
    ignore_sql_errors: bool = False,
    is_internal: bool = False,
    only_pipes: bool = False,
    is_vendor: bool = False,
    current_ws: Optional[Dict[str, Any]] = None,
    workspaces: Optional[List[Dict[str, Any]]] = None,
):
    if only_pipes:
        filenames = [f for f in filenames if f.endswith(".pipe")]

    config = CLIConfig.get_project_config()
    build = True
    dry_run = False
    force = True
    push_deps = True
    only_changes = True
    debug = False
    check = True
    populate = False
    populate_subset = None
    populate_condition = None
    tests_to_run = 0
    tests_failfast = True
    override_datasource = False
    tests_check_requests_from_branch = False
    skip_confirmation = True
    wait = False
    unlink_on_populate_error = False
    upload_fixtures = False
    only_response_times = False
    workspace_map: Dict[str, Any] = {}
    tests_sample_by_params = 1
    tests_ignore_order = False
    tests_validate_processed_bytes = False
    run_tests = False
    verbose = False
    as_standard = False
    raise_on_exists = False
    fork_downstream = True
    fork = False
    release_created = False
    auto_promote = False
    hide_folders = False
    tests_relative_change = 0.01
    tests_sample_by_params = 0
    tests_filter_by = None
    tests_failfast = False
    tests_ignore_order = False
    tests_validate_processed_bytes = False
    tests_check_requests_from_branch = False
    git_release = False
    workspace_lib_paths = []

    workspace_lib_paths = list(workspace_lib_paths)
    # include vendor libs without overriding user ones
    existing_workspaces = set(x[1] for x in workspace_lib_paths)
    vendor_path = Path("vendor")
    user_token = config.get_user_token()
    user_client = deepcopy(tb_client)

    if user_token:
        user_client.token = user_token

    vendor_workspaces = []
    user_workspaces = await user_client.user_workspaces()
    if vendor_path.exists() and not is_vendor:
        for x in vendor_path.iterdir():
            if x.is_dir() and x.name not in existing_workspaces:
                if user_token:
                    try:
                        ws_to_delete = next((ws for ws in user_workspaces["workspaces"] if ws["name"] == x.name), None)
                        if ws_to_delete:
                            await user_client.delete_workspace(ws_to_delete["id"], hard_delete_confirmation=x.name)
                    except Exception:
                        pass
                    vendor_ws = await user_client.create_workspace(x.name, template=None)
                    vendor_workspaces.append(vendor_ws)
                workspace_lib_paths.append((x.name, x))

    workspaces: List[Dict[str, Any]] = (await user_client.user_workspaces()).get("workspaces", [])
    local_ws = next((ws for ws in workspaces if ws["name"] == TB_LOCAL_WORKSPACE_NAME), {})
    current_ws: Dict[str, Any] = current_ws or local_ws
    for vendor_ws in [ws for ws in workspaces if ws["name"] in [ws["name"] for ws in vendor_workspaces]]:
        ws_client = deepcopy(tb_client)
        ws_client.token = vendor_ws["token"]
        shared_ws_path = Path(folder) / "vendor" / vendor_ws["name"]

        if shared_ws_path.exists() and not is_vendor:
            await folder_build(ws_client, folder=shared_ws_path.as_posix(), is_vendor=True, current_ws=vendor_ws)

    datasources: List[Dict[str, Any]] = await tb_client.datasources()
    pipes: List[Dict[str, Any]] = await tb_client.pipes(dependencies=True)

    existing_resources: List[str] = [x["name"] for x in datasources] + [x["name"] for x in pipes]
    # replace workspace mapping names
    for old_ws, new_ws in workspace_map.items():
        existing_resources = [re.sub(f"^{old_ws}\.", f"{new_ws}.", x) for x in existing_resources]

    remote_resource_names = [get_remote_resource_name_without_version(x) for x in existing_resources]

    # replace workspace mapping names
    for old_ws, new_ws in workspace_map.items():
        remote_resource_names = [re.sub(f"^{old_ws}\.", f"{new_ws}.", x) for x in remote_resource_names]

    if not filenames:
        filenames = get_project_filenames(folder)

    changed = None

    # build graph to get new versions for all the files involved in the query
    # dependencies need to be processed always to get the versions
    dependencies_graph = await build_graph(
        filenames,
        tb_client,
        dir_path=folder,
        process_dependencies=True,
        workspace_map=workspace_map,
        skip_connectors=True,
        workspace_lib_paths=workspace_lib_paths,
        current_ws=current_ws,
        changed=changed,
        only_changes=only_changes,
        fork_downstream=fork_downstream,
        is_internal=is_internal,
        build=build,
    )

    resource_versions = {}
    latest_datasource_versions = {}

    # If we have datasources using VERSION, let's try to get the latest version
    dependencies_graph = await build_graph(
        filenames,
        tb_client,
        dir_path=folder,
        resource_versions=latest_datasource_versions,
        workspace_map=workspace_map,
        process_dependencies=push_deps,
        verbose=verbose,
        workspace_lib_paths=workspace_lib_paths,
        current_ws=current_ws,
        changed=changed,
        only_changes=only_changes,
        fork_downstream=fork_downstream,
        is_internal=is_internal,
        build=build,
    )

    if debug:
        pp.pprint(dependencies_graph.to_run)

    def should_push_file(
        name: str,
        remote_resource_names: List[str],
        latest_datasource_versions: Dict[str, Any],
        force: bool,
        run_tests: bool,
    ) -> bool:
        """
        Function to know if we need to run a file or not
        """
        if name not in remote_resource_names:
            return True
        # When we need to try to push a file when it doesn't exist and the version is different that the existing one
        resource_full_name = (
            f"{name}__v{latest_datasource_versions.get(name)}" if name in latest_datasource_versions else name
        )
        if resource_full_name not in existing_resources:
            return True
        if force or run_tests:
            return True
        return False

    async def push(
        name: str,
        to_run: Dict[str, Dict[str, Any]],
        resource_versions: Dict[str, Any],
        latest_datasource_versions: Dict[str, Any],
        dry_run: bool,
        fork_downstream: Optional[bool] = False,
        fork: Optional[bool] = False,
    ):
        if name in to_run:
            resource = to_run[name]["resource"]
            if not dry_run:
                if should_push_file(name, remote_resource_names, latest_datasource_versions, force, run_tests):
                    if name not in resource_versions:
                        version = ""
                        if name in latest_datasource_versions:
                            version = f"(v{latest_datasource_versions[name]})"
                        click.echo(FeedbackManager.info_processing_new_resource(name=name, version=version))
                    else:
                        click.echo(
                            FeedbackManager.info_processing_resource(
                                name=name,
                                version=latest_datasource_versions[name],
                                latest_version=resource_versions.get(name),
                            )
                        )
                    try:
                        await exec_file(
                            to_run[name],
                            tb_client,
                            force,
                            check,
                            debug and verbose,
                            populate,
                            populate_subset,
                            populate_condition,
                            unlink_on_populate_error,
                            wait,
                            user_token,
                            override_datasource,
                            ignore_sql_errors,
                            skip_confirmation,
                            only_response_times,
                            run_tests,
                            as_standard,
                            tests_to_run,
                            tests_relative_change,
                            tests_sample_by_params,
                            tests_filter_by,
                            tests_failfast,
                            tests_ignore_order,
                            tests_validate_processed_bytes,
                            tests_check_requests_from_branch,
                            current_ws,
                            local_ws,
                            fork_downstream,
                            fork,
                            git_release,
                            build,
                            is_vendor,
                        )
                        if not run_tests:
                            click.echo(
                                FeedbackManager.success_create(
                                    name=(
                                        name
                                        if to_run[name]["version"] is None
                                        else f'{name}__v{to_run[name]["version"]}'
                                    )
                                )
                            )
                    except Exception as e:
                        filename = (
                            os.path.basename(to_run[name]["filename"]) if hide_folders else to_run[name]["filename"]
                        )
                        exception = FeedbackManager.error_push_file_exception(
                            filename=filename,
                            error=e,
                        )
                        raise click.ClickException(exception)
                else:
                    if raise_on_exists:
                        raise AlreadyExistsException(
                            FeedbackManager.warning_name_already_exists(
                                name=name if to_run[name]["version"] is None else f'{name}__v{to_run[name]["version"]}'
                            )
                        )
                    else:
                        if await name_matches_existing_resource(resource, name, tb_client):
                            if resource == "pipes":
                                click.echo(FeedbackManager.error_pipe_cannot_be_pushed(name=name))
                            else:
                                click.echo(FeedbackManager.error_datasource_cannot_be_pushed(name=name))
                        else:
                            click.echo(
                                FeedbackManager.warning_name_already_exists(
                                    name=(
                                        name
                                        if to_run[name]["version"] is None
                                        else f'{name}__v{to_run[name]["version"]}'
                                    )
                                )
                            )
            else:
                if should_push_file(name, remote_resource_names, latest_datasource_versions, force, run_tests):
                    if name not in resource_versions:
                        version = ""
                        if name in latest_datasource_versions:
                            version = f"(v{latest_datasource_versions[name]})"
                        if build:
                            extension = "pipe" if resource == "pipes" else "datasource"
                            click.echo(
                                FeedbackManager.info_building_resource(name=f"{name}.{extension}", version=version)
                            )
                        else:
                            click.echo(FeedbackManager.info_dry_processing_new_resource(name=name, version=version))
                    else:
                        click.echo(
                            FeedbackManager.info_dry_processing_resource(
                                name=name,
                                version=latest_datasource_versions[name],
                                latest_version=resource_versions.get(name),
                            )
                        )
                else:
                    if await name_matches_existing_resource(resource, name, tb_client):
                        if resource == "pipes":
                            click.echo(FeedbackManager.warning_pipe_cannot_be_pushed(name=name))
                        else:
                            click.echo(FeedbackManager.warning_datasource_cannot_be_pushed(name=name))
                    else:
                        click.echo(FeedbackManager.warning_dry_name_already_exists(name=name))

    async def push_files(
        dependency_graph: GraphDependencies,
        dry_run: bool = False,
        check_backfill_required: bool = False,
    ):
        endpoints_dep_map = dict()
        processed = set()

        dependencies_graph = dependency_graph.dep_map
        resources_to_run = dependency_graph.to_run

        if not fork_downstream:
            # First, we will deploy the all the resources following the dependency graph except for the endpoints
            groups = [group for group in toposort(dependencies_graph)]
            for group in groups:
                for name in group:
                    if name in processed:
                        continue

                    if is_endpoint_with_no_dependencies(
                        resources_to_run.get(name, {}),
                        dependencies_graph,
                        resources_to_run,
                    ):
                        endpoints_dep_map[name] = dependencies_graph[name]
                        continue

                    await push(
                        name,
                        resources_to_run,
                        resource_versions,
                        latest_datasource_versions,
                        dry_run,
                        fork_downstream,
                        fork,
                    )
                    processed.add(name)

            # Then, we will deploy the endpoints that are on the dependency graph
            groups = [group for group in toposort(endpoints_dep_map)]
            for group in groups:
                for name in group:
                    if name not in processed:
                        await push(
                            name,
                            resources_to_run,
                            resource_versions,
                            latest_datasource_versions,
                            dry_run,
                            fork_downstream,
                            fork,
                        )
                        processed.add(name)
        else:
            # This will generate the graph from right to left and will fill the gaps of the dependencies
            # If we have a graph like this:
            # A -> B -> C
            # If we only modify A, the normal dependencies graph will only contain a node like _{A => B}
            # But we need a graph that contains A, B and C and the dependencies between them to deploy them in the right order
            dependencies_graph_fork_downstream, resources_to_run_fork_downstream = generate_forkdownstream_graph(
                dependency_graph.all_dep_map,
                dependency_graph.all_resources,
                resources_to_run,
                list(dependency_graph.dep_map.keys()),
            )

            # First, we will deploy the datasources that need to be deployed.
            # We need to deploy the datasources from left to right as some datasources might have MV that depend on the column types of previous datasources. Ex: `test_change_column_type_landing_datasource` test
            groups = [group for group in toposort(dependencies_graph_fork_downstream)]

            for group in groups:
                for name in group:
                    try:
                        await tb_client.datasource_delete(name, force=True)
                    except Exception:
                        pass
                    try:
                        await tb_client.pipe_delete(name)
                    except Exception:
                        pass

            groups.reverse()
            for group in groups:
                for name in group:
                    if name in processed or not is_datasource(resources_to_run_fork_downstream[name]):
                        continue

                    # If the resource is new, we will use the normal resource information to deploy it
                    # This is mostly used for datasources with connections.
                    # At the moment, `resources_to_run_fork_downstream` is generated by `all_resources` and this is generated using the parameter `skip_connectors=True`
                    # TODO: Should the `resources_to_run_fork_downstream` be generated using the `skip_connectors` parameter?
                    if is_new(name, changed, dependencies_graph_fork_downstream, dependencies_graph_fork_downstream):
                        await push(
                            name,
                            resources_to_run,
                            resource_versions,
                            latest_datasource_versions,
                            dry_run,
                            fork_downstream,
                            fork,
                        )
                    else:
                        # If we are trying to modify a Kafka or CDK datasource, we need to inform the user that the resource needs to be post-released
                        kafka_connection_name = (
                            resources_to_run_fork_downstream[name].get("params", {}).get("kafka_connection_name")
                        )
                        service = resources_to_run_fork_downstream[name].get("params", {}).get("import_service")
                        if release_created and (kafka_connection_name or service):
                            connector = "Kafka" if kafka_connection_name else service
                            error_msg = FeedbackManager.error_connector_require_post_release(connector=connector)
                            raise click.ClickException(error_msg)

                        # If we are pushing a modified datasource, inform about the backfill``
                        if check_backfill_required and auto_promote and release_created:
                            error_msg = FeedbackManager.error_check_backfill_required(resource_name=name)
                            raise click.ClickException(error_msg)

                        await push(
                            name,
                            resources_to_run_fork_downstream,
                            resource_versions,
                            latest_datasource_versions,
                            dry_run,
                            fork_downstream,
                            fork,
                        )
                    processed.add(name)

            # Now, we will create a map of all the endpoints and there dependencies
            # We are using the forkdownstream graph to get the dependencies of the endpoints as the normal dependencies graph only contains the resources that are going to be deployed
            # But does not include the missing gaps
            # If we have ENDPOINT_A ----> MV_PIPE_B -----> DATASOURCE_B ------> ENDPOINT_C
            # Where endpoint A is being used in the MV_PIPE_B, if we only modify the endpoint A
            # The dependencies graph will only contain the endpoint A and the MV_PIPE_B, but not the DATASOURCE_B and the ENDPOINT_C
            groups = [group for group in toposort(dependencies_graph_fork_downstream)]
            for group in groups:
                for name in group:
                    if name in processed or not is_endpoint(resources_to_run_fork_downstream[name]):
                        continue

                    endpoints_dep_map[name] = dependencies_graph_fork_downstream[name]

            # Now that we have the dependencies of the endpoints, we need to check that the resources has not been deployed yet and only care about the endpoints that depend on endpoints
            groups = [group for group in toposort(endpoints_dep_map)]

            # As we have used the forkdownstream graph to get the dependencies of the endpoints, we have all the dependencies of the endpoints
            # But we need to deploy the endpoints and the dependencies of the endpoints from left to right
            # So we need to reverse the groups
            groups.reverse()
            for group in groups:
                for name in group:
                    if name in processed or not is_endpoint(resources_to_run_fork_downstream[name]):
                        continue

                    await push(
                        name,
                        resources_to_run_fork_downstream,
                        resource_versions,
                        latest_datasource_versions,
                        dry_run,
                        fork_downstream,
                        fork,
                    )
                    processed.add(name)

            # Now we should have the endpoints and datasources deployed, we can deploy the rest of the pipes (copy & sinks)
            # We need to rely on the forkdownstream graph as it contains all the modified pipes as well as the dependencies of the pipes
            # In this case, we don't need to generate a new graph as we did for the endpoints as the pipes are not going to be used as dependencies and the datasources are already deployed
            groups = [group for group in toposort(dependencies_graph_fork_downstream)]
            for group in groups:
                for name in group:
                    if name in processed or is_materialized(resources_to_run_fork_downstream.get(name)):
                        continue

                    await push(
                        name,
                        resources_to_run_fork_downstream,
                        resource_versions,
                        latest_datasource_versions,
                        dry_run,
                        fork_downstream,
                        fork,
                    )
                    processed.add(name)

            # Finally, we need to deploy the materialized views from right to left.
            # We need to rely on the forkdownstream graph as it contains all the modified materialized views as well as the dependencies of the materialized views
            # In this case, we don't need to generate a new graph as we did for the endpoints as the pipes are not going to be used as dependencies and the datasources are already deployed
            groups = [group for group in toposort(dependencies_graph_fork_downstream)]
            for group in groups:
                for name in group:
                    if name in processed or not is_materialized(resources_to_run_fork_downstream.get(name)):
                        continue

                    await push(
                        name,
                        resources_to_run_fork_downstream,
                        resource_versions,
                        latest_datasource_versions,
                        dry_run,
                        fork_downstream,
                        fork,
                    )
                    processed.add(name)

    await push_files(dependencies_graph, dry_run)

    if not dry_run and not run_tests:
        if upload_fixtures:
            click.echo(FeedbackManager.info_pushing_fixtures())

            processed = set()
            for group in toposort(dependencies_graph.dep_map):
                for f in group:
                    name = os.path.basename(f)
                    if name not in processed and name in dependencies_graph.to_run:
                        await check_fixtures_data(
                            tb_client,
                            dependencies_graph.to_run[name],
                            debug,
                            folder,
                            force,
                            mode="replace",
                        )
                        processed.add(name)
            for f in dependencies_graph.to_run:
                if f not in processed:
                    await check_fixtures_data(
                        tb_client,
                        dependencies_graph.to_run[f],
                        debug,
                        folder,
                        force,
                        mode="replace",
                    )
        else:
            if verbose:
                click.echo(FeedbackManager.info_not_pushing_fixtures())

    return dependencies_graph.to_run


async def check_fixtures_data(
    client: TinyB, resource: Dict[str, Any], debug: bool, folder: str = "", force: bool = False, mode: str = "replace"
):
    if debug:
        click.echo(FeedbackManager.info_checking_file(file=pp.pformat(resource)))
    if resource["resource"] in ["pipes", "tokens"]:
        pass
    elif resource["resource"] == "datasources":
        datasource_name = resource["params"]["name"]
        name = os.path.basename(resource["filename"]).rsplit(".", 1)[0]
        fixture_path = Path(folder) / "fixtures" / f"{name}.csv"

        if not fixture_path.exists():
            fixture_path = Path(folder) / "datasources" / "fixtures" / f"{name}.csv"
        if not fixture_path.exists():
            fixture_path = Path(folder) / "datasources" / "fixtures" / f"{name}.ndjson"
        if not fixture_path.exists():
            fixture_path = Path(folder) / "datasources" / "fixtures" / f"{name}.parquet"
        if fixture_path.exists():
            # Let's validate only when when we are going to replace the actual data
            result = await client.query(sql=f"SELECT count() as c FROM {datasource_name} FORMAT JSON")
            count = result["data"][0]["c"]

            if count > 0 and not force:
                raise click.ClickException(
                    FeedbackManager.error_push_fixture_will_replace_data(datasource=datasource_name)
                )

            click.echo(
                FeedbackManager.info_checking_file_size(
                    filename=resource["filename"], size=sizeof_fmt(os.stat(fixture_path).st_size)
                )
            )
            sys.stdout.flush()
            try:
                await client.datasource_append_data(
                    datasource_name=resource["params"]["name"],
                    file=fixture_path,
                    mode=mode,
                    format=fixture_path.suffix[1:],
                )
                click.echo(FeedbackManager.success_processing_data())
            except Exception as e:
                raise click.ClickException(FeedbackManager.error_processing_blocks(error=e))

        else:
            click.echo(FeedbackManager.warning_fixture_not_found(datasource_name=name))
    else:
        raise click.ClickException(FeedbackManager.error_unknown_resource(resource=resource["resource"]))


def is_new(
    name: str,
    changed: Dict[str, str],
    normal_dependency: Dict[str, Set[str]],
    fork_downstream_dependency: Dict[str, Set[str]],
) -> bool:
    def is_git_new(name: str):
        return changed and changed.get(name) == "A"

    if not is_git_new(name):
        return False

    # if should not depend on a changed resource
    if back_deps := normal_dependency.get(name):
        for dep in back_deps:
            if dep in fork_downstream_dependency and not is_git_new(dep):
                return False

    return True


async def name_matches_existing_resource(resource: str, name: str, tb_client: TinyB):
    if resource == "datasources":
        current_pipes: List[Dict[str, Any]] = await tb_client.pipes()
        if name in [x["name"] for x in current_pipes]:
            return True
    else:
        current_datasources: List[Dict[str, Any]] = await tb_client.datasources()
        if name in [x["name"] for x in current_datasources]:
            return True
    return False


async def exec_file(
    r: Dict[str, Any],
    tb_client: TinyB,
    force: bool,
    check: bool,
    debug: bool,
    populate: bool,
    populate_subset,
    populate_condition,
    unlink_on_populate_error,
    wait_populate,
    user_token: Optional[str],
    override_datasource: bool = False,
    ignore_sql_errors: bool = False,
    skip_confirmation: bool = False,
    only_response_times: bool = False,
    run_tests=False,
    as_standard=False,
    tests_to_run: int = 0,
    tests_relative_change: float = 0.01,
    tests_to_sample_by_params: int = 0,
    tests_filter_by: Optional[List[str]] = None,
    tests_failfast: bool = False,
    tests_ignore_order: bool = False,
    tests_validate_processed_bytes: bool = False,
    tests_check_requests_from_branch: bool = False,
    current_ws: Optional[Dict[str, Any]] = None,
    local_ws: Optional[Dict[str, Any]] = None,
    fork_downstream: Optional[bool] = False,
    fork: Optional[bool] = False,
    git_release: Optional[bool] = False,
    build: Optional[bool] = False,
    is_vendor: Optional[bool] = False,
):
    if debug:
        click.echo(FeedbackManager.debug_running_file(file=pp.pformat(r)))
    if r["resource"] == "pipes":
        await new_pipe(
            r,
            tb_client,
            force,
            check,
            populate,
            populate_subset,
            populate_condition,
            unlink_on_populate_error,
            wait_populate,
            ignore_sql_errors=ignore_sql_errors,
            only_response_times=only_response_times,
            run_tests=run_tests,
            as_standard=as_standard,
            tests_to_run=tests_to_run,
            tests_relative_change=tests_relative_change,
            tests_to_sample_by_params=tests_to_sample_by_params,
            tests_filter_by=tests_filter_by,
            tests_failfast=tests_failfast,
            tests_ignore_order=tests_ignore_order,
            tests_validate_processed_bytes=tests_validate_processed_bytes,
            override_datasource=override_datasource,
            tests_check_requests_from_branch=tests_check_requests_from_branch,
            fork_downstream=fork_downstream,
            fork=fork,
        )
        await update_tags_in_resource(r, "pipe", tb_client)
    elif r["resource"] == "datasources":
        await new_ds(
            r,
            tb_client,
            user_token,
            force,
            skip_confirmation=skip_confirmation,
            current_ws=current_ws,
            local_ws=local_ws,
            fork_downstream=fork_downstream,
            fork=fork,
            build=build,
            is_vendor=is_vendor,
        )
        await update_tags_in_resource(r, "datasource", tb_client)
    else:
        raise click.ClickException(FeedbackManager.error_unknown_resource(resource=r["resource"]))


def get_remote_resource_name_without_version(remote_resource_name: str) -> str:
    """
    >>> get_remote_resource_name_without_version("r__datasource")
    'r__datasource'
    >>> get_remote_resource_name_without_version("r__datasource__v0")
    'r__datasource'
    >>> get_remote_resource_name_without_version("datasource")
    'datasource'
    """
    parts = get_name_version(remote_resource_name)
    return parts["name"]


def create_downstream_dependency_graph(dependency_graph: Dict[str, Set[str]], all_resources: Dict[str, Dict[str, Any]]):
    """
    This function reverses the dependency graph obtained from build_graph so you have downstream dependencies for each node in the graph.

    Additionally takes into account target_datasource of materialized views
    """
    downstream_dependency_graph: Dict[str, Set[str]] = {node: set() for node in dependency_graph}

    for node, dependencies in dependency_graph.items():
        for dependency in dependencies:
            if dependency not in downstream_dependency_graph:
                # a shared data source, we can skip it
                continue
            downstream_dependency_graph[dependency].add(node)

    for key in dict(downstream_dependency_graph):
        target_datasource = get_target_materialized_data_source_name(all_resources[key])
        if target_datasource:
            downstream_dependency_graph[key].update({target_datasource})
            try:
                downstream_dependency_graph[target_datasource].remove(key)
            except KeyError:
                pass

    return downstream_dependency_graph


def update_dep_map_recursively(
    dep_map: Dict[str, Set[str]],
    downstream_dep_map: Dict[str, Set[str]],
    all_resources: Dict[str, Dict[str, Any]],
    to_run: Dict[str, Dict[str, Any]],
    dep_map_keys: List[str],
    key: Optional[str] = None,
    visited: Optional[List[str]] = None,
):
    """
    Given a downstream_dep_map obtained from create_downstream_dependency_graph this function updates each node recursively to complete the downstream dependency graph for each node
    """
    if not visited:
        visited = list()
    if not key and len(dep_map_keys) == 0:
        return
    if not key:
        key = dep_map_keys.pop()
    if key not in dep_map:
        dep_map[key] = set()
    else:
        visited.append(key)
        return

    for dep in downstream_dep_map.get(key, {}):
        if dep not in downstream_dep_map:
            continue
        to_run[dep] = all_resources.get(dep, {})
        update_dep_map_recursively(
            dep_map, downstream_dep_map, all_resources, to_run, dep_map_keys, key=dep, visited=visited
        )
        dep_map[key].update(downstream_dep_map[dep])
        dep_map[key].update({dep})
        try:
            dep_map[key].remove(key)
        except KeyError:
            pass

    to_run[key] = all_resources.get(key, {})
    update_dep_map_recursively(
        dep_map, downstream_dep_map, all_resources, to_run, dep_map_keys, key=None, visited=visited
    )


def generate_forkdownstream_graph(
    all_dep_map: Dict[str, Set[str]],
    all_resources: Dict[str, Dict[str, Any]],
    to_run: Dict[str, Dict[str, Any]],
    dep_map_keys: List[str],
) -> Tuple[Dict[str, Set[str]], Dict[str, Dict[str, Any]]]:
    """
    This function for a given graph of dependencies from left to right. It will generate a new graph with the dependencies from right to left, but taking into account that even if some nodes are not inside to_run, they are still dependencies that need to be deployed.

    >>> deps, _ = generate_forkdownstream_graph(
    ...     {
    ...         'a': {'b'},
    ...         'b': {'c'},
    ...         'c': set(),
    ...     },
    ...     {
    ...         'a': {'resource_name': 'a'},
    ...         'b': {'resource_name': 'b', 'nodes': [{'params': {'type': 'materialized', 'datasource': 'c'}}] },
    ...         'c': {'resource_name': 'c'},
    ...     },
    ...     {
    ...         'a': {'resource_name': 'a'},
    ...     },
    ...     ['a', 'b', 'c'],
    ... )
    >>> {k: sorted(v) for k, v in deps.items()}
    {'c': [], 'b': ['a', 'c'], 'a': []}

    >>> deps, _ = generate_forkdownstream_graph(
    ...     {
    ...         'a': {'b'},
    ...         'b': {'c'},
    ...         'c': set(),
    ...     },
    ...     {
    ...         'a': {'resource_name': 'a'},
    ...         'b': {'resource_name': 'b', 'nodes': [{'params': {'type': 'materialized', 'datasource': 'c'}}] },
    ...         'c': {'resource_name': 'c'},
    ...     },
    ...     {
    ...         'b': {'resource_name': 'b'},
    ...     },
    ...     ['a', 'b', 'c'],
    ... )
    >>> {k: sorted(v) for k, v in deps.items()}
    {'c': [], 'b': ['a', 'c'], 'a': []}

    >>> deps, _ = generate_forkdownstream_graph(
    ...     {
    ...         'migrated__a': {'a'},
    ...         'a': {'b'},
    ...         'b': {'c'},
    ...         'c': set(),
    ...     },
    ...     {
    ...         'migrated__a': {'resource_name': 'migrated__a', 'nodes': [{'params': {'type': 'materialized', 'datasource': 'a'}}]},
    ...         'a': {'resource_name': 'a'},
    ...         'b': {'resource_name': 'b', 'nodes': [{'params': {'type': 'materialized', 'datasource': 'c'}}] },
    ...         'c': {'resource_name': 'c'},
    ...     },
    ...     {
    ...         'migrated__a': {'resource_name': 'migrated__a'},
    ...         'a': {'resource_name': 'a'},
    ...     },
    ...     ['migrated_a', 'a', 'b', 'c'],
    ... )
    >>> {k: sorted(v) for k, v in deps.items()}
    {'c': [], 'b': ['a', 'c'], 'a': [], 'migrated_a': []}
    """
    downstream_dep_map = create_downstream_dependency_graph(all_dep_map, all_resources)
    new_dep_map: Dict[str, Set[str]] = {}
    new_to_run = deepcopy(to_run)
    update_dep_map_recursively(new_dep_map, downstream_dep_map, all_resources, new_to_run, dep_map_keys)
    return new_dep_map, new_to_run


@dataclass
class GraphDependencies:
    """
    This class is used to store the dependencies graph and the resources that are going to be deployed
    """

    dep_map: Dict[str, Set[str]]
    to_run: Dict[str, Dict[str, Any]]

    # The same as above but for the whole project, not just the resources affected by the current deployment
    all_dep_map: Dict[str, Set[str]]
    all_resources: Dict[str, Dict[str, Any]]


async def build_graph(
    filenames: Iterable[str],
    tb_client: TinyB,
    dir_path: Optional[str] = None,
    resource_versions=None,
    workspace_map: Optional[Dict] = None,
    process_dependencies: bool = False,
    verbose: bool = False,
    skip_connectors: bool = False,
    workspace_lib_paths: Optional[List[Tuple[str, str]]] = None,
    current_ws: Optional[Dict[str, Any]] = None,
    changed: Optional[Dict[str, Any]] = None,
    only_changes: bool = False,
    fork_downstream: Optional[bool] = False,
    is_internal: Optional[bool] = False,
    build: Optional[bool] = False,
) -> GraphDependencies:
    """
    This method will generate a dependency graph for the given files. It will also return a map of all the resources that are going to be deployed.
    By default it will generate the graph from left to right, but if fork-downstream, it will generate the graph from right to left.
    """
    to_run: Dict[str, Any] = {}
    deps: List[str] = []
    dep_map: Dict[str, Any] = {}
    embedded_datasources = {}
    if not workspace_map:
        workspace_map = {}

    # These dictionaries are used to store all the resources and there dependencies for the whole project
    # This is used for the downstream dependency graph
    all_dep_map: Dict[str, Set[str]] = {}
    all_resources: Dict[str, Dict[str, Any]] = {}

    if dir_path is None:
        dir_path = os.getcwd()

    # When using fork-downstream or --only-changes, we need to generate all the graph of all the resources and their dependencies
    # This way we can add more resources into the to_run dictionary if needed.
    if process_dependencies and only_changes:
        all_dependencies_graph = await build_graph(
            get_project_filenames(dir_path),
            tb_client,
            dir_path=dir_path,
            process_dependencies=True,
            resource_versions=resource_versions,
            workspace_map=workspace_map,
            skip_connectors=True,
            workspace_lib_paths=workspace_lib_paths,
            current_ws=current_ws,
            changed=None,
            only_changes=False,
            is_internal=is_internal,
            build=build,
        )
        all_dep_map = all_dependencies_graph.dep_map
        all_resources = all_dependencies_graph.to_run

    async def process(
        filename: str,
        deps: List[str],
        dep_map: Dict[str, Any],
        to_run: Dict[str, Any],
        workspace_lib_paths: Optional[List[Tuple[str, str]]],
    ):
        name, kind = filename.rsplit(".", 1)
        warnings = []

        try:
            res = await process_file(
                filename,
                tb_client,
                resource_versions=resource_versions,
                skip_connectors=skip_connectors,
                workspace_map=workspace_map,
                workspace_lib_paths=workspace_lib_paths,
                current_ws=current_ws,
            )
        except click.ClickException as e:
            raise e
        except IncludeFileNotFoundException as e:
            raise click.ClickException(FeedbackManager.error_deleted_include(include_file=str(e), filename=filename))
        except Exception as e:
            raise click.ClickException(str(e))

        for r in res:
            fn = r["resource_name"]
            warnings = r.get("warnings", [])
            if changed and fn in changed and (not changed[fn] or changed[fn] in ["shared", "remote"]):
                continue

            if (
                fork_downstream
                and r.get("resource", "") == "pipes"
                and any(["engine" in x.get("params", {}) for x in r.get("nodes", [])])
            ):
                raise click.ClickException(FeedbackManager.error_forkdownstream_pipes_with_engine(pipe=fn))

            to_run[fn] = r
            file_deps = r.get("deps", [])
            deps += file_deps
            # calculate and look for deps
            dep_list = []
            for x in file_deps:
                if x not in INTERNAL_TABLES or is_internal:
                    f, ds = find_file_by_name(dir_path, x, verbose, workspace_lib_paths=workspace_lib_paths, resource=r)
                    if f:
                        dep_list.append(f.rsplit(".", 1)[0])
                    if ds:
                        ds_fn = ds["resource_name"]
                        prev = to_run.get(ds_fn, {})
                        to_run[ds_fn] = deepcopy(r)
                        try:
                            to_run[ds_fn]["deps"] = list(
                                set(to_run[ds_fn].get("deps", []) + prev.get("deps", []) + [fn])
                            )
                        except ValueError:
                            pass
                        embedded_datasources[x] = to_run[ds_fn]
                    else:
                        e_ds = embedded_datasources.get(x, None)
                        if e_ds:
                            dep_list.append(e_ds["resource_name"])

            # In case the datasource is to be shared and we have mapping, let's replace the name
            if "shared_with" in r and workspace_map:
                mapped_workspaces: List[str] = []
                for shared_with in r["shared_with"]:
                    mapped_workspaces.append(
                        workspace_map.get(shared_with)
                        if workspace_map.get(shared_with, None) is not None
                        else shared_with  # type: ignore
                    )
                r["shared_with"] = mapped_workspaces

            dep_map[fn] = set(dep_list)
        return os.path.basename(name), warnings

    processed = set()

    async def get_processed(filenames: Iterable[str]):
        for filename in filenames:
            # just process changed filenames (tb deploy and --only-changes)
            if changed:
                resource = Path(filename).resolve().stem
                if resource in changed and (not changed[resource] or changed[resource] in ["shared", "remote"]):
                    continue
            if os.path.isdir(filename):
                await get_processed(filenames=get_project_filenames(filename))
            else:
                if verbose:
                    click.echo(FeedbackManager.info_processing_file(filename=filename))

                if ".incl" in filename:
                    click.echo(FeedbackManager.warning_skipping_include_file(file=filename))

                name, warnings = await process(filename, deps, dep_map, to_run, workspace_lib_paths)
                processed.add(name)

                if verbose:
                    if len(warnings) == 1:
                        click.echo(FeedbackManager.warning_pipe_restricted_param(word=warnings[0]))
                    elif len(warnings) > 1:
                        click.echo(
                            FeedbackManager.warning_pipe_restricted_params(
                                words=", ".join(["'{}'".format(param) for param in warnings[:-1]]),
                                last_word=warnings[-1],
                            )
                        )

    await get_processed(filenames=filenames)

    if process_dependencies:
        if only_changes:
            for key in dict(to_run):
                # look for deps that are the target data source of a materialized node
                target_datasource = get_target_materialized_data_source_name(to_run[key])
                if target_datasource:
                    # look in all_dep_map items that have as a dependency the target data source and are an endpoint
                    for _key, _deps in all_dep_map.items():
                        for dep in _deps:
                            if (
                                dep == target_datasource
                                or (dep == key and target_datasource not in all_dep_map.get(key, []))
                            ) and is_endpoint_with_no_dependencies(
                                all_resources.get(_key, {}), all_dep_map, all_resources
                            ):
                                dep_map[_key] = _deps
                                to_run[_key] = all_resources.get(_key)
        else:
            while len(deps) > 0:
                dep = deps.pop()
                if dep not in processed:
                    processed.add(dep)
                    f = full_path_by_name(dir_path, dep, workspace_lib_paths)
                    if f:
                        if verbose:
                            try:
                                processed_filename = f.relative_to(os.getcwd())
                            except ValueError:
                                processed_filename = f
                            # This is to avoid processing shared data sources
                            if "vendor/" in str(processed_filename):
                                click.echo(FeedbackManager.info_skipping_resource(resource=processed_filename))
                                continue
                            click.echo(FeedbackManager.info_processing_file(filename=processed_filename))
                        await process(str(f), deps, dep_map, to_run, workspace_lib_paths)

    return GraphDependencies(dep_map, to_run, all_dep_map, all_resources)


async def process_file(
    filename: str,
    tb_client: TinyB,
    resource_versions: Optional[Dict] = None,
    skip_connectors: bool = False,
    workspace_map: Optional[Dict] = None,
    workspace_lib_paths: Optional[List[Tuple[str, str]]] = None,
    current_ws: Optional[Dict[str, Any]] = None,
):
    if workspace_map is None:
        workspace_map = {}

    if resource_versions is None:
        resource_versions = {}
    resource_versions_string = {k: f"__v{v}" for k, v in resource_versions.items() if v >= 0}

    def get_engine_params(node: Dict[str, Any]) -> Dict[str, Any]:
        params = {}

        if "engine" in node:
            engine = node["engine"]["type"]
            params["engine"] = engine
            args = node["engine"]["args"]
            for k, v in args:
                params[f"engine_{k}"] = v
        return params

    async def get_kafka_params(node: Dict[str, Any]):
        params = {key: value for key, value in node.items() if key.startswith("kafka")}

        if not skip_connectors:
            try:
                connector_params = {
                    "kafka_bootstrap_servers": params.get("kafka_bootstrap_servers", None),
                    "kafka_key": params.get("kafka_key", None),
                    "kafka_secret": params.get("kafka_secret", None),
                    "kafka_connection_name": params.get("kafka_connection_name", None),
                    "kafka_auto_offset_reset": params.get("kafka_auto_offset_reset", None),
                    "kafka_schema_registry_url": params.get("kafka_schema_registry_url", None),
                    "kafka_ssl_ca_pem": get_ca_pem_content(params.get("kafka_ssl_ca_pem", None), filename),
                    "kafka_sasl_mechanism": params.get("kafka_sasl_mechanism", None),
                }

                connector = await tb_client.get_connection(**connector_params)
                if not connector:
                    click.echo(
                        FeedbackManager.info_creating_kafka_connection(connection_name=params["kafka_connection_name"])
                    )
                    required_params = [
                        connector_params["kafka_bootstrap_servers"],
                        connector_params["kafka_key"],
                        connector_params["kafka_secret"],
                    ]

                    if not all(required_params):
                        raise click.ClickException(FeedbackManager.error_unknown_kafka_connection(datasource=name))

                    connector = await tb_client.connection_create_kafka(**connector_params)
            except Exception as e:
                raise click.ClickException(
                    FeedbackManager.error_connection_create(
                        connection_name=params["kafka_connection_name"], error=str(e)
                    )
                )

            click.echo(FeedbackManager.success_connection_using(connection_name=connector["name"]))

            params.update(
                {
                    "connector": connector["id"],
                    "service": "kafka",
                }
            )

        return params

    async def get_import_params(datasource: Dict[str, Any], node: Dict[str, Any]) -> Dict[str, Any]:
        params: Dict[str, Any] = {key: value for key, value in node.items() if key.startswith("import_")}

        if len(params) == 0 or skip_connectors:
            return params

        service: Optional[str] = node.get("import_service", None)

        if service and service.lower() == "bigquery":
            if not await tb_client.check_gcp_read_permissions():
                raise click.ClickException(FeedbackManager.error_unknown_bq_connection(datasource=datasource["name"]))

            # Bigquery doesn't have a datalink, so we can stop here
            return params

        # Rest of connectors

        connector_id: Optional[str] = node.get("import_connector", None)
        connector_name: Optional[str] = node.get("import_connection_name", None)
        if not connector_name and not connector_id:
            raise click.ClickException(FeedbackManager.error_missing_connection_name(datasource=datasource["name"]))

        if not connector_id:
            assert isinstance(connector_name, str)

            connector: Optional[Dict[str, Any]] = await tb_client.get_connector(connector_name, service)

            if not connector:
                raise Exception(
                    FeedbackManager.error_unknown_connection(datasource=datasource["name"], connection=connector_name)
                )
            connector_id = connector["id"]
            service = connector["service"]

        # The API needs the connector ID to create the datasource.
        params["import_connector"] = connector_id
        if service:
            params["import_service"] = service

        if import_from_timestamp := params.get("import_from_timestamp", None):
            try:
                str(datetime.fromisoformat(import_from_timestamp).isoformat())
            except ValueError:
                raise click.ClickException(
                    FeedbackManager.error_invalid_import_from_timestamp(datasource=datasource["name"])
                )

        if service in PREVIEW_CONNECTOR_SERVICES:
            if not params.get("import_bucket_uri", None):
                raise click.ClickException(FeedbackManager.error_missing_bucket_uri(datasource=datasource["name"]))
        elif service == "dynamodb":
            if not params.get("import_table_arn", None):
                raise click.ClickException(FeedbackManager.error_missing_table_arn(datasource=datasource["name"]))
            if not params.get("import_export_bucket", None):
                raise click.ClickException(FeedbackManager.error_missing_export_bucket(datasource=datasource["name"]))
        else:
            if not params.get("import_external_datasource", None):
                raise click.ClickException(
                    FeedbackManager.error_missing_external_datasource(datasource=datasource["name"])
                )

        return params

    if DataFileExtensions.DATASOURCE in filename:
        doc = parse_datasource(filename)
        node = doc.nodes[0]
        deps: List[str] = []
        # reemplace tables on materialized columns
        columns = parse_table_structure(node["schema"])

        _format = "csv"
        for x in columns:
            if x["default_value"] and x["default_value"].lower().startswith("materialized"):
                # turn expression to a select query to sql_get_used_tables can get the used tables
                q = "select " + x["default_value"][len("materialized") :]
                tables = await tb_client.sql_get_used_tables(q)
                # materialized columns expressions could have joins so we need to add them as a dep
                deps += tables
                # generate replacements and replace the query
                replacements = {t: t + resource_versions_string.get(t, "") for t in tables}

                replaced_results = await tb_client.replace_tables(q, replacements)
                x["default_value"] = replaced_results.replace("SELECT", "materialized", 1)
            if x.get("jsonpath", None):
                _format = "ndjson"

        schema = ",".join(schema_to_sql_columns(columns))

        name = os.path.basename(filename).rsplit(".", 1)[0]

        if workspace_lib_paths:
            for wk_name, wk_path in workspace_lib_paths:
                try:
                    Path(filename).relative_to(wk_path)
                    name = f"{workspace_map.get(wk_name, wk_name)}.{name}"
                except ValueError:
                    # the path was not relative, not inside workspace
                    pass

        version = f"__v{doc.version}" if doc.version is not None else ""

        def append_version_to_name(name: str, version: str) -> str:
            if version != "":
                name = name.replace(".", "_")
                return name + version
            return name

        description = node.get("description", "")
        indexes_list = node.get("indexes", [])
        indexes = None
        if indexes_list:
            indexes = "\n".join([index.to_sql() for index in indexes_list])
        params = {
            "name": append_version_to_name(name, version),
            "description": description,
            "schema": schema,
            "indexes": indexes,
            "indexes_list": indexes_list,
            "format": _format,
        }

        params.update(get_engine_params(node))

        if "import_service" in node or "import_connection_name" in node:
            VALID_SERVICES: Tuple[str, ...] = ("bigquery", "snowflake", "s3", "s3_iamrole", "gcs", "dynamodb")

            import_params = await get_import_params(params, node)

            service = import_params.get("import_service", None)
            if service and service not in VALID_SERVICES:
                raise Exception(f"Unknown import service: {service}")

            if service in PREVIEW_CONNECTOR_SERVICES:
                ON_DEMAND_CRON = ON_DEMAND
                AUTO_CRON = "@auto"
                ON_DEMAND_CRON_EXPECTED_BY_THE_API = "@once"
                VALID_CRONS: Tuple[str, ...] = (ON_DEMAND_CRON, AUTO_CRON)
                cron = node.get("import_schedule", ON_DEMAND_CRON)

                if cron not in VALID_CRONS:
                    valid_values = ", ".join(VALID_CRONS)
                    raise Exception(f"Invalid import schedule: '{cron}'. Valid values are: {valid_values}")

                if cron == ON_DEMAND_CRON:
                    import_params["import_schedule"] = ON_DEMAND_CRON_EXPECTED_BY_THE_API
                if cron == AUTO_CRON:
                    period: int = DEFAULT_CRON_PERIOD

                    if current_ws:
                        workspaces = (await tb_client.user_workspaces()).get("workspaces", [])
                        workspace_rate_limits: Dict[str, Dict[str, int]] = next(
                            (w.get("rate_limits", {}) for w in workspaces if w["id"] == current_ws["id"]), {}
                        )
                        period = workspace_rate_limits.get("api_datasources_create_append_replace", {}).get(
                            "period", DEFAULT_CRON_PERIOD
                        )

                    def seconds_to_cron_expression(seconds: int) -> str:
                        minutes = seconds // 60
                        hours = minutes // 60
                        days = hours // 24
                        if days > 0:
                            return f"0 0 */{days} * *"
                        if hours > 0:
                            return f"0 */{hours} * * *"
                        if minutes > 0:
                            return f"*/{minutes} * * * *"
                        return f"*/{seconds} * * * *"

                    import_params["import_schedule"] = seconds_to_cron_expression(period)

            # Include all import_ parameters in the datasource params
            params.update(import_params)

            # Substitute the import parameters with the ones used by the
            # import API:
            # - If an import parameter is not present and there's a default
            #   value, use the default value.
            # - If the resulting value is None, do not add the parameter.
            #
            # Note: any unknown import_ parameter is leaved as is.
            for key in ImportReplacements.get_datafile_parameter_keys():
                replacement, default_value = ImportReplacements.get_api_param_for_datafile_param(service, key)
                if not replacement:
                    continue  # We should not reach this never, but just in case...

                value: Any
                try:
                    value = params[key]
                    del params[key]
                except KeyError:
                    value = default_value

                if value:
                    params[replacement] = value

        if "kafka_connection_name" in node:
            kafka_params = await get_kafka_params(node)
            params.update(kafka_params)
            del params["format"]

        if "tags" in node:
            tags = {k: v[0] for k, v in urllib.parse.parse_qs(node["tags"]).items()}
            params.update(tags)

        resources: List[Dict[str, Any]] = []

        resources.append(
            {
                "resource": "datasources",
                "resource_name": name,
                "version": doc.version,
                "params": params,
                "filename": filename,
                "deps": deps,
                "tokens": doc.tokens,
                "shared_with": doc.shared_with,
                "filtering_tags": doc.filtering_tags,
            }
        )

        return resources

    elif DataFileExtensions.PIPE in filename:
        doc = parse_pipe(filename)
        version = f"__v{doc.version}" if doc.version is not None else ""
        name = os.path.basename(filename).split(".")[0]
        description = doc.description if doc.description is not None else ""

        deps = []
        nodes: List[Dict[str, Any]] = []

        is_copy = any([node for node in doc.nodes if node.get("type", "standard").lower() == PipeNodeTypes.COPY])
        for node in doc.nodes:
            sql = node["sql"]
            node_type = node.get("type", "standard").lower()
            params = {
                "name": node["name"],
                "type": node_type,
                "description": node.get("description", ""),
                "target_datasource": node.get("target_datasource", None),
                "copy_schedule": node.get(CopyParameters.COPY_SCHEDULE, None),
                "mode": node.get("mode", CopyModes.APPEND),
            }

            is_export_node = ExportReplacements.is_export_node(node)
            export_params = ExportReplacements.get_params_from_datafile(node) if is_export_node else None

            sql = sql.strip()
            is_template = False
            if sql[0] == "%":
                try:
                    sql_rendered, _, _ = render_sql_template(sql[1:], test_mode=True)
                except Exception as e:
                    raise click.ClickException(
                        FeedbackManager.error_parsing_node(node=node["name"], pipe=name, error=str(e))
                    )
                is_template = True
            else:
                sql_rendered = sql

            try:
                dependencies = await tb_client.sql_get_used_tables(sql_rendered, raising=True, is_copy=is_copy)
                deps += [t for t in dependencies if t not in [n["name"] for n in doc.nodes]]

            except Exception as e:
                raise click.ClickException(
                    FeedbackManager.error_parsing_node(node=node["name"], pipe=name, error=str(e))
                )

            if is_template:
                deps += get_used_tables_in_template(sql[1:])

            is_neither_copy_nor_materialized = "datasource" not in node and "target_datasource" not in node
            if "engine" in node and is_neither_copy_nor_materialized:
                raise ValueError("Defining ENGINE options in a node requires a DATASOURCE")

            if "datasource" in node:
                params["datasource"] = node["datasource"] + resource_versions_string.get(node["datasource"], "")
                deps += [node["datasource"]]

            if "target_datasource" in node:
                params["target_datasource"] = node["target_datasource"] + resource_versions_string.get(
                    node["target_datasource"], ""
                )
                deps += [node["target_datasource"]]

            params.update(get_engine_params(node))

            def create_replacement_for_resource(name: str) -> str:
                for old_ws, new_ws in workspace_map.items():
                    name = name.replace(f"{old_ws}.", f"{new_ws}.")
                return name + resource_versions_string.get(name, "")

            replacements = {
                x: create_replacement_for_resource(x) for x in deps if x not in [n["name"] for n in doc.nodes]
            }

            # FIXME: Ideally we should use await tb_client.replace_tables(sql, replacements)
            for old, new in replacements.items():
                sql = re.sub("([\t \\n']+|^)" + old + "([\t \\n'\\)]+|$)", "\\1" + new + "\\2", sql)

            if "tags" in node:
                tags = {k: v[0] for k, v in urllib.parse.parse_qs(node["tags"]).items()}
                params.update(tags)

            nodes.append(
                {
                    "sql": sql,
                    "params": params,
                    "export_params": export_params,
                }
            )

        return [
            {
                "resource": "pipes",
                "resource_name": name,
                "version": doc.version,
                "filename": filename,
                "name": name + version,
                "nodes": nodes,
                "deps": [x for x in set(deps)],
                "tokens": doc.tokens,
                "description": description,
                "warnings": doc.warnings,
                "filtering_tags": doc.filtering_tags,
            }
        ]
    else:
        raise click.ClickException(FeedbackManager.error_file_extension(filename=filename))


def sizeof_fmt(num: Union[int, float], suffix: str = "b") -> str:
    """Readable file size
    :param num: Bytes value
    :type num: int
    :param suffix: Unit suffix (optionnal) default = o
    :type suffix: str
    :rtype: str
    """
    for unit in ["", "k", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)


def full_path_by_name(
    folder: str, name: str, workspace_lib_paths: Optional[List[Tuple[str, str]]] = None
) -> Optional[Path]:
    f = Path(folder)
    ds = name + ".datasource"
    if os.path.isfile(os.path.join(folder, ds)):
        return f / ds
    if os.path.isfile(f / "datasources" / ds):
        return f / "datasources" / ds

    pipe = name + ".pipe"
    if os.path.isfile(os.path.join(folder, pipe)):
        return f / pipe

    if os.path.isfile(f / "endpoints" / pipe):
        return f / "endpoints" / pipe

    if os.path.isfile(f / "pipes" / pipe):
        return f / "pipes" / pipe

    if os.path.isfile(f / "sinks" / pipe):
        return f / "sinks" / pipe

    if os.path.isfile(f / "copies" / pipe):
        return f / "copies" / pipe

    if os.path.isfile(f / "playgrounds" / pipe):
        return f / "playgrounds" / pipe

    if os.path.isfile(f / "materializations" / pipe):
        return f / "materializations" / pipe

    if workspace_lib_paths:
        for wk_name, wk_path in workspace_lib_paths:
            if name.startswith(f"{wk_name}."):
                r = full_path_by_name(wk_path, name.replace(f"{wk_name}.", ""))
                if r:
                    return r
    return None


async def folder_push(
    tb_client: TinyB,
    filenames: Optional[List[str]] = None,
    dry_run: bool = False,
    check: bool = False,
    push_deps: bool = False,
    only_changes: bool = False,
    git_release: bool = False,
    debug: bool = False,
    force: bool = False,
    override_datasource: bool = False,
    folder: str = ".",
    populate: bool = False,
    populate_subset=None,
    populate_condition: Optional[str] = None,
    unlink_on_populate_error: bool = False,
    upload_fixtures: bool = False,
    wait: bool = False,
    ignore_sql_errors: bool = False,
    skip_confirmation: bool = False,
    only_response_times: bool = False,
    workspace_map=None,
    workspace_lib_paths=None,
    no_versions: bool = False,
    run_tests: bool = False,
    as_standard: bool = False,
    raise_on_exists: bool = False,
    verbose: bool = True,
    tests_to_run: int = 0,
    tests_relative_change: float = 0.01,
    tests_sample_by_params: int = 0,
    tests_filter_by: Optional[List[str]] = None,
    tests_failfast: bool = False,
    tests_ignore_order: bool = False,
    tests_validate_processed_bytes: bool = False,
    tests_check_requests_from_branch: bool = False,
    config: Optional[CLIConfig] = None,
    user_token: Optional[str] = None,
    fork_downstream: Optional[bool] = False,
    fork: Optional[bool] = False,
    is_internal: Optional[bool] = False,
    release_created: Optional[bool] = False,
    auto_promote: Optional[bool] = False,
    check_backfill_required: bool = False,
    use_main: bool = False,
    check_outdated: bool = True,
    hide_folders: bool = False,
):
    workspaces: List[Dict[str, Any]] = (await tb_client.user_workspaces_and_branches()).get("workspaces", [])
    current_ws: Dict[str, Any] = next(
        (workspace for workspace in workspaces if config and workspace.get("id", ".") == config.get("id", "..")), {}
    )
    is_branch = current_ws.get("is_branch", False)

    if not workspace_map:
        workspace_map = {}
    if not workspace_lib_paths:
        workspace_lib_paths = []

    workspace_lib_paths = list(workspace_lib_paths)
    # include vendor libs without overriding user ones
    existing_workspaces = set(x[1] for x in workspace_lib_paths)
    vendor_path = Path("vendor")
    if vendor_path.exists():
        for x in vendor_path.iterdir():
            if x.is_dir() and x.name not in existing_workspaces:
                workspace_lib_paths.append((x.name, x))

    datasources: List[Dict[str, Any]] = await tb_client.datasources()
    pipes: List[Dict[str, Any]] = await tb_client.pipes(dependencies=True)

    existing_resources: List[str] = [x["name"] for x in datasources] + [x["name"] for x in pipes]
    # replace workspace mapping names
    for old_ws, new_ws in workspace_map.items():
        existing_resources = [re.sub(f"^{old_ws}\.", f"{new_ws}.", x) for x in existing_resources]

    remote_resource_names = [get_remote_resource_name_without_version(x) for x in existing_resources]

    # replace workspace mapping names
    for old_ws, new_ws in workspace_map.items():
        remote_resource_names = [re.sub(f"^{old_ws}\.", f"{new_ws}.", x) for x in remote_resource_names]

    if not filenames:
        filenames = get_project_filenames(folder)

    # build graph to get new versions for all the files involved in the query
    # dependencies need to be processed always to get the versions
    dependencies_graph = await build_graph(
        filenames,
        tb_client,
        dir_path=folder,
        process_dependencies=True,
        workspace_map=workspace_map,
        skip_connectors=True,
        workspace_lib_paths=workspace_lib_paths,
        current_ws=current_ws,
        changed=None,
        only_changes=only_changes,
        fork_downstream=fork_downstream,
        is_internal=is_internal,
    )

    resource_versions = {}
    latest_datasource_versions = {}
    changed = None
    # If we have datasources using VERSION, let's try to get the latest version
    dependencies_graph = await build_graph(
        filenames,
        tb_client,
        dir_path=folder,
        resource_versions=latest_datasource_versions,
        workspace_map=workspace_map,
        process_dependencies=push_deps,
        verbose=verbose,
        workspace_lib_paths=workspace_lib_paths,
        current_ws=current_ws,
        changed=None,
        only_changes=only_changes,
        fork_downstream=fork_downstream,
        is_internal=is_internal,
    )

    if debug:
        pp.pprint(dependencies_graph.to_run)

    if verbose:
        click.echo(FeedbackManager.info_building_dependencies())

    def should_push_file(
        name: str,
        remote_resource_names: List[str],
        latest_datasource_versions: Dict[str, Any],
        force: bool,
        run_tests: bool,
    ) -> bool:
        """
        Function to know if we need to run a file or not
        """
        if name not in remote_resource_names:
            return True
        # When we need to try to push a file when it doesn't exist and the version is different that the existing one
        resource_full_name = (
            f"{name}__v{latest_datasource_versions.get(name)}" if name in latest_datasource_versions else name
        )
        if resource_full_name not in existing_resources:
            return True
        if force or run_tests:
            return True
        return False

    async def push(
        name: str,
        to_run: Dict[str, Dict[str, Any]],
        resource_versions: Dict[str, Any],
        latest_datasource_versions: Dict[str, Any],
        dry_run: bool,
        fork_downstream: Optional[bool] = False,
        fork: Optional[bool] = False,
    ):
        if name in to_run:
            resource = to_run[name]["resource"]
            if not dry_run:
                if should_push_file(name, remote_resource_names, latest_datasource_versions, force, run_tests):
                    if name not in resource_versions:
                        version = ""
                        if name in latest_datasource_versions:
                            version = f"(v{latest_datasource_versions[name]})"
                        click.echo(FeedbackManager.info_processing_new_resource(name=name, version=version))
                    else:
                        click.echo(
                            FeedbackManager.info_processing_resource(
                                name=name,
                                version=latest_datasource_versions[name],
                                latest_version=resource_versions.get(name),
                            )
                        )
                    try:
                        await exec_file(
                            to_run[name],
                            tb_client,
                            force,
                            check,
                            debug and verbose,
                            populate,
                            populate_subset,
                            populate_condition,
                            unlink_on_populate_error,
                            wait,
                            user_token,
                            override_datasource,
                            ignore_sql_errors,
                            skip_confirmation,
                            only_response_times,
                            run_tests,
                            as_standard,
                            tests_to_run,
                            tests_relative_change,
                            tests_sample_by_params,
                            tests_filter_by,
                            tests_failfast,
                            tests_ignore_order,
                            tests_validate_processed_bytes,
                            tests_check_requests_from_branch,
                            current_ws,
                            fork_downstream,
                            fork,
                            git_release,
                        )
                        if not run_tests:
                            click.echo(
                                FeedbackManager.success_create(
                                    name=(
                                        name
                                        if to_run[name]["version"] is None
                                        else f'{name}__v{to_run[name]["version"]}'
                                    )
                                )
                            )
                    except Exception as e:
                        filename = (
                            os.path.basename(to_run[name]["filename"]) if hide_folders else to_run[name]["filename"]
                        )
                        exception = FeedbackManager.error_push_file_exception(
                            filename=filename,
                            error=e,
                        )
                        raise click.ClickException(exception)
                else:
                    if raise_on_exists:
                        raise AlreadyExistsException(
                            FeedbackManager.warning_name_already_exists(
                                name=name if to_run[name]["version"] is None else f'{name}__v{to_run[name]["version"]}'
                            )
                        )
                    else:
                        if await name_matches_existing_resource(resource, name, tb_client):
                            if resource == "pipes":
                                click.echo(FeedbackManager.error_pipe_cannot_be_pushed(name=name))
                            else:
                                click.echo(FeedbackManager.error_datasource_cannot_be_pushed(name=name))
                        else:
                            click.echo(
                                FeedbackManager.warning_name_already_exists(
                                    name=(
                                        name
                                        if to_run[name]["version"] is None
                                        else f'{name}__v{to_run[name]["version"]}'
                                    )
                                )
                            )
            else:
                if should_push_file(name, remote_resource_names, latest_datasource_versions, force, run_tests):
                    if name not in resource_versions:
                        version = ""
                        if name in latest_datasource_versions:
                            version = f"(v{latest_datasource_versions[name]})"
                        click.echo(FeedbackManager.info_dry_processing_new_resource(name=name, version=version))
                    else:
                        click.echo(
                            FeedbackManager.info_dry_processing_resource(
                                name=name,
                                version=latest_datasource_versions[name],
                                latest_version=resource_versions.get(name),
                            )
                        )
                else:
                    if await name_matches_existing_resource(resource, name, tb_client):
                        if resource == "pipes":
                            click.echo(FeedbackManager.warning_pipe_cannot_be_pushed(name=name))
                        else:
                            click.echo(FeedbackManager.warning_datasource_cannot_be_pushed(name=name))
                    else:
                        click.echo(FeedbackManager.warning_dry_name_already_exists(name=name))

    async def push_files(
        dependency_graph: GraphDependencies,
        dry_run: bool = False,
        check_backfill_required: bool = False,
    ):
        endpoints_dep_map = dict()
        processed = set()

        dependencies_graph = dependency_graph.dep_map
        resources_to_run = dependency_graph.to_run

        if not fork_downstream:
            # First, we will deploy the all the resources following the dependency graph except for the endpoints
            groups = [group for group in toposort(dependencies_graph)]
            for group in groups:
                for name in group:
                    if name in processed:
                        continue

                    if is_endpoint_with_no_dependencies(
                        resources_to_run.get(name, {}),
                        dependencies_graph,
                        resources_to_run,
                    ):
                        endpoints_dep_map[name] = dependencies_graph[name]
                        continue

                    await push(
                        name,
                        resources_to_run,
                        resource_versions,
                        latest_datasource_versions,
                        dry_run,
                        fork_downstream,
                        fork,
                    )
                    processed.add(name)

            # Then, we will deploy the endpoints that are on the dependency graph
            groups = [group for group in toposort(endpoints_dep_map)]
            for group in groups:
                for name in group:
                    if name not in processed:
                        await push(
                            name,
                            resources_to_run,
                            resource_versions,
                            latest_datasource_versions,
                            dry_run,
                            fork_downstream,
                            fork,
                        )
                        processed.add(name)
        else:
            # This will generate the graph from right to left and will fill the gaps of the dependencies
            # If we have a graph like this:
            # A -> B -> C
            # If we only modify A, the normal dependencies graph will only contain a node like _{A => B}
            # But we need a graph that contains A, B and C and the dependencies between them to deploy them in the right order
            dependencies_graph_fork_downstream, resources_to_run_fork_downstream = generate_forkdownstream_graph(
                dependency_graph.all_dep_map,
                dependency_graph.all_resources,
                resources_to_run,
                list(dependency_graph.dep_map.keys()),
            )

            # First, we will deploy the datasources that need to be deployed.
            # We need to deploy the datasources from left to right as some datasources might have MV that depend on the column types of previous datasources. Ex: `test_change_column_type_landing_datasource` test
            groups = [group for group in toposort(dependencies_graph_fork_downstream)]
            groups.reverse()
            for group in groups:
                for name in group:
                    if name in processed or not is_datasource(resources_to_run_fork_downstream[name]):
                        continue

                    # If the resource is new, we will use the normal resource information to deploy it
                    # This is mostly used for datasources with connections.
                    # At the moment, `resources_to_run_fork_downstream` is generated by `all_resources` and this is generated using the parameter `skip_connectors=True`
                    # TODO: Should the `resources_to_run_fork_downstream` be generated using the `skip_connectors` parameter?
                    if is_new(name, changed, dependencies_graph_fork_downstream, dependencies_graph_fork_downstream):
                        await push(
                            name,
                            resources_to_run,
                            resource_versions,
                            latest_datasource_versions,
                            dry_run,
                            fork_downstream,
                            fork,
                        )
                    else:
                        # If we are trying to modify a Kafka or CDK datasource, we need to inform the user that the resource needs to be post-released
                        kafka_connection_name = (
                            resources_to_run_fork_downstream[name].get("params", {}).get("kafka_connection_name")
                        )
                        service = resources_to_run_fork_downstream[name].get("params", {}).get("import_service")
                        if release_created and (kafka_connection_name or service):
                            connector = "Kafka" if kafka_connection_name else service
                            error_msg = FeedbackManager.error_connector_require_post_release(connector=connector)
                            raise click.ClickException(error_msg)

                        # If we are pushing a modified datasource, inform about the backfill``
                        if check_backfill_required and auto_promote and release_created:
                            error_msg = FeedbackManager.error_check_backfill_required(resource_name=name)
                            raise click.ClickException(error_msg)

                        await push(
                            name,
                            resources_to_run_fork_downstream,
                            resource_versions,
                            latest_datasource_versions,
                            dry_run,
                            fork_downstream,
                            fork,
                        )
                    processed.add(name)

            # Now, we will create a map of all the endpoints and there dependencies
            # We are using the forkdownstream graph to get the dependencies of the endpoints as the normal dependencies graph only contains the resources that are going to be deployed
            # But does not include the missing gaps
            # If we have ENDPOINT_A ----> MV_PIPE_B -----> DATASOURCE_B ------> ENDPOINT_C
            # Where endpoint A is being used in the MV_PIPE_B, if we only modify the endpoint A
            # The dependencies graph will only contain the endpoint A and the MV_PIPE_B, but not the DATASOURCE_B and the ENDPOINT_C
            groups = [group for group in toposort(dependencies_graph_fork_downstream)]
            for group in groups:
                for name in group:
                    if name in processed or not is_endpoint(resources_to_run_fork_downstream[name]):
                        continue

                    endpoints_dep_map[name] = dependencies_graph_fork_downstream[name]

            # Now that we have the dependencies of the endpoints, we need to check that the resources has not been deployed yet and only care about the endpoints that depend on endpoints
            groups = [group for group in toposort(endpoints_dep_map)]

            # As we have used the forkdownstream graph to get the dependencies of the endpoints, we have all the dependencies of the endpoints
            # But we need to deploy the endpoints and the dependencies of the endpoints from left to right
            # So we need to reverse the groups
            groups.reverse()
            for group in groups:
                for name in group:
                    if name in processed or not is_endpoint(resources_to_run_fork_downstream[name]):
                        continue

                    await push(
                        name,
                        resources_to_run_fork_downstream,
                        resource_versions,
                        latest_datasource_versions,
                        dry_run,
                        fork_downstream,
                        fork,
                    )
                    processed.add(name)

            # Now we should have the endpoints and datasources deployed, we can deploy the rest of the pipes (copy & sinks)
            # We need to rely on the forkdownstream graph as it contains all the modified pipes as well as the dependencies of the pipes
            # In this case, we don't need to generate a new graph as we did for the endpoints as the pipes are not going to be used as dependencies and the datasources are already deployed
            groups = [group for group in toposort(dependencies_graph_fork_downstream)]
            for group in groups:
                for name in group:
                    if name in processed or is_materialized(resources_to_run_fork_downstream.get(name)):
                        continue

                    await push(
                        name,
                        resources_to_run_fork_downstream,
                        resource_versions,
                        latest_datasource_versions,
                        dry_run,
                        fork_downstream,
                        fork,
                    )
                    processed.add(name)

            # Finally, we need to deploy the materialized views from right to left.
            # We need to rely on the forkdownstream graph as it contains all the modified materialized views as well as the dependencies of the materialized views
            # In this case, we don't need to generate a new graph as we did for the endpoints as the pipes are not going to be used as dependencies and the datasources are already deployed
            groups = [group for group in toposort(dependencies_graph_fork_downstream)]
            for group in groups:
                for name in group:
                    if name in processed or not is_materialized(resources_to_run_fork_downstream.get(name)):
                        continue

                    await push(
                        name,
                        resources_to_run_fork_downstream,
                        resource_versions,
                        latest_datasource_versions,
                        dry_run,
                        fork_downstream,
                        fork,
                    )
                    processed.add(name)

    await push_files(dependencies_graph, dry_run)

    if not dry_run and not run_tests:
        if upload_fixtures:
            click.echo(FeedbackManager.info_pushing_fixtures())

            # We need to upload the fixtures even if there is no change
            if is_branch:
                filenames = get_project_filenames(folder, with_vendor=True)
                dependencies_graph = await build_graph(
                    filenames,
                    tb_client,
                    dir_path=folder,
                    resource_versions=latest_datasource_versions,
                    workspace_map=workspace_map,
                    process_dependencies=push_deps,
                    verbose=verbose,
                    workspace_lib_paths=workspace_lib_paths,
                    current_ws=current_ws,
                )

            processed = set()
            for group in toposort(dependencies_graph.dep_map):
                for f in group:
                    name = os.path.basename(f)
                    if name not in processed and name in dependencies_graph.to_run:
                        await check_fixtures_data(
                            tb_client,
                            dependencies_graph.to_run[name],
                            debug,
                            folder,
                            force,
                            mode="append" if is_branch else "replace",
                        )
                        processed.add(name)
            for f in dependencies_graph.to_run:
                if f not in processed:
                    await check_fixtures_data(
                        tb_client,
                        dependencies_graph.to_run[f],
                        debug,
                        folder,
                        force,
                        mode="append" if is_branch else "replace",
                    )
        else:
            if verbose:
                click.echo(FeedbackManager.info_not_pushing_fixtures())

    return dependencies_graph.to_run
