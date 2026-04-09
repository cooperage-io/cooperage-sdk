"""Helpers for exposing server documentation as MCP Resources."""

from pathlib import Path


def register_docs(mcp, docs_dir: str = "docs") -> None:
    """Register all markdown files in a directory as MCP Resources.

    Each file becomes a resource with:
    - URI: docs://<filename>
    - Name: derived from filename (e.g. "scene-types.md" → "Scene Types")
    - Description: first non-empty line of the file

    Usage:
        from cooperage_sdk import register_docs

        mcp = FastMCP("my-server", json_response=True, stateless_http=True)
        register_docs(mcp)

    Args:
        mcp: A FastMCP instance.
        docs_dir: Path to the docs directory (default: "docs").
    """
    docs_path = Path(docs_dir)
    if not docs_path.is_dir():
        return

    for filepath in sorted(docs_path.rglob("*")):
        if not filepath.is_file():
            continue

        relative = str(filepath.relative_to(docs_path))
        uri = f"docs://{relative}"
        content = filepath.read_text()

        # Derive a human-readable name from the filename
        name = filepath.stem.replace("-", " ").replace("_", " ").title()

        # Use first non-empty line as description
        description = ""
        for line in content.splitlines():
            stripped = line.strip().lstrip("#").strip()
            if stripped:
                description = stripped[:200]
                break

        # Register as a resource — capture content in closure
        _register_one(mcp, uri, name, description, content)


def _register_one(mcp, uri: str, name: str, description: str, content: str) -> None:
    """Register a single doc resource. Separate function to capture closure correctly."""

    @mcp.resource(uri, name=name, description=description)
    def _read() -> str:
        return content
