import os
from typing import Optional

import click

from tinybird.feedback_manager import FeedbackManager
from tinybird.sql_template import get_template_and_variables, render_sql_template
from tinybird.tb.modules.datafile.common import (
    Datafile,
    format_filename,
    parse,
)
from tinybird.tb.modules.datafile.exceptions import IncludeFileNotFoundException, ParseException
from tinybird.tornado_template import UnClosedIfError


def parse_pipe(
    filename: str,
    replace_includes: bool = True,
    content: Optional[str] = None,
    skip_eval: bool = False,
    hide_folders: bool = False,
) -> Datafile:
    basepath = ""
    if not content:
        with open(filename) as file:
            s = file.read()
        basepath = os.path.dirname(filename)
    else:
        s = content

    filename = format_filename(filename, hide_folders)
    try:
        sql = ""
        doc = parse(s, basepath=basepath, replace_includes=replace_includes, skip_eval=skip_eval)
        for node in doc.nodes:
            sql = node.get("sql", "")
            if sql.strip()[0] == "%":
                sql, _, variable_warnings = render_sql_template(sql[1:], test_mode=True, name=node["name"])
                doc.warnings = variable_warnings
            # it'll fail with a ModuleNotFoundError when the toolset is not available but it returns the parsed doc
            from tinybird.sql_toolset import format_sql as toolset_format_sql

            toolset_format_sql(sql)
    except ParseException as e:
        raise click.ClickException(
            FeedbackManager.error_parsing_file(
                filename=filename, lineno=e.lineno, error=f"{str(e)} + SQL(parse exception): {sql}"
            )
        )
    except ValueError as e:
        t, template_variables, _ = get_template_and_variables(sql, name=node["name"])

        if sql.strip()[0] != "%" and len(template_variables) > 0:
            raise click.ClickException(FeedbackManager.error_template_start(filename=filename))
        raise click.ClickException(
            FeedbackManager.error_parsing_file(
                filename=filename, lineno="", error=f"{str(e)} + SQL(value error): {sql}"
            )
        )
    except UnClosedIfError as e:
        raise click.ClickException(
            FeedbackManager.error_parsing_node_with_unclosed_if(node=e.node, pipe=filename, lineno=e.lineno, sql=e.sql)
        )
    except IncludeFileNotFoundException as e:
        raise click.ClickException(FeedbackManager.error_not_found_include(filename=e, lineno=e.lineno))
    except ModuleNotFoundError:
        pass
    return doc
