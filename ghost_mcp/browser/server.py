from mcp.server.fastmcp import FastMCP

mcp = FastMCP("GHOST Browser Server")

@mcp.tool()
def ping() -> str:
    return "Browser MCP is working!"

if __name__ == "__main__":
    mcp.run()