"""Server helpers for Cooperage MCP servers."""

import os


def serve(mcp, host: str = "0.0.0.0", port: int | None = None) -> None:
    """Start the MCP server. Replaces the uvicorn boilerplate.

    Args:
        mcp: A FastMCP instance.
        host: Bind address (default: 0.0.0.0).
        port: Port to listen on (default: PORT env var or 8000).
    """
    import uvicorn

    if port is None:
        port = int(os.environ.get("PORT", "8000"))

    uvicorn.run(mcp.streamable_http_app(), host=host, port=port)
