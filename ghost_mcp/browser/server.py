from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup

mcp = FastMCP("GHOST Browser Server")

@mcp.tool()
def ping() -> str:
    return "Browser MCP is working!"

@mcp.tool()
def fetch_url(url: str)->str:
    """Fetch and extract readable text from a webpage."""
    
    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Ghost Browser MCP"
        }
    )
    
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    text = soup.get_text(
        separator="\n",
        strip = True
    )
    return text

if __name__ == "__main__":
    mcp.run()