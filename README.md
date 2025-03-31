# Geekbot MCP

![Geekbot MCP Logo](https://img.shields.io/badge/Geekbot-MCP-blue)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Geekbot MCP server acts as a bridge between Anthropic's Claude AI and Geekbot's powerful standup, polls and survey management tools.
Provides access to your Geekbot data and a set of tools to seamlessly use them in your Claude AI conversations.

## Features

- **Standup Information**: Fetch all your standups in Geekbot
- **Report Retrieval**: Get standup reports with filtering options
- **Members Information**: Fetch all your team members in Geekbot

## Installation

Download the uv package manager

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Further instructions can be found [here](https://docs.astral.sh/uv/getting-started/installation/)

```bash
git clone https://github.com/geekbot-com/geekbot-mcp.git
cd geekbot-mcp
uv tool install --editable .
```

## Configuration

Before using Geekbot MCP, you need to set up your Geekbot API key:

You can obtain your Geekbot API key from [here](https://geekbot.com/dashboard/api-webhooks).

Configure the mcp server in your claude_desktop_config.json

```json
{
  "globalShortcut": "",
  "mcpServers": {
    "geekbot-mcp": {
      "command": "<path-to-your-uv-executable>",
      "args": [
        "tool",
        "run",
        "geekbot-mcp"
      ],
      "env": {
        "GB_API_KEY": "<your-geekbot-api-key>"
      }
    }
  }
}
```

To find the path to your uv executable, you can run `which uv` in your terminal.
You can find more information about the configuration [here](https://modelcontextprotocol.io/quickstart/)

### Available Tools

#### `list_standups`

Retrieves a list of all standups from your Geekbot workspace.

The response is in a plain text format.

```text
<Standups>
***Standup: 1 - Infrastructure Changelog***
id: 1
name: Infrastructure Changelog
channel: team-infrastructure
time: 10:00:00
timezone: user_local
questions:

- text: What changed in the infrastructure today?
  answer_type: text
  is_random: False



***Standup: 2 - Meeting Agenda (TOC Beta)***
id: 2
name: Meeting Agenda (TOC Beta)
channel: meeting-notes
time: 10:00:00
timezone: user_local
questions:

- text: What should we discuss in this meeting?
  answer_type: text
  is_random: False

</Standups>
```

#### `fetch_reports`

Fetches standup reports with support for filtering by:

- standup_id
- user_id
- after
- before

The response is in a plain text format.

```text
<Reports>
***Report: 1 - 1***
id: 208367845
reporter_name: John Doe | @john_doe
reporter_id: U1234
standup_id: 1
created_at: 2025-03-27 13:52:59
content:
q: What have you done since your last report?
a: • Plan work for the next week
   • Worked on the new feature

q: What will you do today?
a: • Plan work for the next week
   • Worked on the new feature

q: How do you feel today?
a: I am fine.
```

#### `list_members`

Retrieves a list of all members from your Geekbot workspace.


## Development

### Setup Development Environment

```bash
git clone https://github.com/geekbot-com/geekbot-mcp.git
cd geekbot-mcp

uv venv
source .venv/bin/activate

uv pip install -e
```

### Running Tests

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License

## Acknowledgements

- Built on [Anthropic's MCP Protocol](https://github.com/modelcontextprotocol)
- Using [Geekbot API](https://geekbot.com/developers/)
