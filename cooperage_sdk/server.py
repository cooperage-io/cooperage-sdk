"""Server helpers for Cooperage — start tools from MCP, functions, or REST apps."""

import asyncio
import inspect
import os
from typing import Any, Callable


def serve(mcp, host: str = "0.0.0.0", port: int | None = None) -> None:
    """Start an MCP server. Replaces the uvicorn boilerplate.

    Args:
        mcp: A FastMCP instance.
        host: Bind address (default: 0.0.0.0).
        port: Port to listen on (default: PORT env var or 8000).
    """
    import uvicorn

    if port is None:
        port = int(os.environ.get("PORT", "8000"))

    uvicorn.run(mcp.streamable_http_app(), host=host, port=port)


def serve_functions(
    functions: dict[str, Callable],
    name: str = "cooperage-functions",
    host: str = "0.0.0.0",
    port: int | None = None,
) -> None:
    """Start a Cooperage-compatible server from plain Python functions.

    No MCP knowledge required. Each function becomes a tool the LLM can call.
    Function docstrings become tool descriptions. Type hints become parameter schemas.

    Args:
        functions: Dict of {tool_name: callable}.
        name: Server name (shown in Cooperage UI).
        host: Bind address.
        port: Port to listen on (default: PORT env var or 8000).

    Example:
        from cooperage_sdk import serve_functions, workspace

        def analyze(input_path: str) -> str:
            '''Analyze a file from the workspace.'''
            data = workspace.path(input_path).read_text()
            return f"Analyzed {len(data)} chars"

        serve_functions({"analyze": analyze})
    """
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP(name, json_response=True, stateless_http=True)

    for tool_name, func in functions.items():
        _register_function_as_tool(mcp, tool_name, func)

    serve(mcp, host=host, port=port)


def _register_function_as_tool(mcp, name: str, func: Callable) -> None:
    """Register a plain Python function as an MCP tool."""
    description = (func.__doc__ or "").strip()

    # Build wrapper that handles both sync and async functions
    if asyncio.iscoroutinefunction(func):
        async def handler(**kwargs):
            result = await func(**kwargs)
            return _format_result(result)
        handler.__name__ = name
        handler.__doc__ = description
    else:
        def handler(**kwargs):
            result = func(**kwargs)
            return _format_result(result)
        handler.__name__ = name
        handler.__doc__ = description

    # Copy type hints so FastMCP can generate the schema
    handler.__annotations__ = {
        k: v for k, v in func.__annotations__.items() if k != "return"
    }

    mcp.tool(name=name, description=description)(handler)


def _format_result(result: Any) -> str:
    """Format a function's return value as a string for MCP."""
    if isinstance(result, str):
        return result
    import json
    return json.dumps(result, indent=2, default=str)
