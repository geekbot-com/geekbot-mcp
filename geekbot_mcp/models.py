from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str
    username: str
    email: str
    role: str

    class Config:
        frozen = True

    def __hash__(self):
        return hash(self.id)


class Reporter(BaseModel):
    id: str
    name: str
    username: str

    class Config:
        frozen = True

    def __hash__(self):
        return hash(self.id)


class Question(BaseModel):
    text: str
    answer_type: str
    answer_choices: list[str]
    is_random: bool


class Standup(BaseModel):
    id: int
    name: str
    channel: str
    time: str
    timezone: str
    questions: list[Question]
    participants: list[User]
    owner_id: str

    class Config:
        frozen = True

    def __hash__(self):
        return hash(self.id)


class Poll(BaseModel):
    id: int
    name: str
    time: str
    timezone: str
    questions: list[Question]
    participants: list[User]
    creator: User

    class Config:
        frozen = True

    def __hash__(self):
        return hash(self.id)


class Report(BaseModel):
    id: int
    standup_id: int
    created_at: str
    reporter: Reporter
    content: str

    class Config:
        frozen = True

    def __hash__(self):
        return hash(self.id)


def user_from_json_response(u_res: dict) -> User:
    return User(
        id=u_res["id"],
        name=u_res["realname"],
        username=u_res["username"],
        email=u_res["email"],
        role=u_res["role"],
    )


def question_from_json_response(q_res: dict) -> Question:
    text = q_res["text"]
    if q_res["is_random"]:
        text = "random choice from " + ", ".join(q_res["random_texts"])

    return Question(
        text=text,
        answer_type=q_res["answer_type"],
        answer_choices=q_res["answer_choices"],
        is_random=q_res["is_random"],
    )


def poll_question_from_json_response(q_res: dict) -> Question:
    return Question(
        text=q_res["text"],
        answer_type=q_res["answer_type"],
        answer_choices=q_res["answer_choices"],
        is_random=False,
    )


def standup_from_json_response(s_res: dict) -> Standup:
    return Standup(
        id=s_res["id"],
        name=s_res["name"],
        channel=s_res["channel"],
        time=s_res["time"],
        timezone=s_res["timezone"],
        questions=[question_from_json_response(q) for q in s_res["questions"]],
        participants=[user_from_json_response(p) for p in s_res["users"]],
        owner_id=s_res["master"],
    )


def poll_from_json_response(p_res: dict) -> Poll:
    return Poll(
        id=p_res["id"],
        name=p_res["name"],
        time=p_res["time"],
        timezone=p_res["timezone"],
        questions=[poll_question_from_json_response(q) for q in p_res["questions"]],
        participants=[user_from_json_response(p) for p in p_res["users"]],
        creator=user_from_json_response(p_res["creator"]),
    )


def reporter_from_json_response(r_res: dict) -> Reporter:
    return Reporter(
        id=r_res["id"],
        name=r_res["realname"],
        username=r_res["username"],
    )


def content_from_json_response(c_res: dict) -> str:
    items = []
    for q in c_res:
        items.append(f"q: {q['question']}\na: {q['answer']}\n")

    return "\n".join(items)


def report_from_json_response(r_res: dict) -> Report:
    return Report(
        id=r_res["id"],
        standup_id=r_res["standup_id"],
        created_at=datetime.fromtimestamp(r_res["timestamp"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        reporter=reporter_from_json_response(r_res["member"]),
        content=content_from_json_response(r_res["questions"]),
    )
