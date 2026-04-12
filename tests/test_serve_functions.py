"""Tests for serve_functions and _register_function_as_tool."""

import pytest
from mcp.server.fastmcp import FastMCP

from cooperage_sdk.server import _register_function_as_tool, _format_result


# ── _format_result ───────────────────────────────────────────────────────────


def test_format_string():
    assert _format_result("hello") == "hello"


def test_format_dict():
    result = _format_result({"key": "value"})
    assert '"key"' in result
    assert '"value"' in result


def test_format_list():
    result = _format_result([1, 2, 3])
    assert "[" in result


def test_format_none():
    assert _format_result(None) == "null"


# ── _register_function_as_tool ───────────────────────────────────────────────


def test_register_sync_function():
    mcp = FastMCP("test", json_response=True, stateless_http=True)

    def greet(name: str) -> str:
        """Say hello."""
        return f"Hello, {name}!"

    _register_function_as_tool(mcp, "greet", greet)
    tools = mcp._tool_manager.list_tools()
    names = [t.name for t in tools]
    assert "greet" in names


def test_register_async_function():
    mcp = FastMCP("test", json_response=True, stateless_http=True)

    async def fetch(url: str) -> str:
        """Fetch a URL."""
        return f"fetched {url}"

    _register_function_as_tool(mcp, "fetch", fetch)
    tools = mcp._tool_manager.list_tools()
    names = [t.name for t in tools]
    assert "fetch" in names


def test_register_preserves_description():
    mcp = FastMCP("test", json_response=True, stateless_http=True)

    def my_tool(x: int) -> str:
        """This is the description."""
        return str(x)

    _register_function_as_tool(mcp, "my_tool", my_tool)
    tools = mcp._tool_manager.list_tools()
    tool = next(t for t in tools if t.name == "my_tool")
    assert "description" in tool.description.lower() or tool.description == "This is the description."


def test_register_multiple_functions():
    mcp = FastMCP("test", json_response=True, stateless_http=True)

    def add(a: int, b: int) -> int:
        return a + b

    def sub(a: int, b: int) -> int:
        return a - b

    _register_function_as_tool(mcp, "add", add)
    _register_function_as_tool(mcp, "sub", sub)
    names = [t.name for t in mcp._tool_manager.list_tools()]
    assert "add" in names
    assert "sub" in names
