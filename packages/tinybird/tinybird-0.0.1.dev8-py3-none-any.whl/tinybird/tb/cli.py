import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import tinybird.tb.modules.auth
import tinybird.tb.modules.branch
import tinybird.tb.modules.build
import tinybird.tb.modules.cli
import tinybird.tb.modules.common
import tinybird.tb.modules.connection
import tinybird.tb.modules.create
import tinybird.tb.modules.datasource
import tinybird.tb.modules.fmt
import tinybird.tb.modules.job
import tinybird.tb.modules.mock
import tinybird.tb.modules.pipe
import tinybird.tb.modules.tag
import tinybird.tb.modules.test
import tinybird.tb.modules.token
import tinybird.tb.modules.workspace
import tinybird.tb.modules.workspace_members

cli = tinybird.tb.modules.cli.cli

if __name__ == "__main__":
    cli()
