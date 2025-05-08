import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from geekbot_mcp.gb_api import GeekbotClient
from geekbot_mcp.tools.list_standups import handle_list_standups
from geekbot_mcp.tools.post_report import parse_answer_text
from tests.test_models import STANDUPS_LIST


@pytest.fixture
def standups_list() -> list[dict]:
    """Provides the standups list as a list of dictionaries."""
    return json.loads(STANDUPS_LIST)


@pytest.fixture
def mock_geekbot_client(standups_list):
    """Returns a mock GeekbotClient that returns the standups_list fixture for get_standups()."""
    mock_client = MagicMock(spec=GeekbotClient)
    mock_client.get_standups = AsyncMock(return_value=standups_list)
    return mock_client


@pytest.mark.asyncio
async def test_handle_list_standups(mock_geekbot_client):
    res = await handle_list_standups(mock_geekbot_client)
    serialized = json.loads(res[0].text)
    assert mock_geekbot_client.get_standups.called

    assert serialized["number_of_standups"] == 1
    assert serialized["standups"][0]["name"] == "teststandup"


def test_parse_answer_text():
    assert (
        parse_answer_text("This is a test. It's great!")
        == "This is a test. It's great!"
    )

    assert parse_answer_text(123) == "123"

    assert (
        parse_answer_text("&lt;div&gt;Hello &amp;amp; World&lt;/div&gt;")
        == "<div>Hello &amp; World</div>"
    )

    assert (
        parse_answer_text(
            "&lt;p&gt;Less than &amp;lt; and greater than &amp;gt;&lt;/p&gt;"
        )
        == "<p>Less than &lt; and greater than &gt;</p>"
    )
    assert (
        parse_answer_text("'Single quote &amp;apos; and double quote &amp;quot;'")
        == "'Single quote &apos; and double quote &quot;'"
    )

    assert (
        parse_answer_text(
            "The main challenge we&#039;re facing involves Slack API limitations, which are creating some constraints on what we can implement. However, I&#039;m confident we can find creative workarounds for these issues. Nothing we can&#039;t overcome with a bit of innovative thinking!"
        )
        == "The main challenge we're facing involves Slack API limitations, which are creating some constraints on what we can implement. However, I'm confident we can find creative workarounds for these issues. Nothing we can't overcome with a bit of innovative thinking!"
    )
