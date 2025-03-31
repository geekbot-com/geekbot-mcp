from mcp import types

from geekbot_mcp.prompts.weekly_rollup_report import (
    get_weekly_rollup_prompt,
    weekly_rollup_report_prompt,
)


def list_prompts() -> list[types.Prompt]:
    return [weekly_rollup_report_prompt]


def get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    match name:
        case "weekly_rollup_report":
            return get_weekly_rollup_prompt(arguments)
        case _:
            raise ValueError(f"Prompt {name} not found")
