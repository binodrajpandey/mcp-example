"""
Simple MCP Server Example — covers the 3 core primitives:
  - Tools    : functions Claude can call
  - Resources: data Claude can read
  - Prompts  : reusable prompt templates
"""

from mcp.server.fastmcp import FastMCP

# In-memory notes store (pretend database)
notes: dict[str, str] = {}

# Create the server
mcp = FastMCP("Learning MCP Server")


# ── TOOLS ────────────────────────────────────────────────────────────────────
# Tools are functions that Claude can invoke to take actions or compute things.

@mcp.tool()
def save_note(name: str, content: str) -> str:
    """Save a note with a given name."""
    notes[name] = content
    return f"Note '{name}' saved."


@mcp.tool()
def delete_note(name: str) -> str:
    """Delete a note by name."""
    if name not in notes:
        return f"Note '{name}' not found."
    del notes[name]
    return f"Note '{name}' deleted."


# ── RESOURCES ─────────────────────────────────────────────────────────────────
# Resources expose data that Claude can read (like GET endpoints).

@mcp.resource("notes://list")
def list_notes() -> str:
    """List all saved note names."""
    if not notes:
        return "No notes saved yet."
    return "\n".join(f"- {name}" for name in notes)


@mcp.resource("notes://{name}")
def get_note(name: str) -> str:
    """Read a specific note by name."""
    if name not in notes:
        return f"Note '{name}' not found."
    return notes[name]


# ── PROMPTS ───────────────────────────────────────────────────────────────────
# Prompts are reusable templates that surface in Claude's UI as slash commands.

@mcp.prompt()
def summarize_notes() -> str:
    """Ask Claude to summarize all saved notes."""
    all_notes = "\n\n".join(
        f"### {name}\n{content}" for name, content in notes.items()
    )
    if not all_notes:
        return "There are no notes to summarize yet."
    return f"Please summarize the following notes:\n\n{all_notes}"


@mcp.prompt()
def brainstorm(topic: str) -> str:
    """Generate a brainstorming prompt for a given topic."""
    return f"Brainstorm 5 creative ideas about: {topic}"


# ── ENTRY POINT ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run()
