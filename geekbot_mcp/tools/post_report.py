import html

from mcp import types

from geekbot_mcp.gb_api import GeekbotClient
from geekbot_mcp.models import posted_report_from_json_response

post_report = types.Tool(
    name="post_report",
    description="Posts a report to Geekbot. Use this tool to post a report to Geekbot using the context of the conversation. This tool is usually used after the `list_standups` tool to get the standup id and the question ids. If the context of the conversation lacks sufficient information to answer the questions of the standup, the assistant will ask for the missing information. The report should be beautifully formatted. ALWAYS type formatted reporte in the conversation for preview purposes before calling this tool.",
    inputSchema={
        "type": "object",
        "properties": {
            "standup_id": {
                "type": "integer",
                "description": "ID of the specific standup to post the report to.",
            },
            "answers": {
                "type": "object",
                "description": "An object where keys are the string representation of question IDs and values are objects containing the answer text. All questions of the standup must be included in the object.",
                "additionalProperties": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                    },
                    "required": ["text"],
                },
            },
        },
        "required": ["standup_id", "answers"],
    },
)


def parse_answer_text(answer_text: any) -> str:
    """Parse the answer text to ensure it's a string and escape HTML characters."""
    if not isinstance(answer_text, str):
        answer_text = str(answer_text)
    return html.unescape(answer_text)


async def handle_post_report(
    gb_client: GeekbotClient,
    standup_id: int,
    answers: dict[int, dict[str, str]],
) -> list[types.TextContent]:
    """Post a report to Geekbot

    Args:
        standup_id: int,
        answers: dict[int, dict[str, str]],
    Returns:
        str: Properly formatted JSON string of reports list
    """
    processed_answers_for_api = {}
    for question_id, answer_obj in answers.items():
        processed_answers_for_api[question_id] = {
            "text": parse_answer_text(answer_obj["text"])
        }
    report = await gb_client.post_report(
        standup_id=standup_id,
        answers=processed_answers_for_api,
    )
    parsed_report = posted_report_from_json_response(report)
    return [
        types.TextContent(
            type="text",
            text=f"Report posted successfully: {parsed_report.model_dump()}",
        )
    ]
