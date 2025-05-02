import json

import pytest

from geekbot_mcp.models import (
    PollChoiceResult,
    PollQuestionResult,
    PollQuestionResults,
    PollResults,
    User,
    poll_results_from_json_response,
)

SAMPLE_POLL_RESULT_JSON = """
{
    "total_results": 1,
    "questions": [
        {
            "id": 1,
            "text": "Do you like Geekbot Poll?",
            "results": [
                {
                    "date": "2025-01-20",
                    "answers": [
                        {
                            "text": "Yes :thumbsup:",
                            "votes": 1,
                            "percentage": 100,
                            "users": [
                                {
                                    "id": "UBTDMUC4W",
                                    "role": "member",
                                    "email": "jd@geekbot.com",
                                    "username": "jd",
                                    "realname": "John Doe",
                                    "profile_img": "https://avatars.slack-edge.com/jd-avatar.png"
                                }
                            ]
                        },
                        {
                            "text": "No :thumbsdown:",
                            "votes": 0,
                            "percentage": 0,
                            "users": []
                        },
                        {
                            "text": "I don't know :shrug:",
                            "votes": 0,
                            "percentage": 0,
                            "users": []
                        }
                    ]
                }
            ]
        }
    ]
}
"""


@pytest.fixture
def sample_poll_result_data() -> dict:
    """Provides the sample poll result JSON data as a dictionary."""
    return json.loads(SAMPLE_POLL_RESULT_JSON)


def test_poll_results_parsing(sample_poll_result_data: dict):
    """Tests parsing of sample poll results JSON into a PollResults object."""
    parsed_result = poll_results_from_json_response(sample_poll_result_data)

    assert isinstance(parsed_result, PollResults)
    assert parsed_result.num_poll_instances == 1
    assert len(parsed_result.question_results) == 1

    question_result: PollQuestionResults = parsed_result.question_results[0]
    assert question_result.question_text == "Do you like Geekbot Poll?"
    assert len(question_result.results) == 1

    result: PollQuestionResult = question_result.results[0]
    assert result.date == "2025-01-20"
    assert len(result.choices) == 3

    choice1: PollChoiceResult = result.choices[0]
    assert choice1.text == "Yes :thumbsup:"
    assert choice1.votes == 1
    assert choice1.percentage == 100.0
    assert len(choice1.users) == 1

    user1: User = choice1.users[0]
    assert isinstance(user1, User)
    assert user1.id == "UBTDMUC4W"
    assert user1.name == "John Doe"
    assert user1.username == "jd"
    assert user1.email == "jd@geekbot.com"
    assert user1.role == "member"

    choice2: PollChoiceResult = result.choices[1]
    assert choice2.text == "No :thumbsdown:"
    assert choice2.votes == 0
    assert choice2.percentage == 0.0
    assert len(choice2.users) == 0

    choice3: PollChoiceResult = result.choices[2]
    assert choice3.text == "I don't know :shrug:"
    assert choice3.votes == 0
    assert choice3.percentage == 0.0
    assert len(choice3.users) == 0
