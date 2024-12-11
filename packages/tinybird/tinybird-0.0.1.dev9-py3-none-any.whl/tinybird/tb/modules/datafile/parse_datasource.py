import os
from typing import Optional

import click

from tinybird.feedback_manager import FeedbackManager
from tinybird.tb.modules.datafile.common import (
    Datafile,
    format_filename,
    parse,
)
from tinybird.tb.modules.datafile.exceptions import ParseException


def parse_datasource(
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
        doc = parse(s, "default", basepath, replace_includes=replace_includes, skip_eval=skip_eval)
    except ParseException as e:
        raise click.ClickException(
            FeedbackManager.error_parsing_file(filename=filename, lineno=e.lineno, error=e)
        ) from None

    if len(doc.nodes) > 1:
        raise ValueError(f"{filename}: datasources can't have more than one node")

    return doc
