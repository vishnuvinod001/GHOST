from ghost_mcp.manager import execute_tool

result = execute_tool(
    "list_documents",
    {}
)

print(result)