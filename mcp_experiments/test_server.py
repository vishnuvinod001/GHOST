from mcp.server.fastmcp import FastMCP

import os

mcp = FastMCP("GHOST Filesystem Server")

@mcp.tool()
def list_documents() -> list:
    
    documents_folder = "data/documents"
    
    if not os.path.exists(documents_folder):
        return[]

    return os.listdir(documents_folder)

if __name__ == "__main__":
    mcp.run()