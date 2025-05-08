import json

import pytest

from geekbot_mcp.models import (
    PollChoiceResult,
    PollQuestionResult,
    PollQuestionResults,
    PollResults,
    Report,
    Standup,
    User,
    poll_results_from_json_response,
    posted_report_from_json_response,
    standup_from_json_response,
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
                                    "id": "UBTDMUC34W",
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

SAMPLE_POLL_RESULT_MULTIPLE_INSTANCES_JSON = """
{
    "total_results": 4,
    "questions": [
        {
            "id": 6148682,
            "text": "What time to drink the coffee man?",
            "results": [
                {
                    "date": "2025-05-05",
                    "answers": [
                        {
                            "text": "12:00",
                            "votes": 0,
                            "percentage": 0,
                            "users": []
                        },
                        {
                            "text": "13:00",
                            "votes": 1,
                            "percentage": 100,
                            "users": [
                                {
                                    "id": "UBTDMUC34W",
                                    "role": "member",
                                    "email": "jd@geekbot.com",
                                    "username": "jd",
                                    "realname": "John Doe",
                                    "profile_img": "https://avatars.slack-edge.com/jd-avatar.png"
                                }
                            ]
                        }
                    ]
                },
                {
                    "date": "2025-05-04",
                    "answers": [
                        {
                            "text": "12:00",
                            "votes": 1,
                            "percentage": 100,
                            "users": [
                                {
                                    "id": "UBTDMUC34W",
                                    "role": "member",
                                    "email": "jd@geekbot.com",
                                    "username": "jd",
                                    "realname": "John Doe",
                                    "profile_img": "https://avatars.slack-edge.com/2018-07-17/401189377223_47ad4aede92c871ad992_32.jpg"
                                }
                            ]
                        },
                        {
                            "text": "13:00",
                            "votes": 0,
                            "percentage": 0,
                            "users": []
                        }
                    ]
                },
                {
                    "date": "2025-05-03",
                    "answers": [
                        {
                            "text": "12:00",
                            "votes": 1,
                            "percentage": 100,
                            "users": [
                                {
                                    "id": "UBTDMUC34W",
                                    "role": "member",
                                    "email": "jd@geekbot.com",
                                    "username": "jd",
                                    "realname": "John Doe",
                                    "profile_img": "https://avatars.slack-edge.com/jd-avatar.png"
                                }
                            ]
                        },
                        {
                            "text": "13:00",
                            "votes": 0,
                            "percentage": 0,
                            "users": []
                        }
                    ]
                },
                {
                    "date": "2025-05-02",
                    "answers": [
                        {
                            "text": "12:00",
                            "votes": 0,
                            "percentage": 0,
                            "users": []
                        },
                        {
                            "text": "13:00",
                            "votes": 1,
                            "percentage": 100,
                            "users": [
                                {
                                    "id": "UBTDMUC34W",
                                    "role": "member",
                                    "email": "jd@geekbot.com",
                                    "username": "jd",
                                    "realname": "John Doe",
                                    "profile_img": "https://avatars.slack-edge.com/jd-avatar.png"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}
"""

POLLS_LIST = """[
    {
        "id": 194050,
        "name": "CoffeeTime",
        "time": "10:00:00",
        "timezone": "Europe/Athens",
        "questions": [
            {
                "id": 6148682,
                "text": "What time to drink the coffee man?",
                "answer_type": "multiple_choice",
                "answer_choices": ["12:00", "13:00"],
                "add_own_options": true,
                "one_option_limit": true,
            }
        ],
        "users": [
            {
                "id": "U011YLX239V",
                "role": "member",
                "email": "myfriend@gmail.com",
                "username": "myfriend",
                "realname": "My Friend",
                "profile_img": "https://secure.gravatar.com/my-friend.png",
            },
            {
                "id": "UBTDMUC34W",
                "role": "member",
                "email": "jd@geekbot.com",
                "username": "jd",
                "realname": "John Doe",
                "profile_img": "https://avatars.slack-edge.com/jd-avatar.png",
            },
        ],
        "recurrence": {
            "type": "custom",
            "repeat": 1,
            "every": "day",
            "day": null,
            "month": null,
        },
        "sync_channel_members": false,
        "sync_channel": null,
        "dm_mode": true,
        "anonymous": false,
        "intro": "Please take a few minutes to answer this poll. :ballot_box_with_ballot: Your participation is appreciated!",
        "creator": {
            "id": "UBTDMUC34W",
            "role": "member",
            "email": "jd@geekbot.com",
            "username": "jd",
            "realname": "John Doe",
            "profile_img": "https://avatars.slack-edge.com/jd-avatar.png",
        },
        "users_total": 2,
        "paused": false,
    },
    {
        "id": 194354,
        "name": "ReplyFast",
        "time": "10:00:00",
        "timezone": "Europe/Athens",
        "questions": [
            {
                "id": 6148812,
                "text": "Which of these times work best for the team meeting?",
                "answer_type": "multiple_choice",
                "answer_choices": ["12:00", "13:00", "16:00", "17:00"],
                "add_own_options": true,
                "one_option_limit": false,
            }
        ],
        "users": [
            {
                "id": "UBTDMUC34W",
                "role": "member",
                "email": "jd@geekbot.com",
                "username": "jd",
                "realname": "John Doe",
                "profile_img": "https://avatars.slack-edge.com/jd-avatar.png",
            }
        ],
        "recurrence": {
            "type": "weekly",
            "repeat": null,
            "every": null,
            "day": {"value": "friday", "order": null},
            "month": null,
        },
        "sync_channel_members": false,
        "sync_channel": null,
        "dm_mode": true,
        "anonymous": false,
        "intro": "Please take a few minutes to answer this poll. :ballot_box_with_ballot: Your participation is appreciated!",
        "creator": {
            "id": "UBTDMUC34W",
            "role": "member",
            "email": "jd@geekbot.com",
            "username": "jd",
            "realname": "John Doe",
            "profile_img": "https://avatars.slack-edge.com/jd-avatar.png",
        },
        "users_total": 1,
        "paused": false,
    },
    {
        "id": 3386416,
        "name": "testpoll",
        "time": "18:23:32",
        "timezone": "Europe/Athens",
        "questions": [
            {
                "id": 5845349,
                "text": "Do you like Geekbot Poll?",
                "answer_type": "yes_no",
                "answer_choices": [
                    "Yes :thumbsup:",
                    "No :thumbsdown:",
                    "I don't know :shrug:",
                ],
                "add_own_options": false,
                "one_option_limit": true,
            }
        ],
        "users": [
            {
                "id": "UBTDMUC34W",
                "role": "member",
                "email": "jd@geekbot.com",
                "username": "jd",
                "realname": "John Doe",
                "profile_img": "https://avatars.slack-edge.com/jd-avatar.png",
            }
        ],
        "recurrence": {
            "type": "once",
            "repeat": null,
            "every": null,
            "day": null,
            "month": null,
        },
        "sync_channel_members": false,
        "sync_channel": null,
        "dm_mode": true,
        "anonymous": false,
        "intro": "Please take a few minutes to answer this poll. :ballot_box_with_ballot: Your participation is appreciated!",
        "creator": {
            "id": "UBTDMUC34W",
            "role": "member",
            "email": "jd@geekbot.com",
            "username": "jd",
            "realname": "John Doe",
            "profile_img": "https://avatars.slack-edge.com/jd-avatar.png",
        },
        "users_total": 1,
        "paused": false,
    },
]
"""

POSTED_REPORT_JSON = """
{
    "id": 27391,
    "slack_ts": null,
    "standup_id": 193911,
    "timestamp": 1746521708,
    "started_at": 1746521708,
    "done_at": 1746521709,
    "broadcasted_at": null,
    "channel": "--testing",
    "member": {
        "id": "UBTDMUC34W",
        "role": "member",
        "username": "jd",
        "realname": "John Doe",
        "profileImg": "https://avatars.slack-edge.com/jd-avatar.png"
    },
    "answers": [
        {
            "id": 179012748,
            "answer": "test",
            "question": "How do you feel today?",
            "question_id": 3143977,
            "color": "EEEEEE",
            "images": []
        },
        {
            "id": 179011249,
            "answer": "test",
            "question": "What have you done since {last_report_date}?",
            "question_id": 6143980,
            "color": "CEF1F3",
            "images": []
        },
        {
            "id": 179018750,
            "answer": "test",
            "question": "What will you do today?",
            "question_id": 6143928,
            "color": "D299EB",
            "images": []
        },
        {
            "id": 179018751,
            "answer": "test",
            "question": "Anything blocking your progress?",
            "question_id": 6143979,
            "color": "FBDADD",
            "images": []
        }
    ]
}
"""

STANDUPS_LIST = """
[
    {
        "id": 1942323270,
        "name": "testconfidentialpaused",
        "time": "16:00:00",
        "wait_time": -1,
        "timezone": "user_local",
        "days": [],
        "channel": null,
        "channel_ready": true,
        "questions": [
            {
                "id": 57508,
                "color": "E5C1F5",
                "text": "Was anything a particular struggle?",
                "schedule": null,
                "answer_type": "text",
                "answer_choices": [],
                "hasAnswers": false,
                "is_random": false,
                "random_texts": [],
                "prefilled_by": null,
                "text_id": 523,
                "preconditions": [],
                "label": "other"
            },
            {
                "id": 506,
                "color": "EEEEEE",
                "text": "If there was one thing I could do to help you, what would it be?",
                "schedule": null,
                "answer_type": "text",
                "answer_choices": [],
                "hasAnswers": false,
                "is_random": false,
                "random_texts": [],
                "prefilled_by": null,
                "text_id": 527,
                "preconditions": [],
                "label": "other"
            },
            {
                "id": 6157509,
                "color": "CEF1F3",
                "text": "On a scale of 1-10, how happy are you with your work-life balance?",
                "schedule": null,
                "answer_type": "numeric",
                "answer_choices": [],
                "hasAnswers": false,
                "is_random": false,
                "random_texts": [],
                "prefilled_by": null,
                "text_id": 121528,
                "preconditions": [],
                "label": "other"
            },
            {
                "id": 57510,
                "color": "FBDADD",
                "text": "Growth-wise, where do you want to focus next month?",
                "schedule": null,
                "answer_type": "text",
                "answer_choices": [],
                "hasAnswers": false,
                "is_random": false,
                "random_texts": [],
                "prefilled_by": null,
                "text_id": 121530,
                "preconditions": [],
                "label": "other"
            },
            {
                "id": 57507,
                "color": "E5C1F5",
                "text": "Anything you'd like to add?",
                "schedule": null,
                "answer_type": "text",
                "answer_choices": [],
                "hasAnswers": false,
                "is_random": false,
                "random_texts": [],
                "prefilled_by": null,
                "text_id": 20887,
                "preconditions": [],
                "label": "other"
            }
        ],
        "users": [
            {
                "id": "U02PV",
                "role": "billing_admin",
                "email": "myfriend@gmail.com",
                "username": "myfriend",
                "realname": "My Friend",
                "profile_img": "https://secure.gravatar.com/my-friend.png"
            }
        ],
        "users_total": 1,
        "webhooks": [],
        "master": "UBTDMUC34W",
        "sync_channel_members": false,
        "sync_channel_ready": false,
        "sync_channel": null,
        "confidential": true,
        "anonymous": false,
        "draft": false,
        "paused": true
    },
    {
        "id": 3221,
        "name": "teststandup",
        "time": "10:00:00",
        "wait_time": -1,
        "timezone": "user_local",
        "days": [],
        "channel": "--test",
        "channel_ready": true,
        "questions": [
            {
                "id": 977,
                "color": "EEEEEE",
                "text": "How do you feel today?",
                "schedule": null,
                "answer_type": "text",
                "answer_choices": [],
                "hasAnswers": true,
                "is_random": false,
                "random_texts": [],
                "prefilled_by": null,
                "text_id": 20725,
                "preconditions": [],
                "label": "sentiment"
            },
            {
                "id": 980,
                "color": "CEF1F3",
                "text": "What have you done since {last_report_date}?",
                "schedule": null,
                "answer_type": "text",
                "answer_choices": [],
                "hasAnswers": true,
                "is_random": false,
                "random_texts": [],
                "prefilled_by": 43978,
                "text_id": 439,
                "preconditions": [],
                "label": "done"
            },
            {
                "id": 3978,
                "color": "D299EB",
                "text": "What will you do today?",
                "schedule": null,
                "answer_type": "text",
                "answer_choices": [],
                "hasAnswers": true,
                "is_random": false,
                "random_texts": [],
                "prefilled_by": null,
                "text_id": 20197,
                "preconditions": [],
                "label": "todo"
            },
            {
                "id": 3979,
                "color": "FBDADD",
                "text": "Anything blocking your progress?",
                "schedule": null,
                "answer_type": "text",
                "answer_choices": [],
                "hasAnswers": true,
                "is_random": false,
                "random_texts": [],
                "prefilled_by": null,
                "text_id": 20868,
                "preconditions": [],
                "label": "obstacles"
            }
        ],
        "users": [
            {
                "id": "UBTDMUC34W",
                "role": "member",
                "email": "jd@geekbot.com",
                "username": "jd",
                "realname": "John Doe",
                "profile_img": "https://avatars.slack-edge.com/jd-avatar.png"
            }
        ],
        "users_total": 1,
        "webhooks": [],
        "master": "UBTDMUC34W",
        "sync_channel_members": false,
        "sync_channel_ready": false,
        "sync_channel": null,
        "confidential": false,
        "anonymous": false,
        "draft": false,
        "paused": false
    }
]
"""


@pytest.fixture
def sample_poll_result_data() -> dict:
    """Provides the sample poll result JSON data as a dictionary."""
    return json.loads(SAMPLE_POLL_RESULT_JSON)


@pytest.fixture
def sample_poll_result_multiple_instances_data() -> dict:
    """Provides the sample poll result JSON data as a dictionary."""
    return json.loads(SAMPLE_POLL_RESULT_MULTIPLE_INSTANCES_JSON)


@pytest.fixture
def polls_list() -> list[dict]:
    """Provides the polls list as a list of dictionaries."""
    return POLLS_LIST


@pytest.fixture
def posted_report_data() -> dict:
    """Provides the posted report JSON data as a dictionary."""
    return json.loads(POSTED_REPORT_JSON)


@pytest.fixture
def standups_list() -> list[dict]:
    """Provides the standups list as a list of dictionaries."""
    return json.loads(STANDUPS_LIST)


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
    assert user1.id == "UBTDMUC34W"
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


def test_poll_results_parsing_multiple_instances(
    sample_poll_result_multiple_instances_data: dict,
):
    """Tests parsing of sample poll results JSON into a PollResults object."""
    parsed_result = poll_results_from_json_response(
        sample_poll_result_multiple_instances_data
    )

    assert isinstance(parsed_result, PollResults)
    assert parsed_result.num_poll_instances == 4
    assert len(parsed_result.question_results) == 1

    question_result: PollQuestionResults = parsed_result.question_results[0]
    assert question_result.question_text == "What time to drink the coffee man?"
    assert len(question_result.results) == 4

    result: PollQuestionResult = question_result.results[0]
    assert result.date == "2025-05-05"
    assert len(result.choices) == 2

    choice1: PollChoiceResult = result.choices[0]
    assert choice1.text == "12:00"
    assert choice1.votes == 0
    assert choice1.percentage == 0.0
    assert len(choice1.users) == 0


def test_posted_report_parsing(posted_report_data: dict):
    """Tests parsing of posted report JSON into a PostedReport object."""
    parsed_result = posted_report_from_json_response(posted_report_data)

    assert isinstance(parsed_result, Report)
    assert parsed_result.id == 27391
    assert parsed_result.standup_id == 193911
    assert parsed_result.reporter.id == "UBTDMUC34W"
    assert parsed_result.reporter.name == "John Doe"
    assert parsed_result.reporter.username == "jd"


def test_standups_list_parsing(standups_list: list[dict]):
    """Tests parsing of standups list JSON into a StandupsList object."""
    standup = standups_list[1]
    parsed_result = standup_from_json_response(standup)

    assert isinstance(parsed_result, Standup)
    assert parsed_result.id == standup["id"]
    assert parsed_result.name == standup["name"]
    assert parsed_result.channel == standup["channel"]
    assert parsed_result.time == standup["time"]
    assert parsed_result.timezone == standup["timezone"]

    confidential_standup = standups_list[0]
    parsed_result = standup_from_json_response(confidential_standup)

    assert isinstance(parsed_result, Standup)
    assert parsed_result.channel == "confidential standup - dm with user"
    assert parsed_result.name == confidential_standup["name"]
    assert parsed_result.time == confidential_standup["time"]
    assert parsed_result.timezone == confidential_standup["timezone"]
