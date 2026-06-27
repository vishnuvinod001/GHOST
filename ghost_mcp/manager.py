import asyncio

from ghost_mcp.filesystem.client import call_tool

def execute_tool(
    tool_name: str,
    arguments: dict
):
    return asyncio.run(
        call_tool(
            tool_name,
            arguments
        )
    )