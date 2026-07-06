# Geekbot MCP

> [!IMPORTANT]
> ## ⚠️ This project is no longer maintained and has been archived
>
> Development of this local, self-installed MCP server has stopped. We've moved to a **remote, OAuth-authenticated Geekbot MCP server** that requires no local install, no API key in a config file, and stays up to date automatically.
>
> **What to use instead:**
>
> - **Geekbot Remote MCP Server:** Connect your AI assistant to Geekbot via the remote MCP server. → [Setup guide](https://help.geekbot.com/en/articles/15692639-geekbot-mcp-server)
> - **Geekbot CLI & AI Skill:** Submit reports, analyse past responses, and manage standups and polls from your terminal or AI coding agent (Claude Code, Cursor, Windsurf, Copilot). → [github.com/geekbot-com/geekbot-cli](https://github.com/geekbot-com/geekbot-cli)
>
> This repository remains available, read-only, for reference. The instructions below are kept for historical purposes and are no longer supported.

[![Geekbot MCP Logo](https://img.shields.io/badge/Geekbot-MCP-blue)](https://geekbot.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/geekbot-mcp.svg)](https://badge.fury.io/py/geekbot-mcp)
[![smithery badge](https://smithery.ai/badge/@geekbot-com/geekbot-mcp)](https://smithery.ai/server/@geekbot-com/geekbot-mcp)
[![Verified on MseeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/0d0b7e7a-b902-4488-9d0a-eca75559f02b)

**Unlock your Geekbot data within your LLM applications 🚀**

Geekbot MCP (Model Context Protocol) server acts as a bridge, connecting LLM client applications (like Claude, Cursor, Windsurf, etc.) directly to your Geekbot workspace. This allows you to interact with your standups, reports, and team members seamlessly within your conversations using natural language.

## Key Features ✨

- **Access Standup and Poll Information**: List all standups and polls in your Geekbot workspace. 📊
- **Retrieve Standup Reports and Poll Results**: Fetch reports and poll results with filters for specific standups, users, or date ranges. 📄
- **View Team Members**: Get a list of members you collaborate with in Geekbot. 👥
- **Post Standup Reports**: Post a standup report to Geekbot. 📝

Check the video:

  [![Alt text](https://img.youtube.com/vi/6ZUlX6GByw4/0.jpg)](https://www.youtube.com/watch?v=6ZUlX6GByw4)

## Installation 💻

### Manual Installation

Requires Python 3.10+ and `uv`.

1. **Install Python 3.10+ (if you haven't already):**

    - **macOS:**

      ```bash
      brew install python@3.10
      ```

      See [Homebrew Python installation guide](https://docs.brew.sh/Homebrew-and-Python) for more details.

    - **Ubuntu/Debian:**

      ```bash
      sudo apt update
      sudo apt install python3.10
      ```

    - **Windows:**
      Download and install from [Python.org](https://www.python.org/downloads/windows/).

      See [Windows Python installation guide](https://docs.python.org/3/using/windows.html) for more details.

2. **Install uv (if you haven't already):**

    - **macOS/Linux:**
    In your terminal, run the following command:

      ```bash
      curl -LsSf https://astral.sh/uv/install.sh | sh
      ```

    - **Windows:**
      In your PowerShell, run the following command:

      ```powershell
      powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
      ```

    (See [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/) for more options.)

3. **Install/Upgrade Geekbot MCP:**

    - **macOS/Linux:**
      In your terminal, run the following command:

      ```bash
      uv tool install --upgrade geekbot-mcp
      ```

    - **Windows:**
      In your PowerShell, run the following command:

      ```powershell
      uv tool install --upgrade geekbot-mcp
      ```


## Configuration ⚙️

After installling Geekbot MCP, you can connect it to your an LLM client desktop application (e.g., Claude Desktop, Cursor, Windsurf, etc.):

1. **Get your Geekbot API Key:** Find it in your [Geekbot API/Webhooks settings](https://geekbot.com/dashboard/api-webhooks) 🔑.

2. **Find your `uv` executable path:**

- **Linux/macOS:**
  In your terminal, run the following command:

  ```bash
    which uv
  ```

- **Windows:**
  In your PowerShell, run the following command:

  ```powershell
    (Get-Command uv | Select-Object -ExpandProperty Path) -replace '\\', '\\'
  ```

3. **Configure your LLM client desktop application:**
Each LLM client that supports MCP provides a configuration file that you can edit to add Geekbot MCP server.
- [Claude Desktop](https://modelcontextprotocol.io/quickstart/user)
- [Cursor](https://docs.cursor.com/context/model-context-protocol)
- [Windsurf](https://docs.windsurf.com/windsurf/cascade/mcp)

If you are using a different LLM client, please refer to the documentation of your client to learn how to configure the MCP server.

After you locate the configuration file, edit it to add Geekbot MCP server:

```json
    {
      "mcpServers": {
        "geekbot-mcp": {
          "command": "UV-PATH",
          "args": [
            "tool",
            "run",
            "geekbot-mcp"
          ],
          "env": {
            "GB_API_KEY": "YOUR-API-KEY"
          }
        }
      }
    }
```

Make sure to replace:
  - `UV-PATH` with the path to your `uv` executable from step 2
  - `YOUR-API-KEY` with your Geekbot API key from step 1

## Usage 💡

Once configured, your LLM client application will have access to the following tools and prompts to interact with your Geekbot data:

### Tools 🛠️

**`list_standups`**

**Purpose:** Lists all the standups accessible via your API key. Useful for getting an overview or finding a specific standup ID.

**Example Prompt:** "Hey, can you list my Geekbot standups?"

**Data Fields Returned:**

- `id`: Unique standup identifier.
- `name`: Name of the standup.
- `channel`: Associated communication channel (e.g., Slack channel).
- `time`: Scheduled time for the standup report.
- `timezone`: Timezone for the scheduled time.
- `questions`: List of questions asked in the standup.
- `participants`: List of users participating in the standup.
- `owner_id`: ID of the standup owner.
- `confidential`: Whether the standup is confidential.
- `anonymous`: Whether the standup is anonymous.

**`list_polls`**

**Purpose:** Lists all the polls accessible via your API key. Useful for getting an overview or finding a specific poll ID.

**Example Prompt:** "Hey, can you list my Geekbot polls?"

**Data Fields Returned:**

- `id`: Unique poll identifier.
- `name`: Name of the poll.
- `time`: Scheduled time for the poll.
- `timezone`: Timezone for the scheduled time.
- `questions`: List of questions asked in the poll.
- `participants`: List of users participating in the poll.
- `creator`: The poll creator.

`fetch_reports`

**Purpose:** Retrieves specific standup reports. You can filter by standup, user, and date range.

**Example Prompts:**

- "Fetch the reports for submitted yesterday in the Retrospective."
- "Show me reports from user John Doe for the 'Weekly Sync' standup."
- "Get all reports submitted to the Daily Standup standup after June 1st, 2024."

**Available Filters:**

- `standup_id`: Filter by a specific standup ID.
- `user_id`: Filter reports by a specific user ID.
- `after`: Retrieve reports submitted after this date (YYYY-MM-DD) 🗓️.
- `before`: Retrieve reports submitted before this date (YYYY-MM-DD) 🗓️.

**Data Fields Returned:**

- `id`: Unique report identifier.
- `reporter_name`: Name of the user who submitted the report.
- `reporter_id`: ID of the user who submitted the report.
- `standup_id`: ID of the standup the report belongs to.
- `created_at`: Timestamp when the report was submitted.
- `content`: The actual answers/content of the report.

**`post_report`**

**Purpose:** Posts a report to Geekbot.

**Example Prompt:** "Hey, can you post the report for the Daily Standup standup?"

**Data Fields Returned:**

- `id`: Unique report identifier.
- `reporter_name`: Name of the user who submitted the report.
- `reporter_id`: ID of the user who submitted the report.
- `standup_id`: ID of the standup the report belongs to.
- `created_at`: Timestamp when the report was submitted.
- `content`: The actual answers/content of the report.

**`list_members`**

**Purpose:** Lists all team members you share standups with in your Geekbot workspace.

**Example Prompt:** "Who are the members in my Geekbot workspace?"

**Data Fields Returned:**

- `id`: Unique member identifier.
- `name`: Member's full name.
- `email`: Member's email address.
- `role`: Member's role within Geekbot (e.g., Admin, Member).

**`fetch_poll_results`**

**Purpose:** Retrieves specific poll results. Requires a poll id and optionally a date range.

**Example Prompt:** "Hey, what was decided about the new logo in Geekbot polls?"

**Data Fields Returned:**

- `total_results`: Total number of results.
- `question_results`: List of question results.

### Prompts 💬

**`weekly_rollup_report`**

**Purpose:** Generates a comprehensive weekly rollup report that summarizes team standup responses, highlights key updates, identifies risks and mitigation strategies, outlines next steps, and tracks upcoming launches.


### Tips 💡

- **Review Tool Usage**: Make the agent ask for your explicit approval for each tool action and not allow automatic tool calls. This safety feature ensures you maintain control over sensitive operations, particularly when posting reports to Geekbot. You'll be prompted to review and approve each tool call before execution, helping prevent unintended data submissions.

- **Ask for preview**: Before posting a report, ask the agent to preview the report and not actually post it. This will give you a chance to review the report and make sure it is correct or make changes to it before posting it to Geekbot.

- **Limit the volume of retrieved data**: If you are using the `fetch_reports` tool, limit the date range to a reasonable period. This will help prevent the agent from retrieving a large amount of data and causing performance issues. Have in mind that the agent will apply limits in the number of reports it can retrieve.

**Arguments:**

- `standup_id`: ID of the standup to include in the rollup report.

## Development 🧑‍💻

Interested in contributing or running the server locally?

### Setup Development Environment

```bash
# 1. Clone the repository
git clone https://github.com/geekbot-com/geekbot-mcp.git
cd geekbot-mcp

# 2. Install uv (if needed)
# curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Create a virtual environment and install dependencies
uv sync
```

### Running Tests ✅

```bash
# Ensure dependencies are installed (uv sync)
pytest
```

## Contributing 🤝

Contributions are welcome! Please fork the repository and submit a Pull Request with your changes.

## License 📜

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements 🙏

- Built upon the [Anthropic Model Context Protocol](https://github.com/modelcontextprotocol) framework.
- Leverages the official [Geekbot API](https://geekbot.com/developers/).
