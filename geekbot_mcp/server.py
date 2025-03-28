import json
import logging
import os
from datetime import datetime

from mcp.server.fastmcp import FastMCP

from geekbot_mcp.config import load_api_key
from geekbot_mcp.geekbot_api import GeekbotAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("geekbot_mcp")

gb_api = GeekbotAPI(api_key=load_api_key())

mcp = FastMCP("Geekbot")


@mcp.tool()
async def fetch_standups():
    """Fetch standups list from Geekbot

    Returns:
        str: Properly formatted JSON string of standups list
    """
    async with gb_api as gb_session:
        standups = await gb_session.get_standups()
        return json.dumps(standups, indent=2)


@mcp.tool()
async def fetch_reports(
    standup_id: int = None,
    user_id: int = None,
    after: str = None,
    before: str = None,
):
    """Fetch reports list from Geekbot

    Args:
        standup_id: int, optional, default is None The standup id to fetch reports for
        user_id: int, optional, default is None The user id to fetch reports for
        after: str, optional, default is None The date to fetch reports after in YYYY-MM-DD format
        before: str, optional, default is None The date to fetch reports before in YYYY-MM-DD format
    Returns:
        str: Properly formatted JSON string of reports list
    """
    after_ts = None
    before_ts = None

    if after:
        after_ts = datetime.strptime(after, "%Y-%m-%d").timestamp()

    if before:
        before_ts = datetime.strptime(before, "%Y-%m-%d").timestamp()

    async with gb_api as gb_session:
        reports = await gb_session.get_reports(
            standup_id=standup_id,
            user_id=user_id,
            after=after_ts,
            before=before_ts,
        )
        return json.dumps(reports, indent=2)


def main():
    logger.info("Starting Geekbot MCP server")
    mcp.run()


if __name__ == "__main__":
    main()
