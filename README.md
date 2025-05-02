# Geekbot MCP

[![Geekbot MCP Logo](https://img.shields.io/badge/Geekbot-MCP-blue)](https://geekbot.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/geekbot-mcp.svg)](https://badge.fury.io/py/geekbot-mcp)

**Unlock your Geekbot data within your LLM applications 🚀**

Geekbot MCP (Model Context Protocol) server acts as a bridge, connecting LLM client applications (like Claude) directly to your Geekbot workspace. This allows you to interact with your standups, reports, and team members seamlessly within your conversations using natural language.

## Key Features ✨

- **Access Standup Information**: List all standups in your Geekbot workspace. 📊
- **Retrieve Standup Reports**: Fetch reports with filters for specific standups, users, or date ranges. 📄
- **View Team Members**: Get a list of members you collaborate with in Geekbot. 👥

## Installation 💻

Requires Python 3.10+ and `uv`.

1. **Install uv (if you haven't already):**

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    (See [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/) for more options.)

2. **Install Geekbot MCP:**

    ```bash
    uv tool install geekbot-mcp
    ```

## Upgrading ⬆️

To update to the latest version:

```bash
  uv tool install --upgrade geekbot-mcp
```

## Configuration ⚙️

Connect Geekbot MCP to your LLM (e.g., Claude Desktop):

1. **Get your Geekbot API Key:** Find it in your [Geekbot API/Webhooks settings](https://geekbot.com/dashboard/api-webhooks) 🔑.

2. **Find your `uv` executable path:**

    ```bash
      which uv
    ```

3. **Configure your LLM client application:** Edit your `claude_desktop_config.json` (or equivalent configuration file for other MCP clients) to add Geekbot MCP server
    ```json
    {
      "globalShortcut": "",
      "mcpServers": {
        // Add or update this section
        "geekbot-mcp": {

          "command": "<path-returned-by-which-uv>", // Replace with your actual uv path
          "args": [
            "tool",
            "run",
            "geekbot-mcp"
          ],
          // Environment variables needed by the server
          "env": {
            "GB_API_KEY": "<your-geekbot-api-key>" // Replace with your actual API key
          }
        }
        // ... other MCP servers if any
      }
      // ... other configurations
    }
    ```

    *(Refer to the [MCP Quickstart](https://modelcontextprotocol.io/quickstart/) for more details on client configuration.)*


## Usage 💡

Once configured, your LLM client application will have access to the following tools and prompts to interact with your Geekbot data:

### Tools 🛠️

- `list_standups`

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

- `list_polls`

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

- `fetch_reports`

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

- `list_members`

**Purpose:** Lists all team members you share standups with in your Geekbot workspace.

**Example Prompt:** "Who are the members in my Geekbot workspace?"

**Data Fields Returned:**

- `id`: Unique member identifier.
- `name`: Member's full name.
- `email`: Member's email address.
- `role`: Member's role within Geekbot (e.g., Admin, Member).

- `fetch_poll_results`

**Purpose:** Retrieves specific poll results. Requires a poll id and optionally a date range.

**Example Prompt:** "Hey, what was decided about the new logo in Geekbot polls?"

**Data Fields Returned:**

- `total_results`: Total number of results.
- `question_results`: List of question results.

### Prompts 💬

- `weekly_rollup_report`

**Purpose:** Generates a comprehensive weekly rollup report that summarizes team standup responses, highlights key updates, identifies risks and mitigation strategies, outlines next steps, and tracks upcoming launches.

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
