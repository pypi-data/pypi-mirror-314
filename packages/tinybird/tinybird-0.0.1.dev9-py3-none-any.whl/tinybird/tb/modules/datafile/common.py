import glob
import itertools
import os
import os.path
import pprint
import re
import shlex
import textwrap
import traceback
from collections import namedtuple
from io import StringIO
from pathlib import Path
from string import Template
from typing import Any, Callable, Dict, List, Optional, Tuple, cast

import click
from mypy_extensions import KwArg, VarArg

from tinybird.ch_utils.engine import ENABLED_ENGINES
from tinybird.feedback_manager import FeedbackManager
from tinybird.sql import parse_indexes_structure, parse_table_structure, schema_to_sql_columns
from tinybird.tb.modules.datafile.exceptions import IncludeFileNotFoundException, ParseException, ValidationException
from tinybird.tb.modules.exceptions import CLIPipeException


class PipeTypes:
    MATERIALIZED = "materialized"
    ENDPOINT = "endpoint"
    COPY = "copy"
    DATA_SINK = "sink"
    STREAM = "stream"
    DEFAULT = "default"


class PipeNodeTypes:
    MATERIALIZED = "materialized"
    ENDPOINT = "endpoint"
    STANDARD = "standard"
    DEFAULT = "default"
    DATA_SINK = "sink"
    COPY = "copy"
    STREAM = "stream"


class DataFileExtensions:
    PIPE = ".pipe"
    DATASOURCE = ".datasource"
    INCL = ".incl"


class CopyModes:
    APPEND = "append"
    REPLACE = "replace"

    valid_modes = (APPEND, REPLACE)

    @staticmethod
    def is_valid(node_mode):
        return node_mode.lower() in CopyModes.valid_modes


class CopyParameters:
    TARGET_DATASOURCE = "target_datasource"
    COPY_SCHEDULE = "copy_schedule"
    COPY_MODE = "copy_mode"


DATAFILE_NEW_LINE = "\n"
DATAFILE_INDENT = " " * 4

ON_DEMAND = "@on-demand"
DEFAULT_CRON_PERIOD: int = 60

INTERNAL_TABLES: Tuple[str, ...] = (
    "datasources_ops_log",
    "pipe_stats",
    "pipe_stats_rt",
    "block_log",
    "data_connectors_log",
    "kafka_ops_log",
    "datasources_storage",
    "endpoint_errors",
    "bi_stats_rt",
    "bi_stats",
)

PREVIEW_CONNECTOR_SERVICES = ["s3", "s3_iamrole", "gcs"]
TB_LOCAL_WORKSPACE_NAME = "Tinybird_Local_Testing"

pp = pprint.PrettyPrinter()


class Datafile:
    def __init__(self) -> None:
        self.maintainer: Optional[str] = None
        self.sources: List[str] = []
        self.nodes: List[Dict[str, Any]] = []
        self.tokens: List[Dict[str, Any]] = []
        self.version: Optional[int] = None
        self.description: Optional[str] = None
        self.raw: Optional[List[str]] = None
        self.includes: Dict[str, Any] = {}
        self.shared_with: List[str] = []
        self.warnings: List[str] = []
        self.filtering_tags: Optional[List[str]] = None

    def validate(self) -> None:
        for x in self.nodes:
            if not x["name"].strip():
                raise ValidationException("invalid node name, can't be empty")
            if "sql" not in x:
                raise ValidationException("node %s must have a SQL query" % x["name"])
        if self.version is not None and (not isinstance(self.version, int) or self.version < 0):
            raise ValidationException("version must be a positive integer")

    def is_equal(self, other):
        if len(self.nodes) != len(other.nodes):
            return False

        return all(self.nodes[i] == other.nodes[i] for i, _ in enumerate(self.nodes))


def format_filename(filename: str, hide_folders: bool = False):
    return os.path.basename(filename) if hide_folders else filename


def _unquote(x: str):
    QUOTES = ('"', "'")
    if x[0] in QUOTES and x[-1] in QUOTES:
        x = x[1:-1]
    return x


def eval_var(s: str, skip: bool = False) -> str:
    if skip:
        return s
    # replace ENV variables
    # it's probably a bad idea to allow to get any env var
    return Template(s).safe_substitute(os.environ)


def parse_tags(tags: str) -> Tuple[str, List[str]]:
    """
    Parses a string of tags into:
    - kv_tags: a string of key-value tags: the previous tags we have for operational purposes. It
        has the format key=value&key2=value2 (with_staging=true&with_last_date=true)
    - filtering_tags: a list of tags that are used for filtering.

    Example: "with_staging=true&with_last_date=true,billing,stats" ->
        kv_tags = {"with_staging": "true", "with_last_date": "true"}
        filtering_tags = ["billing", "stats"]
    """
    kv_tags = []
    filtering_tags = []

    entries = tags.split(",")
    for entry in entries:
        trimmed_entry = entry.strip()
        if "=" in trimmed_entry:
            kv_tags.append(trimmed_entry)
        else:
            filtering_tags.append(trimmed_entry)

    all_kv_tags = "&".join(kv_tags)

    return all_kv_tags, filtering_tags


def parse(
    s: str,
    default_node: Optional[str] = None,
    basepath: str = ".",
    replace_includes: bool = True,
    skip_eval: bool = False,
) -> Datafile:
    """
    Parses `s` string into a document
    >>> d = parse("FROM SCRATCH\\nSOURCE 'https://example.com'\\n#this is a comment\\nMAINTAINER 'rambo' #this is me\\nNODE \\"test_01\\"\\n    DESCRIPTION this is a node that does whatever\\nSQL >\\n\\n        SELECT * from test_00\\n\\n\\nNODE \\"test_02\\"\\n    DESCRIPTION this is a node that does whatever\\nSQL >\\n\\n    SELECT * from test_01\\n    WHERE a > 1\\n    GROUP by a\\n")
    >>> d.maintainer
    'rambo'
    >>> d.sources
    ['https://example.com']
    >>> len(d.nodes)
    2
    >>> d.nodes[0]
    {'name': 'test_01', 'description': 'this is a node that does whatever', 'sql': 'SELECT * from test_00'}
    >>> d.nodes[1]
    {'name': 'test_02', 'description': 'this is a node that does whatever', 'sql': 'SELECT * from test_01\\nWHERE a > 1\\nGROUP by a'}
    """
    lines = list(StringIO(s, newline=None))

    doc = Datafile()
    doc.raw = list(StringIO(s, newline=None))

    parser_state = namedtuple("parser_state", ["multiline", "current_node", "command", "multiline_string", "is_sql"])

    parser_state.multiline = False
    parser_state.current_node = False

    def assign(attr):
        def _fn(x, **kwargs):
            setattr(doc, attr, _unquote(x))

        return _fn

    def schema(*args, **kwargs):
        s = _unquote("".join(args))
        try:
            sh = parse_table_structure(s)
        except Exception as e:
            raise ParseException(FeedbackManager.error_parsing_schema(line=kwargs["lineno"], error=e))

        parser_state.current_node["schema"] = ",".join(schema_to_sql_columns(sh))
        parser_state.current_node["columns"] = sh

    def indexes(*args, **kwargs):
        s = _unquote("".join(args))
        if not s:
            return
        try:
            indexes = parse_indexes_structure(s.splitlines())
        except Exception as e:
            raise ParseException(FeedbackManager.error_parsing_indices(line=kwargs["lineno"], error=e))

        parser_state.current_node["indexes"] = indexes

    def assign_var(v: str) -> Callable[[VarArg(str), KwArg(Any)], None]:
        def _f(*args: str, **kwargs: Any):
            s = _unquote((" ".join(args)).strip())
            parser_state.current_node[v.lower()] = eval_var(s, skip=skip_eval)

        return _f

    def sources(x: str, **kwargs: Any) -> None:
        doc.sources.append(_unquote(x))

    def node(*args: str, **kwargs: Any) -> None:
        node = {"name": eval_var(_unquote(args[0]))}
        doc.nodes.append(node)
        parser_state.current_node = node

    def scope(*args: str, **kwargs: Any) -> None:
        scope = {"name": eval_var(_unquote(args[0]))}
        doc.nodes.append(scope)
        parser_state.current_node = scope

    def description(*args: str, **kwargs: Any) -> None:
        description = (" ".join(args)).strip()

        if parser_state.current_node:
            parser_state.current_node["description"] = description
            if parser_state.current_node.get("name", "") == "default":
                doc.description = description
        else:
            doc.description = description

    def sql(var_name: str, **kwargs: Any) -> Callable[[str, KwArg(Any)], None]:
        def _f(sql: str, **kwargs: Any) -> None:
            if not parser_state.current_node:
                raise ParseException("SQL must be called after a NODE command")
            parser_state.current_node[var_name] = (
                textwrap.dedent(sql).rstrip() if "%" not in sql.strip()[0] else sql.strip()
            )

        # HACK this cast is needed because Mypy
        return cast(Callable[[str, KwArg(Any)], None], _f)

    def assign_node_var(v: str) -> Callable[[VarArg(str), KwArg(Any)], None]:
        def _f(*args: str, **kwargs: Any) -> None:
            if not parser_state.current_node:
                raise ParseException("%s must be called after a NODE command" % v)
            return assign_var(v)(*args, **kwargs)

        return _f

    def add_token(*args: str, **kwargs: Any) -> None:  # token_name, permissions):
        if len(args) < 2:
            raise ParseException('TOKEN gets two params, token name and permissions e.g TOKEN "read api token" READ')
        doc.tokens.append({"token_name": _unquote(args[0]), "permissions": args[1]})

    def test(*args: str, **kwargs: Any) -> None:
        # TODO: Should be removed?
        print("test", args, kwargs)  # noqa: T201

    def include(*args: str, **kwargs: Any) -> None:
        f = _unquote(args[0])
        f = eval_var(f)
        attrs = dict(_unquote(x).split("=", 1) for x in args[1:])
        nonlocal lines
        lineno = kwargs["lineno"]
        replace_includes = kwargs["replace_includes"]
        n = lineno
        args_with_attrs = " ".join(args)

        try:
            while True:
                n += 1
                if len(lines) <= n:
                    break
                if "NODE" in lines[n]:
                    doc.includes[args_with_attrs] = lines[n]
                    break
            if args_with_attrs not in doc.includes:
                doc.includes[args_with_attrs] = ""
        except Exception:
            pass

        # If this parse was triggered by format, we don't want to replace the file
        if not replace_includes:
            return

        # be sure to replace the include line
        p = Path(basepath)

        try:
            with open(p / f) as file:
                try:
                    ll = list(StringIO(file.read(), newline=None))
                    node_line = [line for line in ll if "NODE" in line]
                    if node_line and doc.includes[args_with_attrs]:
                        doc.includes[node_line[0].split("NODE")[-1].split("\n")[0].strip()] = ""
                except Exception:
                    pass
                finally:
                    file.seek(0)
                lines[lineno : lineno + 1] = [
                    "",
                    *list(StringIO(Template(file.read()).safe_substitute(attrs), newline=None)),
                ]
        except FileNotFoundError:
            raise IncludeFileNotFoundException(f, lineno)

    def version(*args: str, **kwargs: Any) -> None:
        if len(args) < 1:
            raise ParseException("VERSION gets one positive integer param")
        try:
            version = int(args[0])
            if version < 0:
                raise ValidationException("version must be a positive integer e.g VERSION 2")
            doc.version = version
        except ValueError:
            raise ValidationException("version must be a positive integer e.g VERSION 2")

    def shared_with(*args: str, **kwargs: Any) -> None:
        for entries in args:
            # In case they specify multiple workspaces
            doc.shared_with += [workspace.strip() for workspace in entries.splitlines()]

    def __init_engine(v: str):
        if not parser_state.current_node:
            raise Exception(f"{v} must be called after a NODE command")
        if "engine" not in parser_state.current_node:
            parser_state.current_node["engine"] = {"type": None, "args": []}

    def set_engine(*args: str, **kwargs: Any) -> None:
        __init_engine("ENGINE")
        engine_type = _unquote((" ".join(args)).strip())
        parser_state.current_node["engine"]["type"] = eval_var(engine_type, skip=skip_eval)

    def add_engine_var(v: str) -> Callable[[VarArg(str), KwArg(Any)], None]:
        def _f(*args: str, **kwargs: Any):
            __init_engine(f"ENGINE_{v}".upper())
            engine_arg = eval_var(_unquote((" ".join(args)).strip()), skip=skip_eval)
            parser_state.current_node["engine"]["args"].append((v, engine_arg))

        return _f

    def tags(*args: str, **kwargs: Any) -> None:
        raw_tags = _unquote((" ".join(args)).strip())
        operational_tags, filtering_tags = parse_tags(raw_tags)

        # Pipe nodes or Data Sources
        if parser_state.current_node and operational_tags:
            operational_tags_args = (operational_tags,)
            assign_node_var("tags")(*operational_tags_args, **kwargs)

        if filtering_tags:
            if doc.filtering_tags is None:
                doc.filtering_tags = filtering_tags
            else:
                doc.filtering_tags += filtering_tags

    cmds = {
        "from": assign("from"),
        "source": sources,
        "maintainer": assign("maintainer"),
        "schema": schema,
        "indexes": indexes,
        # TODO: Added to be able to merge MR 11347, let's remove it afterwards
        "indices": indexes,
        "engine": set_engine,
        "partition_key": assign_var("partition_key"),
        "sorting_key": assign_var("sorting_key"),
        "primary_key": assign_var("primary_key"),
        "sampling_key": assign_var("sampling_key"),
        "ttl": assign_var("ttl"),
        "settings": assign_var("settings"),
        "node": node,
        "scope": scope,
        "description": description,
        "type": assign_node_var("type"),
        "datasource": assign_node_var("datasource"),
        "tags": tags,
        "target_datasource": assign_node_var("target_datasource"),
        "copy_schedule": assign_node_var(CopyParameters.COPY_SCHEDULE),
        "copy_mode": assign_node_var("mode"),
        "mode": assign_node_var("mode"),
        "resource": assign_node_var("resource"),
        "filter": assign_node_var("filter"),
        "token": add_token,
        "test": test,
        "include": include,
        "sql": sql("sql"),
        "version": version,
        "kafka_connection_name": assign_var("kafka_connection_name"),
        "kafka_topic": assign_var("kafka_topic"),
        "kafka_group_id": assign_var("kafka_group_id"),
        "kafka_bootstrap_servers": assign_var("kafka_bootstrap_servers"),
        "kafka_key": assign_var("kafka_key"),
        "kafka_secret": assign_var("kafka_secret"),
        "kafka_schema_registry_url": assign_var("kafka_schema_registry_url"),
        "kafka_target_partitions": assign_var("kafka_target_partitions"),
        "kafka_auto_offset_reset": assign_var("kafka_auto_offset_reset"),
        "kafka_store_raw_value": assign_var("kafka_store_raw_value"),
        "kafka_store_headers": assign_var("kafka_store_headers"),
        "kafka_store_binary_headers": assign_var("kafka_store_binary_headers"),
        "kafka_key_avro_deserialization": assign_var("kafka_key_avro_deserialization"),
        "kafka_ssl_ca_pem": assign_var("kafka_ssl_ca_pem"),
        "kafka_sasl_mechanism": assign_var("kafka_sasl_mechanism"),
        "import_service": assign_var("import_service"),
        "import_connection_name": assign_var("import_connection_name"),
        "import_schedule": assign_var("import_schedule"),
        "import_strategy": assign_var("import_strategy"),
        "import_external_datasource": assign_var("import_external_datasource"),
        "import_bucket_uri": assign_var("import_bucket_uri"),
        "import_from_timestamp": assign_var("import_from_timestamp"),
        "import_query": assign_var("import_query"),
        "import_table_arn": assign_var("import_table_arn"),
        "import_export_bucket": assign_var("import_export_bucket"),
        "shared_with": shared_with,
        "export_service": assign_var("export_service"),
        "export_connection_name": assign_var("export_connection_name"),
        "export_schedule": assign_var("export_schedule"),
        "export_bucket_uri": assign_var("export_bucket_uri"),
        "export_file_template": assign_var("export_file_template"),
        "export_format": assign_var("export_format"),
        "export_strategy": assign_var("export_strategy"),
        "export_compression": assign_var("export_compression"),
        "export_kafka_topic": assign_var("export_kafka_topic"),
    }

    engine_vars = set()

    for _engine, (params, options) in ENABLED_ENGINES:
        for p in params:
            engine_vars.add(p.name)
        for o in options:
            engine_vars.add(o.name)
    for v in engine_vars:
        cmds[f"engine_{v}"] = add_engine_var(v)

    if default_node:
        node(default_node)

    lineno = 0
    try:
        while lineno < len(lines):
            line = lines[lineno]
            try:
                sa = shlex.shlex(line)
                sa.whitespace_split = True
                lexer = list(sa)
            except ValueError:
                sa = shlex.shlex(shlex.quote(line))
                sa.whitespace_split = True
                lexer = list(sa)
            if lexer:
                cmd, args = lexer[0], lexer[1:]
                if (
                    parser_state.multiline
                    and cmd.lower() in cmds
                    and not (line.startswith(" ") or line.startswith("\t") or line.lower().startswith("from"))
                ):
                    parser_state.multiline = False
                    cmds[parser_state.command](
                        parser_state.multiline_string, lineno=lineno, replace_includes=replace_includes
                    )

                if not parser_state.multiline:
                    if len(args) >= 1 and args[0] == ">":
                        parser_state.multiline = True
                        parser_state.command = cmd.lower()
                        parser_state.multiline_string = ""
                    else:
                        if cmd.lower() == "settings":
                            raise click.ClickException(FeedbackManager.error_settings_not_allowed())
                        if cmd.lower() in cmds:
                            cmds[cmd.lower()](*args, lineno=lineno, replace_includes=replace_includes)
                        else:
                            raise click.ClickException(FeedbackManager.error_option(option=cmd.upper()))
                else:
                    parser_state.multiline_string += line
            lineno += 1
        # close final state
        if parser_state.multiline:
            cmds[parser_state.command](parser_state.multiline_string, lineno=lineno, replace_includes=replace_includes)
    except ParseException as e:
        raise ParseException(str(e), lineno=lineno)
    except ValidationException as e:
        raise ValidationException(str(e), lineno=lineno)
    except IndexError as e:
        if "node" in line.lower():
            raise click.ClickException(FeedbackManager.error_missing_node_name())
        elif "sql" in line.lower():
            raise click.ClickException(FeedbackManager.error_missing_sql_command())
        elif "datasource" in line.lower():
            raise click.ClickException(FeedbackManager.error_missing_datasource_name())
        else:
            raise ValidationException(f"Validation error, found {line} in line {str(lineno)}: {str(e)}", lineno=lineno)
    except IncludeFileNotFoundException as e:
        raise IncludeFileNotFoundException(str(e), lineno=lineno)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        raise ParseException(f"Unexpected error: {e}", lineno=lineno)

    return doc


class ImportReplacements:
    _REPLACEMENTS: Tuple[Tuple[str, str, Optional[str]], ...] = (
        ("import_service", "service", None),
        ("import_strategy", "mode", "replace"),
        ("import_connection_name", "connection", None),
        ("import_schedule", "cron", ON_DEMAND),
        ("import_query", "query", None),
        ("import_connector", "connector", None),
        ("import_external_datasource", "external_data_source", None),
        ("import_bucket_uri", "bucket_uri", None),
        ("import_from_timestamp", "from_time", None),
        ("import_table_arn", "dynamodb_table_arn", None),
        ("import_export_bucket", "dynamodb_export_bucket", None),
    )

    @staticmethod
    def get_datafile_parameter_keys() -> List[str]:
        return [x[0] for x in ImportReplacements._REPLACEMENTS]

    @staticmethod
    def get_api_param_for_datafile_param(connector_service: str, key: str) -> Tuple[Optional[str], Optional[str]]:
        """Returns the API parameter name and default value for a given
        datafile parameter.
        """
        key = key.lower()
        for datafile_k, linker_k, value in ImportReplacements._REPLACEMENTS:
            if datafile_k == key:
                return linker_k, value
        return None, None

    @staticmethod
    def get_datafile_param_for_linker_param(connector_service: str, linker_param: str) -> Optional[str]:
        """Returns the datafile parameter name for a given linter parameter."""
        linker_param = linker_param.lower()
        for datafile_k, linker_k, _ in ImportReplacements._REPLACEMENTS:
            if linker_k == linker_param:
                return datafile_k
        return None

    @staticmethod
    def get_datafile_value_for_linker_value(
        connector_service: str, linker_param: str, linker_value: str
    ) -> Optional[str]:
        """Map linker values to datafile values."""
        linker_param = linker_param.lower()
        if linker_param != "cron":
            return linker_value
        if linker_value == "@once":
            return ON_DEMAND
        if connector_service in PREVIEW_CONNECTOR_SERVICES:
            return "@auto"
        return linker_value


class ExportReplacements:
    SERVICES = ("gcs_hmac", "s3", "s3_iamrole", "kafka")
    NODE_TYPES = (PipeNodeTypes.DATA_SINK, PipeNodeTypes.STREAM)
    _REPLACEMENTS = (
        ("export_service", "service", None),
        ("export_connection_name", "connection", None),
        ("export_schedule", "schedule_cron", ""),
        ("export_bucket_uri", "path", None),
        ("export_file_template", "file_template", None),
        ("export_format", "format", "csv"),
        ("export_compression", "compression", None),
        ("export_strategy", "strategy", "@new"),
        ("export_kafka_topic", "kafka_topic", None),
        ("kafka_connection_name", "connection", None),
        ("kafka_topic", "kafka_topic", None),
    )

    @staticmethod
    def get_export_service(node: Dict[str, Optional[str]]) -> str:
        if (node.get("type", "standard") or "standard").lower() == PipeNodeTypes.STREAM:
            return "kafka"
        return (node.get("export_service", "") or "").lower()

    @staticmethod
    def get_node_type(node: Dict[str, Optional[str]]) -> str:
        return (node.get("type", "standard") or "standard").lower()

    @staticmethod
    def is_export_node(node: Dict[str, Optional[str]]) -> bool:
        export_service = ExportReplacements.get_export_service(node)
        node_type = (node.get("type", "standard") or "standard").lower()
        if not export_service:
            return False
        if export_service not in ExportReplacements.SERVICES:
            raise CLIPipeException(f"Invalid export service: {export_service}")
        if node_type not in ExportReplacements.NODE_TYPES:
            raise CLIPipeException(f"Invalid export node type: {node_type}")
        return True

    @staticmethod
    def get_params_from_datafile(node: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
        """Returns the export parameters for a given node."""
        params = {}
        node_type = ExportReplacements.get_node_type(node)
        for datafile_key, export_key, default_value in ExportReplacements._REPLACEMENTS:
            if node_type != PipeNodeTypes.STREAM and datafile_key.startswith("kafka_"):
                continue
            if node_type == PipeNodeTypes.STREAM and datafile_key.startswith("export_"):
                continue
            if datafile_key == "export_schedule" and node.get(datafile_key, None) == ON_DEMAND:
                node[datafile_key] = ""
            params[export_key] = node.get(datafile_key, default_value)
        return params

    @staticmethod
    def get_datafile_key(param: str, node: Dict[str, Optional[str]]) -> Optional[str]:
        """Returns the datafile key for a given export parameter."""
        node_type = ExportReplacements.get_node_type(node)
        for datafile_key, export_key, _ in ExportReplacements._REPLACEMENTS:
            if node_type != PipeNodeTypes.STREAM and datafile_key.startswith("kafka_"):
                continue
            if node_type == PipeNodeTypes.STREAM and datafile_key.startswith("export_"):
                continue
            if export_key == param.lower():
                return datafile_key.upper()
        return None


def get_project_filenames(folder: str, with_vendor=False) -> List[str]:
    folders: List[str] = [
        f"{folder}/*.datasource",
        f"{folder}/datasources/*.datasource",
        f"{folder}/*.pipe",
        f"{folder}/pipes/*.pipe",
        f"{folder}/endpoints/*.pipe",
        f"{folder}/materializations/*.pipe",
        f"{folder}/sinks/*.pipe",
        f"{folder}/copies/*.pipe",
        f"{folder}/playgrounds/*.pipe",
    ]
    if with_vendor:
        folders.append(f"{folder}/vendor/**/**/*.datasource")
    filenames: List[str] = []
    for x in folders:
        filenames += glob.glob(x)
    return filenames


def has_internal_datafiles(folder: str) -> bool:
    folder = folder or "."
    filenames = get_project_filenames(folder)
    return any([f for f in filenames if "spans" in str(f) and "vendor" not in str(f)])


def peek(iterable):
    try:
        first = next(iterable)
    except Exception:
        return None, None
    return first, itertools.chain([first], iterable)


def normalize_array(items: List[Dict[str, Optional[Any]]]) -> List[Dict]:
    """
        Sorted() doesn't not support values with different types for the same column like None vs str.
        So, we need to cast all None to default value of the type of the column if exist and if all the values are None, we can leave them as None
    >>> normalize_array([{'x': 'hello World'}, {'x': None}])
    [{'x': 'hello World'}, {'x': ''}]
    >>> normalize_array([{'x': 3}, {'x': None}])
    [{'x': 3}, {'x': 0}]
    >>> normalize_array([{'x': {'y': [1,2,3,4]}}, {'x': {'z': "Hello" }}])
    [{'x': {'y': [1, 2, 3, 4]}}, {'x': {'z': 'Hello'}}]
    """
    types: Dict[str, type] = {}
    if len(items) == 0:
        return items

    columns = items[0].keys()
    for column in columns:
        for object in items:
            if object[column] is not None:
                types[column] = type(object[column])
                break

    for object in items:
        for column in columns:
            if object[column] is not None:
                continue

            # If None, we replace it for the default value
            if types.get(column, None):
                object[column] = types[column]()

    return items


def find_file_by_name(
    folder: str,
    name: str,
    verbose: bool = False,
    is_raw: bool = False,
    workspace_lib_paths: Optional[List[Tuple[str, str]]] = None,
    resource: Optional[Dict] = None,
):
    f = Path(folder)
    ds = name + ".datasource"
    if os.path.isfile(os.path.join(folder, ds)):
        return ds, None
    if os.path.isfile(f / "datasources" / ds):
        return ds, None

    pipe = name + ".pipe"
    if os.path.isfile(os.path.join(folder, pipe)):
        return pipe, None

    if os.path.isfile(f / "endpoints" / pipe):
        return pipe, None

    if os.path.isfile(f / "pipes" / pipe):
        return pipe, None

    token = name + ".token"
    if os.path.isfile(f / "tokens" / token):
        return token, None

    # look for the file in subdirectories if it's not found in datasources folder
    if workspace_lib_paths:
        _resource = None
        for wk_name, wk_path in workspace_lib_paths:
            file = None
            if name.startswith(f"{wk_name}."):
                file, _resource = find_file_by_name(
                    wk_path, name.replace(f"{wk_name}.", ""), verbose, is_raw, resource=resource
                )
            if file:
                return file, _resource

    if not is_raw:
        f, raw = find_file_by_name(
            folder,
            name,
            verbose=verbose,
            is_raw=True,
            workspace_lib_paths=workspace_lib_paths,
            resource=resource,
        )
        return f, raw

    # materialized node with DATASOURCE definition
    if resource and "nodes" in resource:
        for node in resource["nodes"]:
            params = node.get("params", {})
            if (
                params.get("type", None) == "materialized"
                and params.get("engine", None)
                and params.get("datasource", None)
            ):
                pipe = resource["resource_name"] + ".pipe"
                pipe_file_exists = (
                    os.path.isfile(os.path.join(folder, pipe))
                    or os.path.isfile(f / "endpoints" / pipe)
                    or os.path.isfile(f / "pipes" / pipe)
                )
                is_target_datasource = params["datasource"] == name
                if pipe_file_exists and is_target_datasource:
                    return pipe, {"resource_name": params.get("datasource")}

    if verbose:
        click.echo(FeedbackManager.warning_file_not_found_inside(name=name, folder=folder))

    return None, None


def get_name_version(ds: str) -> Dict[str, Any]:
    """
    Given a name like "name__dev__v0" returns ['name', 'dev', 'v0']
    >>> get_name_version('dev__name__v0')
    {'name': 'dev__name', 'version': 0}
    >>> get_name_version('name__v0')
    {'name': 'name', 'version': 0}
    >>> get_name_version('dev__name')
    {'name': 'dev__name', 'version': None}
    >>> get_name_version('name')
    {'name': 'name', 'version': None}
    >>> get_name_version('horario__3__pipe')
    {'name': 'horario__3__pipe', 'version': None}
    >>> get_name_version('horario__checker')
    {'name': 'horario__checker', 'version': None}
    >>> get_name_version('dev__horario__checker')
    {'name': 'dev__horario__checker', 'version': None}
    >>> get_name_version('tg__dActividades__v0_pipe_3907')
    {'name': 'tg__dActividades', 'version': 0}
    >>> get_name_version('tg__dActividades__va_pipe_3907')
    {'name': 'tg__dActividades__va_pipe_3907', 'version': None}
    >>> get_name_version('tg__origin_workspace.shared_ds__v3907')
    {'name': 'tg__origin_workspace.shared_ds', 'version': 3907}
    >>> get_name_version('tmph8egtl__')
    {'name': 'tmph8egtl__', 'version': None}
    >>> get_name_version('tmph8egtl__123__')
    {'name': 'tmph8egtl__123__', 'version': None}
    >>> get_name_version('dev__name__v0')
    {'name': 'dev__name', 'version': 0}
    >>> get_name_version('name__v0')
    {'name': 'name', 'version': 0}
    >>> get_name_version('dev__name')
    {'name': 'dev__name', 'version': None}
    >>> get_name_version('name')
    {'name': 'name', 'version': None}
    >>> get_name_version('horario__3__pipe')
    {'name': 'horario__3__pipe', 'version': None}
    >>> get_name_version('horario__checker')
    {'name': 'horario__checker', 'version': None}
    >>> get_name_version('dev__horario__checker')
    {'name': 'dev__horario__checker', 'version': None}
    >>> get_name_version('tg__dActividades__v0_pipe_3907')
    {'name': 'tg__dActividades', 'version': 0}
    >>> get_name_version('tg__origin_workspace.shared_ds__v3907')
    {'name': 'tg__origin_workspace.shared_ds', 'version': 3907}
    >>> get_name_version('tmph8egtl__')
    {'name': 'tmph8egtl__', 'version': None}
    >>> get_name_version('tmph8egtl__123__')
    {'name': 'tmph8egtl__123__', 'version': None}
    """
    tk = ds.rsplit("__", 2)
    if len(tk) == 1:
        return {"name": tk[0], "version": None}
    elif len(tk) == 2:
        if len(tk[1]):
            if tk[1][0] == "v" and re.match("[0-9]+$", tk[1][1:]):
                return {"name": tk[0], "version": int(tk[1][1:])}
            else:
                return {"name": tk[0] + "__" + tk[1], "version": None}
    elif len(tk) == 3 and len(tk[2]):
        if tk[2] == "checker":
            return {"name": tk[0] + "__" + tk[1] + "__" + tk[2], "version": None}
        if tk[2][0] == "v":
            parts = tk[2].split("_")
            try:
                return {"name": tk[0] + "__" + tk[1], "version": int(parts[0][1:])}
            except ValueError:
                return {"name": tk[0] + "__" + tk[1] + "__" + tk[2], "version": None}
        else:
            return {"name": "__".join(tk[0:]), "version": None}

    return {"name": ds, "version": None}


def get_resource_versions(datasources: List[str]):
    """
    return the latest version for all the datasources
    """
    versions = {}
    for x in datasources:
        t = get_name_version(x)
        name = t["name"]
        if t.get("version", None) is not None:
            versions[name] = t["version"]
    return versions


def is_file_a_datasource(filename: str) -> bool:
    extensions = Path(filename).suffixes
    if ".datasource" in extensions:  # Accepts '.datasource' and '.datasource.incl'
        return True

    if ".incl" in extensions:
        lines = []
        with open(filename) as file:
            lines = file.readlines()

        for line in lines:
            trimmed_line = line.strip().lower()
            if trimmed_line.startswith("schema") or trimmed_line.startswith("engine"):
                return True

    return False
