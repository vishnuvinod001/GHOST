from mcp.server.fastmcp import FastMCP

mcp = FastMCP("GHOST Test Server")

@mcp.tool()
def hello() -> str:
    return "Hello from GHOST MCP"

if __name__ == "__main__":
    mcp.run()