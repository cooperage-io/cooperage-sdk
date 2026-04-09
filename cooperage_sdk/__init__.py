"""
Cooperage SDK — lightweight helpers for writing Cooperage-compatible MCP servers.

Usage:
    from mcp.server.fastmcp import FastMCP
    from cooperage_sdk import workspace, serve

    mcp = FastMCP("my-server", json_response=True, stateless_http=True)

    @mcp.tool()
    def my_tool(input_file: str) -> str:
        data = workspace.read(input_file)
        workspace.write("output.txt", data.upper())
        return "Done"

    serve(mcp)
"""

from cooperage_sdk.workspace import workspace
from cooperage_sdk.server import serve

__all__ = ["workspace", "serve"]
