import asyncio

from ghost_mcp.filesystem.client import call_tool as filesystem_call_tool
from ghost_mcp.browser.client import call_tool as browser_call_tool  

FILESYSTEM_TOOLS = {
    "read_file",
    "create_file",
    "edit_file",
    "delete_file",
    "search_file",
    "list_documents"
}

BROWSER_TOOLS = {
    "fetch_url"
}                       # Python Sets for easy O(1) lookup.

def execute_tool(
    tool_name: str,
    arguments: dict
):
    if tool_name in FILESYSTEM_TOOLS:
        return asyncio.run(
            filesystem_call_tool(
                tool_name,
                arguments
            )
        )
    
    if tool_name in BROWSER_TOOLS:
        return asyncio.run(
            browser_call_tool(
                tool_name,
                arguments
            )
        )
    
    raise ValueError(f"Unknown tool: {tool_name}")