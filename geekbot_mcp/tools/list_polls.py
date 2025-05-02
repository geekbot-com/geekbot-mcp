import json

import mcp.types as types
from jinja2 import Template

from geekbot_mcp.gb_api import GeekbotClient
from geekbot_mcp.models import poll_from_json_response

RESPONSE_TEMPLATE = Template(
    """
    <Polls>
    {% for poll in polls %}
    ***Poll: {{ poll.id }} - {{ poll.name }}***
        id: {{ poll.id }}
        name: {{ poll.name }}
        time: {{ poll.time }}
        timezone: {{ poll.timezone }}
        questions:
            {% for question in poll.questions %}
            - text: {{ question.text }}
            answer_type: {{ question.answer_type }}
            is_random: {{ question.is_random }}
            answer_choices: {{ question.answer_choices }}
            {% endfor %}
    {% endfor %}
    </Polls>
    """
)


list_polls = types.Tool(
    name="list_polls",
    description="Retrieves and displays all Geekbot polls a user has access to, including their complete configuration details such as name, time, timezone, questions, participants, recurrence, anonymous, and creator.",
    inputSchema={"type": "object", "properties": {}, "required": []},
)


async def handle_list_polls(gb: GeekbotClient) -> list[types.TextContent]:
    """List all polls of a Geekbot user

    Returns:
        str: Properly formatted JSON string of polls list
    """
    polls = await gb.get_polls()
    parsed_polls = [poll_from_json_response(p).model_dump() for p in polls]
    return [
        types.TextContent(
            type="text",
            text=json.dumps(
                {
                    "number_of_polls": len(parsed_polls),
                    "polls": parsed_polls,
                }
            ),
        )
    ]
