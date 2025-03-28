# Geekbot MCP

![Geekbot MCP Logo](https://img.shields.io/badge/Geekbot-MCP-blue?style=for-the-badge)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Geekbot MCP server acts as a bridge between Anthropic's Claude AI and Geekbot's powerful standup, polls and survey management tools.
Provides access to your Geekbot data and a set of tools to seamlessly use them in your Claude AI conversations.

## Features

- **Standup Information**: Fetch all your standups in Geekbot
- **Report Retrieval**: Get standup reports with filtering options

## Installation

```bash
# Install from PyPI
pip install geekbot-mcp

# Or install from source
git clone https://github.com/yourusername/geekbot-mcp.git
cd geekbot-mcp
pip install -e .
```

## Configuration

Before using Geekbot MCP, you need to set up your Geekbot API key:

```bash
# Add to your environment
export GB_API_KEY="your-geekbot-api-key"

# Or add to .env file
echo "GB_API_KEY=your-geekbot-api-key" > .env
```

You can obtain your Geekbot API key from [here](https://geekbot.com/dashboard/api-webhooks).

## Usage

### Running the Server

```bash
# Start the Geekbot MCP server
geekbot-mcp
```

### Available Tools

#### `fetch_standups`

Retrieves a list of all standups from your Geekbot workspace.

```json
{
  "id": 1234,
  "name": "Daily Standup",
  "schedule": "Weekdays at 10:00 AM",
  "questions": ["What did you do yesterday?", "What will you do today?", "Anything blocking your progress?"]
}
```

#### `fetch_reports`

Fetches standup reports with support for filtering by:
- Standup ID
- User ID
- Date range (after/before)

```json
{
  "id": 5678,
  "standup_id": 1234,
  "user_id": 9012,
  "answers": [
    {"question": "What did you do yesterday?", "answer": "Implemented feature X"},
    {"question": "What will you do today?", "answer": "Working on feature Y"},
    {"question": "Anything blocking your progress?", "answer": "No blockers"}
  ],
  "created_at": "2023-03-28T10:00:00Z"
}
```

## Development

### Setup Development Environment

```bash
git clone
cd geekbot-mcp

# Set up a virtual environment (optional but recommended)
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install with test dependencies
uv pip install -e
```

### Running Tests

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Built on [Anthropic's MCP Protocol](https://github.com/modelcontextprotocol)
- Using [Geekbot API](https://geekbot.com/developers/)
