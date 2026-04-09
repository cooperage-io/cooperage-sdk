"""
Cooperage SDK — lightweight helpers for writing Cooperage-compatible MCP servers.

Usage:
    from mcp.server.fastmcp import FastMCP
    from cooperage_sdk import workspace, serve, register_docs

    mcp = FastMCP("my-server", json_response=True, stateless_http=True)

    @mcp.tool()
    def my_tool(input_file: str) -> str:
        data = workspace.path(input_file).read_text()
        workspace.path("output.txt").write_text(data.upper())
        return "Done"

    register_docs(mcp)
    serve(mcp)
"""

from cooperage_sdk.workspace import workspace
from cooperage_sdk.server import serve
from cooperage_sdk.docs import register_docs

__all__ = ["workspace", "serve", "register_docs"]
