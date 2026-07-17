from mcp.server.fastmcp import FastMCP
import requests

mcp = FastMCP("GHOST Browser Server")

@mcp.tool()
def ping() -> str:
    return "Browser MCP is working!"

@mcp.tool()
def fetch_url(url: str)->str:
    """Fetch the HTML of a webpage."""
    
    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Ghost Browser MCP"
        }
    )
    
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    mcp.run()