import json

import mcp.types as types
from jinja2 import Template

from geekbot_mcp.gb_api import GeekbotClient
from geekbot_mcp.models import standup_from_json_response

RESPONSE_TEMPLATE = Template(
    """
    <Standups>
    {% for standup in standups %}
    ***Standup: {{ standup.id }} - {{ standup.name }}***
        id: {{ standup.id }}
        name: {{ standup.name }}
        channel: {{ standup.channel }}
        time: {{ standup.time }}
        timezone: {{ standup.timezone }}
        questions:
            {% for question in standup.questions %}
            - text: {{ question.text }}
            answer_type: {{ question.answer_type }}
            is_random: {{ question.is_random }}
            {% if question.answer_type == "multiple_choice" %}
            answer_choices: {{ question.answer_choices }}
            {% endif %}
            {% endfor %}
    {% endfor %}
    </Standups>
    """
)


list_standups = types.Tool(
    name="list_standups",
    description="Retrieves and displays all Geekbot standups a user has access to, including their complete configuration details such as name, channel, questions, participants, and schedule information. Use this tool to understand the structure of the team and the processes they use track progress and sync.",
    inputSchema={"type": "object", "properties": {}, "required": []},
)


async def handle_list_standups(gb: GeekbotClient) -> list[types.TextContent]:
    """List all standups of a Geekbot user

    Returns:
        str: Properly formatted JSON string of standups list
    """
    standups = await gb.get_standups()
    parsed_standups = [
        standup_from_json_response(s).model_dump()
        for s in standups
        if not s["paused"] and not s["draft"]
    ]
    return [
        types.TextContent(
            type="text",
            text=json.dumps(
                {
                    "number_of_standups": len(parsed_standups),
                    "standups": parsed_standups,
                }
            ),
        )
    ]
