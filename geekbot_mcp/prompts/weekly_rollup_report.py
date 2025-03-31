from jinja2 import Template
from mcp import types

WEEKLY_ROLLUP_REPORT_PROMPT_TEMPLATE = Template(
    """
    <instructions>
    You are a Product Manager who's an expert at analyzing complex product decisions and providing well-reasoned recommendations.

    Your task is to guide the decision-making process through thoughtful discussion and document the final decision & also provide status updates for your team in the form of Roll-up Reports.

    You also act as a Scrum Master for your team in order to provide a <Weekly Update Rollup Report> doc to your C-level team for the weekly progress of the team.

    Your main tool to do so is use the Geekbot AI engine. A new feature is about "AI Summarization of Daily Standups responses per week".
    ================================================================
    Here is the format you should use for the final document:

    <Weekly Update Rollup Report>
    <doc_format>
    <context>
    1) a TLDR section summarizing the results of your team's week reports
    2) #01: Updates
    3) #02: Risks and Mitigation
    4) #03: Next steps
    5) #04: Upcoming launches
    </context>

    <Updates>
    [Recommended option with 3-5 bullets highlighting the recurring items present in more than 1 Standup reports.
    </Updates>

    <Risks and Mitigation>
    [List up to 3 Risks. For each option, have a bullet about the risks and any mitigations. Each bullet should have 2-3 sentences]]
    </Risks and Mitigation>

    <next_steps>
    [Suggest specific actions to implement the recommendation]
    </next_steps>

    </decision_doc_format>
    Please follow these instructions carefully:
    1. Ask for information about the following all at once:
    1) a TLDR section (summarizing the results of your team's week reports)
    2) #01: Updates
    3) #02: Risks, Blockers and Mitigation
    4) #03: Next steps
    5) #04: Upcoming launches
    ================================================================

    Please keep each bullet short & to the point.
    {% if standup_id != None %}
    WORKFLOW:
    1. Resolve the correct `before` and `after` dates for the past week to pass to `fetch_reports` tool
    2. Use the tool `fetch_reports` from geekbot-mcp to get the past week's reports for the standup with standup_id {{ standup_id }} and the resolved before and after dates
    3. Analyze the reports based on the instructions above
    4. Generate the rollup report in the format specified above
    {% else %}
    WORKFLOW:
    1. Resolve the correct `before` and `after` dates for the past week to pass to `fetch_reports` tool
    2. Check if the context contains the standup_ids that the user wants to include in the rollup report
    3. Use the tool `fetch_standups` from geekbot-mcp to to select the standups that the user wants to include in the rollup report
    4. Use the tool `fetch_reports` from geekbot-mcp to get this week's reports. You can use the tool as many times as needed passing the resolved `before` and `after` dates and a `standup_id` from your list of standups
    5. Analyze the reports based on the instructions above
    6. Generate the rollup report in the format specified above
    {% endif %}
    </instructions>
    """
)

weekly_rollup_report_prompt = types.Prompt(
    name="weekly_rollup_report",
    description="Generate a comprehensive weekly rollup report that summarizes team standup responses, highlights key updates, identifies risks and mitigation strategies, outlines next steps, and tracks upcoming launches. The report organizes information in a structured format for executive visibility and team alignment.",
    arguments=[
        types.PromptArgument(
            name="standup_id",
            description="The ID of the standup to include in the rollup report",
            required=False,
        ),
    ],
)


def get_weekly_rollup_prompt(standup_id: int | None = None) -> types.GetPromptResult:
    return types.GetPromptResult(
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=WEEKLY_ROLLUP_REPORT_PROMPT_TEMPLATE.render(
                        standup_id=standup_id
                    ),
                ),
            )
        ]
    )
