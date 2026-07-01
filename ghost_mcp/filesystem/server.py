from mcp.server.fastmcp import FastMCP

import os

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

WORKSPACE_ROOT = os.path.join(
    BASE_DIR,
    "workspace"
)


PROJECTS_ROOT = r"C:\Users\Asus\Desktop\All\Projects"

os.makedirs(
    WORKSPACE_ROOT,
    exist_ok = True
)

mcp = FastMCP("GHOST Filesystem Server")

#------------------------------LIST DOCUMENTS---------------------------------

@mcp.tool()
def list_documents() -> list:
    
    documents_folder = "data/documents"
    
    if not os.path.exists(documents_folder):
        return[]

    return os.listdir(documents_folder)

#------------------------------READ FILE---------------------------------

@mcp.tool()
def read_file(path: str) -> str:
    
    if not path.startswith("workspace/"):
        return "Access denied."

    relative_path = path.replace(
        "workspace/",
        "",
        1
    )
    
    filepath = os.path.join(
        WORKSPACE_ROOT,
        relative_path
    )
    
    
    if not os.path.exists(filepath):
        return f"File not found: {filepath}"
    
    
    with open(                  # Other text file handler 
        filepath,
        "r",
        encoding = "utf-8",
        errors = "ignore"
    ) as file:
        
        return file.read()
   
#------------------------------CREATE FILE---------------------------------   
    
@mcp.tool()
def create_file(
    path: str,
    content: str = ""
) -> str:
    
    if path.startswith("workspace/"):
        
        relative_path = path.replace(
            "workspace/",
            "",
            1
        )
        
        filepath = os.path.join(
            WORKSPACE_ROOT,
            relative_path
        )
    
    elif path.startswith("projects/"):
        
        relative_path = path.replace(
            "projects/",
            "",
            1
        )
        
        filepath = os.path.join(
            PROJECTS_ROOT,
            relative_path
        )
    
    
    else:
        return "Access denied."
    
    
    os.makedirs(
        os.path.dirname(filepath),
        exist_ok = True
    )
    
    with open(
        filepath,
        "w",
        encoding = "utf-8"
    ) as file:
        
        file.write(content)
    
    return f"File created successfully: {path}"

if __name__ == "__main__":
    
    mcp.run()