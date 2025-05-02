import json
from datetime import datetime

from mcp import types

from geekbot_mcp.gb_api import GeekbotClient
from geekbot_mcp.models import report_from_json_response

fetch_reports = types.Tool(
    name="fetch_reports",
    description="Retrieves Geekbot standup reports. Use this tool to analyze team updates or updates from specific colleagues, track progress, or compile summaries of standup activities. This tool is usually used after the `list_standups` tool.",
    inputSchema={
        "type": "object",
        "properties": {
            "standup_id": {
                "type": "integer",
                "description": "ID of the specific standup to fetch reports for. If not provided, reports for all standups will be fetched.",
            },
            "user_id": {
                "type": "string",
                "description": "ID of the specific user to fetch reports for. If not provided, reports for all members will be fetched.",
            },
            "after": {
                "type": "string",
                "description": "Fetch reports after this date (format: YYYY-MM-DD)",
            },
            "before": {
                "type": "string",
                "description": "Fetch reports before this date (format: YYYY-MM-DD)",
            },
        },
        "required": [],
    },
)


async def handle_fetch_reports(
    gb_client: GeekbotClient,
    standup_id: int | None = None,
    user_id: int | None = None,
    after: str | None = None,
    before: str | None = None,
) -> list[types.TextContent]:
    """Fetch reports list from Geekbot

    Args:
        standup_id: int, optional, default is None and means for all standups. The standup id to fetch reports for
        user_id: int, optional, default is None and means for all members. The user id to fetch reports for
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

    reports = await gb_client.get_reports(
        standup_id=standup_id,
        user_id=user_id,
        after=after_ts,
        before=before_ts,
    )
    parsed_reports = [report_from_json_response(r) for r in reports]
    parsed_reports_json = [r.model_dump() for r in parsed_reports]
    unique_reporters = list({r.reporter for r in parsed_reports})
    return [
        types.TextContent(
            type="text",
            text=json.dumps(
                {
                    "number_of_reports": len(parsed_reports),
                    "reports": parsed_reports_json,
                    "number_of_reporters": len(unique_reporters),
                }
            ),
        )
    ]
