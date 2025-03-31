import json

import mcp.types as types

from geekbot_mcp.gb_api import GeekbotClient
from geekbot_mcp.models import standup_from_json_response

list_members = types.Tool(
    name="list_members",
    description="Lists all team members participating in the standups and polls of the user. Use this tool to get information about the colleagues of the user",
    inputSchema={"type": "object", "properties": {}, "required": []},
)


async def handle_list_members(gb: GeekbotClient) -> list[types.TextContent]:
    """List all members of participants in the standups and pollsof the user

    Returns:
        str: Properly formatted JSON string of members list
    """
    standups = await gb.get_standups()
    participants = []
    for s in standups:
        standup_obj = standup_from_json_response(s)
        participants.extend(standup_obj.participants)

    unique_participants = list(set(participants))
    unique_participants_json = [p.model_dump() for p in unique_participants]
    return [
        types.TextContent(
            type="text",
            text=json.dumps(
                {
                    "number_of_members": len(unique_participants),
                    "members": unique_participants_json,
                }
            ),
        )
    ]
