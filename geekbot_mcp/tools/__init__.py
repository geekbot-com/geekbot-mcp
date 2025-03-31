from mcp import types

from geekbot_mcp.gb_api import GeekbotClient
from geekbot_mcp.tools.fetch_reports import fetch_reports, handle_fetch_reports
from geekbot_mcp.tools.list_members import handle_list_members, list_members
from geekbot_mcp.tools.list_standups import handle_list_standups, list_standups


def list_tools() -> list[types.Tool]:
    return [fetch_reports, list_standups, list_members]


async def run_tool(
    gb_client: GeekbotClient,
    name: str,
    arguments: dict[str, str] | None,
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    match name:
        case "fetch_reports":
            return await handle_fetch_reports(gb_client, **arguments)
        case "list_standups":
            return await handle_list_standups(gb_client)
        case "list_members":
            return await handle_list_members(gb_client)
        case _:
            raise ValueError(f"Tool {name} not found")
