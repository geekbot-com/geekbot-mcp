import asyncio
import logging

from mcp import types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

from geekbot_mcp.gb_api import GeekbotClient
from geekbot_mcp.prompts import get_prompt, list_prompts
from geekbot_mcp.settings import Settings
from geekbot_mcp.tools import list_tools, run_tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("geekbot_mcp")

settings = Settings()
gb_client = GeekbotClient(settings.gb_api_key, version=settings.server_version)
server = Server(name=settings.server_name, version=settings.server_version)


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return list_prompts()


@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    return get_prompt(name, arguments)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return list_tools()


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    return await run_tool(gb_client, name, arguments)


# defining this handler even if we have no resources to avoid "Method not found" error
@server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    return []


async def start_server():
    logger.info("Starting Geekbot MCP server")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=settings.server_name,
                server_version=settings.server_version,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(
                        prompts_changed=True,
                        resources_changed=True,
                        tools_changed=True,
                    ),
                    experimental_capabilities={},
                ),
            ),
        )
    gb_client.close()


def main():
    """Synchronous entry point that runs the main async function."""
    asyncio.run(start_server())
