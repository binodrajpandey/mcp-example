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

## Test

### Option 1 — MCP Inspector (recommended)

```bash
uv run mcp dev server.py
```

Opens a browser UI at `http://localhost:6274`. From there you can:
- **Tools tab**: call `save_note`, `delete_note` with custom inputs
- **Resources tab**: read `notes://list` or `notes://{name}`
- **Prompts tab**: run `summarize_notes` or `brainstorm` with arguments

### Option 2 — CLI with `mcp` client

List all available tools:

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | uv run python server.py
```

## Connect to Claude Code (CLI)

Add the server to your Claude Code session:

```bash
claude mcp add learning-mcp -- uv run --directory /Users/binod/projects/mcp-example python server.py
```

Verify it's connected:

```bash
claude mcp list
```

Once added, Claude Code can call your tools directly in the chat — just ask it to, e.g. _"save a note called 'ideas'"_.

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

## Use programmatically (Python)

Use the `mcp` library to call tools, read resources, and fetch prompts from your own code:

```python
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
import asyncio

async def main():
    server = StdioServerParameters(
        command="uv", args=["run", "python", "server.py"]
    )
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Read a resource
            notes = await session.read_resource("notes://list")
            print(notes)

            # Get a prompt
            prompt = await session.get_prompt("brainstorm", {"topic": "side projects"})
            print(prompt)

asyncio.run(main())
```

To let **Claude (via Anthropic API)** call your tools, add `anthropic[mcp]` to your dependencies and convert the tools:

```python
from anthropic.lib.tools.mcp import async_mcp_tool
import anthropic

client = anthropic.AsyncAnthropic()
tools = [async_mcp_tool(t, session) for t in (await session.list_tools()).tools]

runner = client.beta.messages.tool_runner(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Save a note called ideas"}],
    tools=tools,
)
async for message in runner:
    for block in message.content:
        if hasattr(block, "text"):
            print(block.text)
```

## What's inside

| File | Description |
|------|-------------|
| `server.py` | MCP server with tools, resources, and prompts |
| `pyproject.toml` | Project dependencies |

### Tools (Claude can call these)

| Tool | Description |
|------|-------------|
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
