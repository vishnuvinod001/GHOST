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

#------------------------------EDIT FILE---------------------------------   

@mcp.tool()
def edit_file(
    path: str,
    content:str,
    mode: str = "replace"
) -> str:
    
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
        return "File not found."
    
    if mode == "replace":
        
        with open(
            filepath,
            "w",
            encoding = "utf-8"
        ) as file:
            
            file.write(content)
    
    elif mode == "append":
        
        with open(
            filepath,
            "a",
            encoding = "utf-8"
        ) as file:
            
            file.write(content)
    
    elif mode == "prepend":
        
        with open(
            filepath,
            "r",
            encoding = "utf-8"
        ) as file:
            
            existing_content = file.read()
            
        with open(
            filepath,
            "w",
            encoding = "utf-8"
        ) as file:
            
            file.write(content + existing_content)
    
    else:
        return "Invalid mode."
    
    return f"File edited successfully: {path}"


#------------------------------DELETE FILE---------------------------------   

@mcp.tool()
def delete_file(
    path: str,
)-> str:
    
    if not path.startswith("workspace/"):
        return "Access denied."
    
    relative_path = path.replace(
        "workspace/",
        "",
        1 # 1 - replace just the 1st occurrence
    )
    
    filepath = os.path.join(
        WORKSPACE_ROOT,
        relative_path
    )
    
    if not os.path.exists(filepath):
        return "File not found."
    
    os.remove(filepath)
    
    return f"File deleted successfully: {path}"

#------------------------------SEARCH FILE---------------------------------

@mcp.tool()
def search_files(
    query: str
) -> list:
    
    matches = []
    
    for root, _, files in os.walk( # goes through the current directory and also its nested dirs too 
        WORKSPACE_ROOT
    ):
        
        for file in files:
            
            if query.lower() in file.lower():
                
                relative_path = os.path.relpath(
                    os.path.join(root, file),
                    WORKSPACE_ROOT
                )
                
                matches.append(
                    f"workspace/{relative_path}"
                )
        
    return matches

if __name__ == "__main__":
    
    mcp.run()