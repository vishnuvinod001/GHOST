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
    
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
        
    title = "Untitled"
    
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    
    text = soup.get_text(
        separator="\n",
        strip = True
    )
    
    lines = text.splitlines()
    
    while lines and lines[0].strip() == title:
        lines.pop(0)
        
    text = "\n".join(lines).strip()
    
    return (
        f"Title:\n"
        f"{title}\n\n"
        f"Content:\n"
        f"{text}"
    )


if __name__ == "__main__":
    mcp.run()