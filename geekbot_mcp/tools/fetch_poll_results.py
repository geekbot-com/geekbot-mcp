import json

from mcp import types

from geekbot_mcp.gb_api import GeekbotClient
from geekbot_mcp.models import poll_results_from_json_response

fetch_poll_results = types.Tool(
    name="fetch_poll_results",
    description="Retrieves Geekbot poll results. Use this tool to analyze poll results or track progress of polls. This tool is usually used after the `list_polls` tool to get the poll id.",
    inputSchema={
        "type": "object",
        "properties": {
            "poll_id": {
                "type": "integer",
                "description": "ID of the specific standup to fetch reports for. If not provided, reports for all standups will be fetched.",
            },
            "before": {
                "type": "string",
                "description": "Fetch results before this date (format: YYYY-MM-DD). This is not provided unless explicitly asked by the user.",
            },
            "after": {
                "type": "string",
                "description": "Fetch results after this date (format: YYYY-MM-DD). This is not provided unless explicitly asked by the user.",
            },
        },
        "required": ["poll_id"],
    },
)


async def handle_fetch_poll_results(
    gb_client: GeekbotClient,
    poll_id: int,
    before: str | None = None,
    after: str | None = None,
) -> list[types.TextContent]:
    """Fetch poll results from Geekbot

    Args:
        poll_id: int, required, the ID of the poll to fetch results for
        before: str, optional, the date to fetch results before in YYYY-MM-DD format
        after: str, optional, the date to fetch results after in YYYY-MM-DD format
    Returns:
        str: Properly formatted JSON string of poll results
    """
    poll_results = await gb_client.get_poll_results(
        poll_id=poll_id, before=before, after=after
    )
    parsed_poll_results = poll_results_from_json_response(poll_results)

    return [
        types.TextContent(
            type="text",
            text=json.dumps(parsed_poll_results.model_dump()),
        )
    ]
