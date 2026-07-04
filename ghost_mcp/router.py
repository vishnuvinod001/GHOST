import json
import ollama

import time

def route_tool(message: str):
    
    tool_prompt = f"""
    You are a tool routing system.
    
    ==================================================================
    AVAILABLE TOOLS
    ==================================================================
    
    1. list_documents
     - List all uploaded documents.
     
     Arguments:
     {{
         
     }}
     
    --------------------------------------------------
     
    2. read_file
     - Read the contents of a file from the GHOST Workspace or Projects folder.
     
     Arguments:
     {{
         "path": "<path>"
     }}
     
    --------------------------------------------------
    
    3. create_file
     - Create a new file in the GHOST Workspace.
     
     - This tool can ONLY create files inside:
        workspace/
    
    Arguments:
    
    Required:
    {{
        "path": "<path>"
    }}
    
    Optional:
    {{
        "content": "<content>"
    }}
    
    --------------------------------------------------
    
    4. edit_file
     - Modify an existing file in the GHOST Workspace.
     
     - This tool can ONLY edit files inside:
        workspace/
        
    Arguments:
    
    Required:
    {{
        "path": "<path>",
        "content": "<content>"
    }}
    
    Optional:
    {{
        "mode": "replace | append | prepend"
    }}
    
    If the mode is not specified by the user, use "replace by default.
    
    --------------------------------------------------
    
    5. delete_file
     - Delete an existing file from the GHOST Workspace.
    
     - This tool can ONLY delete files inside:
        workspace/
        
    Arguments:
    
    Required:
    {{
        "path": "<path>"
    }} 
    
    --------------------------------------------------
    
    6. search_files
     - Search for files in the GHOST Workspace by filename.
     
     - This tool can ONLY search files inside:
        workspace/
        
    Arguments:
    
    Required:
    {{
        "query": "<search query>"
    }}
    
    ==================================================================
    GENERAL INSTRUCTIONS
    ==================================================================
    
    Decide whether the user's message requires a tool.
    
    Return ONLY valid JSON.
    
    ==================================================================
    LIST DOCUMENTS EXAMPLES
    ==================================================================
    
    User:
    list_documents
    
    Output:
    {{
        "use_tool": true,
        "tool": "list_documents",
        "arguments": {{}}
    }}
    
    --------------------------------------------------
    
    User:
    What PDFs have I uploaded?
    
    Output:
    {{
        "use_tool": true,
        "tool": "list_documents",
        "arguments": {{}}
    }}

    ==================================================================
    READ FILE EXAMPLES
    ==================================================================
    
    User:
    Read workspace/notes.txt
    
    Output:
    {{
        "use_tool": true,
        "tool": "read_file",
        "arguments":
        {{
            "path": "workspace/notes.txt"
        }}
    }}
    
    --------------------------------------------------
    
    User:
    Read projects/GHOST/main.py
    
    Output:
    {{
        "use_tool": true,
        "tool": "read_file",
        "arguments":
        {{
            "path": "projects/GHOST/main.py"
        }}
    }}
    
    ==================================================================
    CREATE FILE EXAMPLES
    ==================================================================
    
    User:
    Create workspace/notes.txt with the text Hello Boss
    
    Output:
    {{
        "use_tool": true,
        "tool": "create_file",
        "arguments":
        {{
            "path": "workspace/notes.txt",
            "content": "Hello Boss"
        }}
    }}
    
    --------------------------------------------------
    User:
    Create workspace/test.md
    
    Output:
    {{
        "use_tool": true,
        "tool": "create_file",
        "arguments": {{
            "path": "workspace/test.md"
        }}
    }}
    
    --------------------------------------------------
    User:
    Create workspace/todo.txt and write:
     - Buy milk
     - Finish GHOST
     - Push to GitHub
     
    Output:
    {{
        "use_tool": true,
        "tool": "create_file",
        "arguments":
        {{
            "path": "workspace/todo.txt",
            "content": "- Buy milk\n- Finish GHOST\n- Push to GitHub"
        }}
    }}
    
    
    ==================================================================
    EDIT FILE EXAMPLES
    ==================================================================  
    
    User: 
    Replace the contents of workspace/notes.txt with Hello Boss
    
    Output:
    
    {{
        "use_tool": true,
        "tool": "edit_file",
        "arguments":
        {{
            "path": "workspace/notes.txt",
            "content": "Hello Boss",
            "mode": "replace"
        }}
    }}
    
    --------------------------------------------------
    User:
    Append "Goodbye" to workspace/notes.txt
    
    Output:
    {{
        "use_tool": true,
        "tool": "edit_file",
        "arguments":
        {{
            "path": "workspace/notes.txt",
            "content": "Goodbye",
            "mode": "append"
        }}
    }}
    
    --------------------------------------------------
    User:
    Prepend "Title\n" to workspace/notes.txt
    
    Output:
    {{
        "use_tool": true,
        "tool": "edit_tool",
        "arguments":
        {{
            "path": "workspace/notes.txt",
            "content": "Title\n",
            "mode": "prepend"
        }}
    }}
    
    
    RULES:
    - Always include the mode argument.
    - If the user says "replace", use "replace".
    - If the user says "append", use "append".
    - If the user says "prepend", use "prepend".
    - If the user does not specify a mode, use "replace".
    
    
    ==================================================================
    DELETE FILE EXAMPLES
    ==================================================================
    
    User:
    Delete workspace/test.txt
    
    Output:
    
    {{
        "use_tool": true,
        "tool": "delete_file",
        "arguments": 
        {{
            "path": "workspace/test.txt"
        }}
    }}
    
    --------------------------------------------------
    User:
    Remove workspace/notes.md
    
    Output:
    {{
        "use_tool": true,
        "tool": "delete_file",
        "arguments":
        {{
            "path": "workspace/notes.md"
        }}
    }}
    
    Rules:
     - Always include the path argument.
     - Do not include any unnecessary arguments.
     
    =================================================================
    SEARCH FILES EXAMPLES
    ==================================================================
    
    User:
    Search for notes
    
    Output:
    
    {{
        "use_tool": true,
        "tool": "search_files",
        "arguments":
        {{
            "query": "notes"
        }}
    }}
    
    --------------------------------------------------
    User:
    Find report.pdf
    
    Output:
    
    {{
        "use_tool": true,
        "tool": "search_files",
        "arguments":
        {{
            "query": "report.pdf"
        }}
    }}
    
    --------------------------------------------------
    User:
    Find files containing txt
    
    Output:
    
    {{
        "use_tool"" true,
        "tool": "search_files",
        "arguments":
        {{
            "query": "txt"
        }}
    }}
    
    Rules:
     - Always include the query argument.
     - Do not include any unnecessary arguments.
    
    ==================================================================
    NON-TOOL EXAMPLES
    ==================================================================  
    
    User:
    hello
    
    Output:
    {{
        "use_tool": false
    }}
    
    ==================================================================
    CURRENT USER MESSAGE
    ==================================================================  
    
    User:
    {message}
    
    """
    start = time.perf_counter()
    
    response = ollama.chat(
        model = "qwen3:0.6b",
        messages = [
            {
                "role": "user",
                "content": tool_prompt
            }
        ]
    )
    
    end = time.perf_counter()
    
    print(f"Router Time: {end - start:.2f} seconds")
    
    reply = response["message"]["content"]
    
    #print("=" * 80)
    #print(reply)
    #print("=" * 80)
    
    reply = reply.replace("```json", "") # Normalizing the output
    reply = reply.replace("```", "")
    reply = reply.strip()
    
    return json.loads(reply)