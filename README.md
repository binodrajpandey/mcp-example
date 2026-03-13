# MCP Server Example

A simple MCP (Model Context Protocol) server for learning the core primitives: **Tools**, **Resources**, and **Prompts**.

## Setup

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

### Install

```bash
uv sync
```

## Run

### Dev mode (interactive inspector)

```bash
uv run mcp dev server.py
```

This opens the MCP Inspector in your browser — great for testing tools and resources without Claude Desktop.

### Direct run

```bash
uv run python server.py
```

## Test

### Option 1 — MCP Inspector (recommended)

```bash
uv run mcp dev server.py
```

Opens a browser UI at `http://localhost:5173`. From there you can:
- **Tools tab**: call `add`, `multiply`, `save_note`, `delete_note` with custom inputs
- **Resources tab**: read `notes://list` or `notes://{name}`
- **Prompts tab**: run `summarize_notes` or `brainstorm` with arguments

### Option 2 — CLI with `mcp` client

List all available tools:

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | uv run python server.py
```

Call a tool (e.g. add 3 + 4):

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"add","arguments":{"a":3,"b":4}}}' | uv run python server.py
```

## Connect to Claude Desktop

Add this to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "learning-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/Users/binod/projects/mcp-example",
        "python", "server.py"
      ]
    }
  }
}
```

Then restart Claude Desktop.

## What's inside

| File | Description |
|------|-------------|
| `server.py` | MCP server with tools, resources, and prompts |
| `pyproject.toml` | Project dependencies |

### Tools (Claude can call these)

| Tool | Description |
|------|-------------|
| `add(a, b)` | Add two numbers |
| `multiply(a, b)` | Multiply two numbers |
| `save_note(name, content)` | Save a note |
| `delete_note(name)` | Delete a note |

### Resources (Claude can read these)

| URI | Description |
|-----|-------------|
| `notes://list` | List all saved notes |
| `notes://{name}` | Read a specific note |

### Prompts (reusable templates)

| Prompt | Description |
|--------|-------------|
| `summarize_notes` | Summarize all saved notes |
| `brainstorm(topic)` | Brainstorm ideas on a topic |
