import json
import logging
from copy import deepcopy
from typing import Any, Dict, List, Optional, Set
from urllib.parse import urlencode

import click
import requests
from croniter import croniter

from tinybird.client import DoesNotExistException, TinyB
from tinybird.feedback_manager import FeedbackManager
from tinybird.tb.modules.common import getenv_bool, requests_delete, requests_get, wait_job
from tinybird.tb.modules.datafile.common import ON_DEMAND, CopyModes, CopyParameters, PipeNodeTypes, PipeTypes
from tinybird.tb.modules.datafile.pipe_checker import PipeCheckerRunner
from tinybird.tb.modules.exceptions import CLIPipeException
from tinybird.tb.modules.table import format_pretty_table


async def new_pipe(
    p,
    tb_client: TinyB,
    force: bool = False,
    check: bool = True,
    populate: bool = False,
    populate_subset=None,
    populate_condition=None,
    unlink_on_populate_error: bool = False,
    wait_populate: bool = False,
    skip_tokens: bool = False,
    ignore_sql_errors: bool = False,
    only_response_times: bool = False,
    run_tests: bool = False,
    as_standard: bool = False,
    tests_to_run: int = 0,
    tests_relative_change: float = 0.01,
    tests_to_sample_by_params: int = 0,
    tests_filter_by: Optional[List[str]] = None,
    tests_failfast: bool = False,
    tests_ignore_order: bool = False,
    tests_validate_processed_bytes: bool = False,
    override_datasource: bool = False,
    tests_check_requests_from_branch: bool = False,
    config: Any = None,
    fork_downstream: Optional[bool] = False,
    fork: Optional[bool] = False,
):
    # TODO use tb_client instead of calling the urls directly.
    host = tb_client.host
    token = tb_client.token

    headers = {"Authorization": f"Bearer {token}"}

    cli_params = {}
    cli_params["cli_version"] = tb_client.version
    cli_params["description"] = p.get("description", "")
    cli_params["ignore_sql_errors"] = "true" if ignore_sql_errors else "false"

    r: requests.Response = await requests_get(f"{host}/v0/pipes/{p['name']}?{urlencode(cli_params)}", headers=headers)

    current_pipe = r.json() if r.status_code == 200 else None
    pipe_exists = current_pipe is not None

    is_materialized = any([node.get("params", {}).get("type", None) == "materialized" for node in p["nodes"]])
    copy_node = next((node for node in p["nodes"] if node.get("params", {}).get("type", None) == "copy"), None)
    sink_node = next((node for node in p["nodes"] if node.get("params", {}).get("type", None) == "sink"), None)
    stream_node = next((node for node in p["nodes"] if node.get("params", {}).get("type", None) == "stream"), None)

    for node in p["nodes"]:
        if node["params"]["name"] == p["name"]:
            raise click.ClickException(FeedbackManager.error_pipe_node_same_name(name=p["name"]))

    if pipe_exists:
        if force or run_tests:
            # TODO: this should create a different node and rename it to the final one on success
            if check and not populate:
                if not is_materialized and not copy_node and not sink_node and not stream_node:
                    await check_pipe(
                        p,
                        host,
                        token,
                        populate,
                        tb_client,
                        only_response_times=only_response_times,
                        limit=tests_to_run,
                        relative_change=tests_relative_change,
                        sample_by_params=tests_to_sample_by_params,
                        matches=tests_filter_by,
                        failfast=tests_failfast,
                        validate_processed_bytes=tests_validate_processed_bytes,
                        ignore_order=tests_ignore_order,
                        token_for_requests_to_check=(
                            await get_token_from_main_branch(tb_client)
                            if not tests_check_requests_from_branch
                            else None
                        ),
                        current_pipe=current_pipe,
                    )
                else:
                    if is_materialized:
                        await check_materialized(
                            p,
                            host,
                            token,
                            tb_client,
                            override_datasource=override_datasource,
                            current_pipe=current_pipe,
                        )
                    if copy_node:
                        await check_copy_pipe(pipe=current_pipe, copy_node=copy_node, tb_client=tb_client)
                    if sink_node:
                        await check_sink_pipe(pipe=current_pipe, sink_node=sink_node, tb_client=tb_client)
                    if stream_node:
                        await check_stream_pipe(pipe=current_pipe, stream_node=stream_node, tb_client=tb_client)
            if run_tests:
                logging.info(f"skipping force override of {p['name']}")
                return
        else:
            raise click.ClickException(FeedbackManager.error_pipe_already_exists(pipe=p["name"]))
    elif not pipe_exists and check:
        if is_materialized:
            await check_materialized(
                p, host, token, tb_client, override_datasource=override_datasource, current_pipe=current_pipe
            )
        if copy_node:
            await check_copy_pipe(pipe=current_pipe, copy_node=copy_node, tb_client=tb_client)

    params = {}
    params.update(cli_params)
    if force:
        params["force"] = "true"
    if populate:
        params["populate"] = "true"
    if populate_condition:
        params["populate_condition"] = populate_condition
    if populate_subset:
        params["populate_subset"] = populate_subset
    params["unlink_on_populate_error"] = "true" if unlink_on_populate_error else "false"
    params["branch_mode"] = "fork" if fork_downstream or fork else "None"

    body = {"name": p["name"], "description": p.get("description", "")}

    def parse_node(node):
        if "params" in node:
            node.update(node["params"])
            if node.get("type", "") == "materialized" and override_datasource:
                node["override_datasource"] = "true"
            del node["params"]
        return node

    if p["nodes"]:
        body["nodes"] = [parse_node(n) for n in p["nodes"]]

    if copy_node:
        body["target_datasource"] = copy_node.get("target_datasource", None)
        # We will update the schedule cron later
        body["schedule_cron"] = None

    if sink_node:
        body.update(sink_node.get("export_params", {}))

    if stream_node:
        body.update(stream_node.get("export_params", {}))

    post_headers = {"Content-Type": "application/json"}

    post_headers.update(headers)

    try:
        data = await tb_client._req(
            f"/v0/pipes?{urlencode(params)}", method="POST", headers=post_headers, data=json.dumps(body)
        )
    except Exception as e:
        raise click.ClickException(FeedbackManager.error_pushing_pipe(pipe=p["name"], error=str(e)))

    datasource = data.get("datasource", None)

    if datasource and populate and not copy_node:
        job_url = data.get("job", {}).get("job_url", None)
        job_id = data.get("job", {}).get("job_id", None)
        if populate_subset:
            click.echo(FeedbackManager.info_populate_subset_job_url(url=job_url, subset=populate_subset))
        elif populate_condition:
            click.echo(
                FeedbackManager.info_populate_condition_job_url(url=job_url, populate_condition=populate_condition)
            )
        else:
            click.echo(FeedbackManager.info_populate_job_url(url=job_url))

        if wait_populate:
            result = await wait_job(tb_client, job_id, job_url, "Populating")
            click.echo(FeedbackManager.info_populate_job_result(result=result))
    else:
        if data.get("type") == "default" and not skip_tokens and not as_standard and not copy_node and not sink_node:
            # FIXME: set option to add last node as endpoint in the API
            endpoint_node = next(
                (node for node in data.get("nodes", []) if node.get("type") == "endpoint"), data.get("nodes", [])[-1]
            )
            try:
                data = await tb_client._req(
                    f"/v0/pipes/{p['name']}/nodes/{endpoint_node.get('id')}/endpoint?{urlencode(cli_params)}",
                    method="POST",
                    headers=headers,
                )
            except Exception as e:
                raise Exception(
                    FeedbackManager.error_creating_endpoint(
                        node=endpoint_node.get("name"), pipe=p["name"], error=str(e)
                    )
                )

    if copy_node:
        pipe_id = data["id"]
        node = next((node for node in data["nodes"] if node["node_type"] == "copy"), None)
        if node:
            copy_params = {"pipe_name_or_id": pipe_id, "node_id": node["id"]}
            try:
                target_datasource = copy_node.get(CopyParameters.TARGET_DATASOURCE, None)
                schedule_cron = copy_node.get(CopyParameters.COPY_SCHEDULE, None)
                mode = copy_node.get("mode", CopyModes.APPEND)
                schedule_cron = None if schedule_cron == ON_DEMAND else schedule_cron
                current_target_datasource_id = data["copy_target_datasource"]
                target_datasource_response = await tb_client.get_datasource(target_datasource)
                target_datasource_to_send = (
                    target_datasource
                    if target_datasource_response.get("id", target_datasource) != current_target_datasource_id
                    else None
                )
                copy_params[CopyParameters.TARGET_DATASOURCE] = target_datasource_to_send
                current_schedule = data.get("schedule", {})
                current_schedule_cron = current_schedule.get("cron", None) if current_schedule else None
                schedule_cron_should_be_removed = current_schedule_cron and not schedule_cron
                copy_params["schedule_cron"] = "None" if schedule_cron_should_be_removed else schedule_cron
                copy_params["mode"] = mode
                await tb_client.pipe_update_copy(**copy_params)
            except Exception as e:
                raise Exception(
                    FeedbackManager.error_setting_copy_node(node=copy_node.get("name"), pipe=p["name"], error=str(e))
                )

    if p["tokens"] and not skip_tokens and not as_standard and data.get("type") in ["endpoint", "copy"]:
        # search for token with specified name and adds it if not found or adds permissions to it
        t = None
        for tk in p["tokens"]:
            token_name = tk["token_name"]
            t = await tb_client.get_token_by_name(token_name)
            if t:
                scopes = [f"PIPES:{tk['permissions']}:{p['name']}"]
                for x in t["scopes"]:
                    sc = x["type"] if "resource" not in x else f"{x['type']}:{x['resource']}"
                    scopes.append(sc)
                try:
                    r = await tb_client.alter_tokens(token_name, scopes)
                    token = r["token"]  # type: ignore
                except Exception as e:
                    raise click.ClickException(FeedbackManager.error_creating_pipe(error=e))
            else:
                token_name = tk["token_name"]
                click.echo(FeedbackManager.info_create_not_found_token(token=token_name))
                try:
                    r = await tb_client.create_token(
                        token_name, [f"PIPES:{tk['permissions']}:{p['name']}"], "P", p["name"]
                    )
                    token = r["token"]  # type: ignore
                except Exception as e:
                    raise click.ClickException(FeedbackManager.error_creating_pipe(error=e))


async def get_token_from_main_branch(branch_tb_client: TinyB) -> Optional[str]:
    token_from_main_branch = None
    current_workspace = await branch_tb_client.workspace_info()
    # current workspace is a branch
    if current_workspace.get("main"):
        response = await branch_tb_client.user_workspaces()
        workspaces = response["workspaces"]
        prod_workspace = next(
            (workspace for workspace in workspaces if workspace["id"] == current_workspace["main"]), None
        )
        if prod_workspace:
            token_from_main_branch = prod_workspace.get("token")
    return token_from_main_branch


async def check_pipe(
    pipe,
    host: str,
    token: str,
    populate: bool,
    cl: TinyB,
    limit: int = 0,
    relative_change: float = 0.01,
    sample_by_params: int = 0,
    only_response_times=False,
    matches: Optional[List[str]] = None,
    failfast: bool = False,
    validate_processed_bytes: bool = False,
    ignore_order: bool = False,
    token_for_requests_to_check: Optional[str] = None,
    current_pipe: Optional[Dict[str, Any]] = None,
):
    checker_pipe = deepcopy(pipe)
    checker_pipe["name"] = f"{checker_pipe['name']}__checker"

    if current_pipe:
        pipe_type = current_pipe["type"]
        if pipe_type == PipeTypes.COPY:
            await cl.pipe_remove_copy(current_pipe["id"], current_pipe["copy_node"])
        if pipe_type == PipeTypes.DATA_SINK:
            await cl.pipe_remove_sink(current_pipe["id"], current_pipe["sink_node"])
        if pipe_type == PipeTypes.STREAM:
            await cl.pipe_remove_stream(current_pipe["id"], current_pipe["stream_node"])

    # In case of doing --force for a materialized view, checker is being created as standard pipe
    for node in checker_pipe["nodes"]:
        node["params"]["type"] = PipeNodeTypes.STANDARD

    if populate:
        raise click.ClickException(FeedbackManager.error_check_pipes_populate())

    runner = PipeCheckerRunner(pipe["name"], host)
    headers = (
        {"Authorization": f"Bearer {token_for_requests_to_check}"}
        if token_for_requests_to_check
        else {"Authorization": f"Bearer {token}"}
    )

    sql_for_coverage, sql_latest_requests = runner.get_sqls_for_requests_to_check(
        matches or [], sample_by_params, limit
    )

    params = {"q": sql_for_coverage if limit == 0 and sample_by_params > 0 else sql_latest_requests}
    r: requests.Response = await requests_get(
        f"{host}/v0/sql?{urlencode(params)}", headers=headers, verify=not getenv_bool("TB_DISABLE_SSL_CHECKS", False)
    )

    # If we get a timeout, fallback to just the last requests

    if not r or r.status_code == 408:
        params = {"q": sql_latest_requests}
        r = await requests_get(
            f"{host}/v0/sql?{urlencode(params)}",
            headers=headers,
            verify=not getenv_bool("TB_DISABLE_SSL_CHECKS", False),
        )

    if not r or r.status_code != 200:
        raise click.ClickException(FeedbackManager.error_check_pipes_api(pipe=pipe["name"]))

    pipe_requests_to_check: List[Dict[str, Any]] = []
    for row in r.json().get("data", []):
        for i in range(len(row["endpoint_url"])):
            pipe_requests_to_check += [
                {
                    "endpoint_url": f"{host}{row['endpoint_url'][i]}",
                    "pipe_request_params": row["pipe_request_params"][i],
                    "http_method": row["http_method"],
                }
            ]

    if not pipe_requests_to_check:
        return

    await new_pipe(checker_pipe, cl, force=True, check=False, populate=populate)

    runner_response = runner.run_pipe_checker(
        pipe_requests_to_check,
        checker_pipe["name"],
        token,
        only_response_times,
        ignore_order,
        validate_processed_bytes,
        relative_change,
        failfast,
    )

    try:
        if runner_response.metrics_summary and runner_response.metrics_timing:
            column_names_tests = ["Test Run", "Test Passed", "Test Failed", "% Test Passed", "% Test Failed"]
            click.echo("\n==== Test Metrics ====\n")
            click.echo(
                format_pretty_table(
                    [
                        [
                            runner_response.metrics_summary["run"],
                            runner_response.metrics_summary["passed"],
                            runner_response.metrics_summary["failed"],
                            runner_response.metrics_summary["percentage_passed"],
                            runner_response.metrics_summary["percentage_failed"],
                        ]
                    ],
                    column_names=column_names_tests,
                )
            )

            column_names_timing = ["Timing Metric (s)", "Current", "New"]
            click.echo("\n==== Response Time Metrics ====\n")
            click.echo(
                format_pretty_table(
                    [
                        [metric, runner_response.metrics_timing[metric][0], runner_response.metrics_timing[metric][1]]
                        for metric in [
                            "min response time",
                            "max response time",
                            "mean response time",
                            "median response time",
                            "p90 response time",
                            "min read bytes",
                            "max read bytes",
                            "mean read bytes",
                            "median read bytes",
                            "p90 read bytes",
                        ]
                    ],
                    column_names=column_names_timing,
                )
            )
    except Exception:
        pass

    if not runner_response.was_successfull:
        for failure in runner_response.failed:
            try:
                click.echo("==== Test FAILED ====\n")
                click.echo(failure["name"])
                click.echo(FeedbackManager.error_check_pipe(error=failure["error"]))
                click.echo("=====================\n\n\n")
            except Exception:
                pass
        raise RuntimeError("Invalid results, you can bypass checks by running push with the --no-check flag")

    # Only delete if no errors, so we can check results after failure
    headers = {"Authorization": f"Bearer {token}"}
    r = await requests_delete(f"{host}/v0/pipes/{checker_pipe['name']}", headers=headers)
    if r.status_code != 204:
        click.echo(FeedbackManager.warning_check_pipe(content=r.content))


async def check_materialized(pipe, host, token, cl, override_datasource=False, current_pipe=None):
    checker_pipe = deepcopy(pipe)
    checker_pipe["name"] = f"{checker_pipe['name']}__checker"
    headers = {"Authorization": f"Bearer {token}"}

    if current_pipe:
        from_copy_to_materialized = current_pipe["type"] == "copy"
        if from_copy_to_materialized:
            await cl.pipe_remove_copy(current_pipe["id"], current_pipe["copy_node"])

    materialized_node = None
    for node in checker_pipe["nodes"]:
        if node["params"]["type"] == "materialized":
            materialized_node = deepcopy(node)
            materialized_node["params"]["override_datasource"] = "true" if override_datasource else "false"
        node["params"]["type"] = "standard"

    try:
        pipe_created = False
        await new_pipe(
            checker_pipe, cl, force=True, check=False, populate=False, skip_tokens=True, ignore_sql_errors=False
        )
        pipe_created = True
        response = await cl.analyze_pipe_node(checker_pipe["name"], materialized_node, dry_run="true")
        if response.get("warnings"):
            show_materialized_view_warnings(response["warnings"])

    except Exception as e:
        raise click.ClickException(FeedbackManager.error_while_check_materialized(error=str(e)))
    finally:
        if pipe_created:
            r = await requests_delete(f"{host}/v0/pipes/{checker_pipe['name']}", headers=headers)
            if r.status_code != 204:
                click.echo(FeedbackManager.warning_check_pipe(content=r.content))


async def check_copy_pipe(pipe, copy_node, tb_client: TinyB):
    target_datasource = copy_node["params"].get("target_datasource", None)
    if not target_datasource:
        raise CLIPipeException(FeedbackManager.error_creating_copy_pipe_target_datasource_required())

    try:
        await tb_client.get_datasource(target_datasource)
    except DoesNotExistException:
        raise CLIPipeException(
            FeedbackManager.error_creating_copy_pipe_target_datasource_not_found(target_datasource=target_datasource)
        )
    except Exception as e:
        raise CLIPipeException(FeedbackManager.error_exception(error=e))

    schedule_cron = copy_node["params"].get(CopyParameters.COPY_SCHEDULE, None)
    is_valid_cron = not schedule_cron or (
        schedule_cron and (schedule_cron == ON_DEMAND or croniter.is_valid(schedule_cron))
    )

    if not is_valid_cron:
        raise CLIPipeException(FeedbackManager.error_creating_copy_pipe_invalid_cron(schedule_cron=schedule_cron))

    mode = copy_node["params"].get("mode", CopyModes.APPEND)
    is_valid_mode = CopyModes.is_valid(mode)

    if not is_valid_mode:
        raise CLIPipeException(FeedbackManager.error_creating_copy_pipe_invalid_mode(mode=mode))

    if not pipe:
        return

    pipe_name = pipe["name"]
    pipe_type = pipe["type"]

    if pipe_type == PipeTypes.ENDPOINT:
        await tb_client.pipe_remove_endpoint(pipe_name, pipe["endpoint"])

    if pipe_type == PipeTypes.DATA_SINK:
        await tb_client.pipe_remove_sink(pipe_name, pipe["sink_node"])

    if pipe_type == PipeTypes.STREAM:
        await tb_client.pipe_remove_stream(pipe_name, pipe["stream_node"])


async def check_sink_pipe(pipe, sink_node, tb_client: TinyB):
    if not sink_node["export_params"]:
        return

    if not pipe:
        return

    pipe_name = pipe["name"]
    pipe_type = pipe["type"]

    schedule_cron = sink_node["export_params"].get("schedule_cron", "")
    is_valid_cron = not schedule_cron or (schedule_cron and croniter.is_valid(schedule_cron))

    if not is_valid_cron:
        raise CLIPipeException(FeedbackManager.error_creating_sink_pipe_invalid_cron(schedule_cron=schedule_cron))

    if pipe_type == PipeTypes.ENDPOINT:
        await tb_client.pipe_remove_endpoint(pipe_name, pipe["endpoint"])

    if pipe_type == PipeTypes.COPY:
        await tb_client.pipe_remove_copy(pipe_name, pipe["copy_node"])

    if pipe_type == PipeTypes.STREAM:
        await tb_client.pipe_remove_stream(pipe_name, pipe["stream_node"])


async def check_stream_pipe(pipe, stream_node, tb_client: TinyB):
    if not stream_node["params"]:
        return

    if not pipe:
        return

    pipe_name = pipe["name"]
    pipe_type = pipe["type"]

    if pipe_type == PipeTypes.ENDPOINT:
        await tb_client.pipe_remove_endpoint(pipe_name, pipe["endpoint"])

    if pipe_type == PipeTypes.COPY:
        await tb_client.pipe_remove_copy(pipe_name, pipe["copy_node"])

    if pipe_type == PipeTypes.DATA_SINK:
        await tb_client.pipe_remove_sink(pipe_name, pipe["sink_node"])


def show_materialized_view_warnings(warnings):
    """
    >>> show_materialized_view_warnings([{'code': 'SIM', 'weight': 1}])

    >>> show_materialized_view_warnings([{'code': 'SIM', 'weight': 1}, {'code': 'HUGE_JOIN', 'weight': 2}, {'text': "Column 'number' is present in the GROUP BY but not in the SELECT clause. This might indicate a not valid Materialized View, please make sure you aggregate and GROUP BY in the topmost query.", 'code': 'GROUP_BY', 'weight': 100, 'documentation': 'https://tinybird.co/docs/guides/materialized-views.html#use-the-same-alias-in-select-and-group-by'}])
    ⚠️  Column 'number' is present in the GROUP BY but not in the SELECT clause. This might indicate a not valid Materialized View, please make sure you aggregate and GROUP BY in the topmost query. For more information read https://tinybird.co/docs/guides/materialized-views.html#use-the-same-alias-in-select-and-group-by or contact us at support@tinybird.co
    >>> show_materialized_view_warnings([{'code': 'SINGLE_JOIN', 'weight': 300}, {'text': "Column 'number' is present in the GROUP BY but not in the SELECT clause. This might indicate a not valid Materialized View, please make sure you aggregate and GROUP BY in the topmost query.", 'code': 'GROUP_BY', 'weight': 100, 'documentation': 'https://tinybird.co/docs/guides/materialized-views.html#use-the-same-alias-in-select-and-group-by'}])
    ⚠️  Column 'number' is present in the GROUP BY but not in the SELECT clause. This might indicate a not valid Materialized View, please make sure you aggregate and GROUP BY in the topmost query. For more information read https://tinybird.co/docs/guides/materialized-views.html#use-the-same-alias-in-select-and-group-by or contact us at support@tinybird.co
    """
    excluded_warnings = ["SIM", "SIM_UNKNOWN", "HUGE_JOIN"]
    sorted_warnings = sorted(warnings, key=lambda warning: warning["weight"])
    most_important_warning = {}
    for warning in sorted_warnings:
        if warning.get("code") and warning["code"] not in excluded_warnings:
            most_important_warning = warning
            break
    if most_important_warning:
        click.echo(
            FeedbackManager.single_warning_materialized_pipe(
                content=most_important_warning["text"], docs_url=most_important_warning["documentation"]
            )
        )


def is_endpoint_with_no_dependencies(
    resource: Dict[str, Any], dep_map: Dict[str, Set[str]], to_run: Dict[str, Dict[str, Any]]
) -> bool:
    if not resource or resource.get("resource") == "datasources":
        return False

    for node in resource.get("nodes", []):
        # FIXME: https://gitlab.com/tinybird/analytics/-/issues/2391
        if node.get("params", {}).get("type", "").lower() in [
            PipeNodeTypes.MATERIALIZED,
            PipeNodeTypes.COPY,
            PipeNodeTypes.DATA_SINK,
            PipeNodeTypes.STREAM,
        ]:
            return False

    for key, values in dep_map.items():
        if resource["resource_name"] in values:
            r = to_run.get(key, None)
            if not r:
                continue
            return False

    deps = dep_map.get(resource["resource_name"])
    if not deps:
        return True

    for dep in deps:
        r = to_run.get(dep, None)
        if is_endpoint(r) or is_materialized(r):
            return False

    return True


def is_endpoint(resource: Optional[Dict[str, Any]]) -> bool:
    if resource and len(resource.get("tokens", [])) != 0 and resource.get("resource") == "pipes":
        return True
    return False


def is_materialized(resource: Optional[Dict[str, Any]]) -> bool:
    if not resource:
        return False

    is_materialized = any(
        [node.get("params", {}).get("type", None) == "materialized" for node in resource.get("nodes", []) or []]
    )
    return is_materialized


def get_target_materialized_data_source_name(resource: Optional[Dict[str, Any]]) -> Optional[str]:
    if not resource:
        return None

    for node in resource.get("nodes", []):
        # FIXME: https://gitlab.com/tinybird/analytics/-/issues/2391
        if node.get("params", {}).get("type", "").lower() == PipeNodeTypes.MATERIALIZED:
            return node.get("params")["datasource"].split("__v")[0]

    return None
