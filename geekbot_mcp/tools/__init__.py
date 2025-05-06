from mcp import types

from geekbot_mcp.gb_api import GeekbotClient
from geekbot_mcp.tools.fetch_poll_results import (
    fetch_poll_results,
    handle_fetch_poll_results,
)
from geekbot_mcp.tools.fetch_reports import fetch_reports, handle_fetch_reports
from geekbot_mcp.tools.list_members import handle_list_members, list_members
from geekbot_mcp.tools.list_polls import handle_list_polls, list_polls
from geekbot_mcp.tools.list_standups import handle_list_standups, list_standups
from geekbot_mcp.tools.post_report import handle_post_report, post_report


def list_tools() -> list[types.Tool]:
    return [
        list_members,
        list_standups,
        fetch_reports,
        post_report,
        list_polls,
        fetch_poll_results,
    ]


async def run_tool(
    gb_client: GeekbotClient,
    name: str,
    arguments: dict[str, str] | None,
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    match name:
        case "list_members":
            return await handle_list_members(gb_client)
        case "list_standups":
            return await handle_list_standups(gb_client)
        case "fetch_reports":
            return await handle_fetch_reports(gb_client, **arguments)
        case "post_report":
            return await handle_post_report(gb_client, **arguments)
        case "list_polls":
            return await handle_list_polls(gb_client)
        case "fetch_poll_results":
            return await handle_fetch_poll_results(gb_client, **arguments)
        case _:
            raise ValueError(f"Tool {name} not found")
