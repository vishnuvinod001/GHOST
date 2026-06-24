from mcp.server.fastmcp import FastMCP

import os

mcp = FastMCP("GHOST Filesystem Server")

@mcp.tool()
def list_documents() -> list:
    
    documents_folder = "data/documents"
    
    if not os.path.exists(documents_folder):
        return[]

    return os.listdir(documents_folder)


@mcp.tool()
def read_file(filename: str) -> str:
    
    filepath = os.path.join(
        "data/documents",
        filename
    )
    
    if not os.path.exists(filepath):
        return "File not found"

    with open(
        filepath,
        "r",
        encoding = "utf-8",
        errors = "ignore"
    ) as file:
        
        return file.read()
    

if __name__ == "__main__":
    
    mcp.run()