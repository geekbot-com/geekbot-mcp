import json
import logging
from datetime import datetime

from jinja2 import Template
from mcp.server.fastmcp import FastMCP

from geekbot_mcp.config import load_api_key
from geekbot_mcp.geekbot_api import GeekbotAPI
from geekbot_mcp.models import report_from_json_response, standup_from_json_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("geekbot_mcp")

gb_api = GeekbotAPI(api_key=load_api_key())

mcp = FastMCP("Geekbot")

standups_template = Template(
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

reports_template = Template(
    """
<Reports>
{% for report in reports %}
***Report: {{ report.id }} - {{ report.standup_id }}***
id: {{ report.id }}
reporter_name: {{ report.reporter.name }} | @{{ report.reporter.username }}
reporter_id: {{ report.reporter.id }}
standup_id: {{ report.standup_id }}
created_at: {{ report.created_at }}
content:
{{ report.content }}
{% endfor %}
</Reports>
"""
)


@mcp.tool()
async def fetch_standups():
    """Fetch standups list from Geekbot

    Returns:
        str: Properly formatted JSON string of standups list
    """
    async with gb_api as gb_session:
        standups = await gb_session.get_standups()
        parsed_standups = [standup_from_json_response(s) for s in standups]
        return standups_template.render(standups=parsed_standups)


@mcp.tool()
async def fetch_reports(
    standup_id: int = None,
    user_id: int = None,
    after: str = None,
    before: str = None,
):
    """Fetch reports list from Geekbot

    Args:
        standup_id: int, optional, default is None The standup id to fetch reports for
        user_id: int, optional, default is None The user id to fetch reports for
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

    async with gb_api as gb_session:
        reports = await gb_session.get_reports(
            standup_id=standup_id,
            user_id=user_id,
            after=after_ts,
            before=before_ts,
        )
        parsed_reports = [report_from_json_response(r) for r in reports]
        return reports_template.render(reports=parsed_reports)


def main():
    logger.info("Starting Geekbot MCP server")
    mcp.run()


if __name__ == "__main__":
    main()
