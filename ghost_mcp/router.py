import json
import ollama

def route_tool(message: str):
    
    tool_prompt = f"""
        You are a tool routing system.
        
        Available tools:
        
        1. list_documents
        - List all uploaded documents.
        
        Decide whether the user's message requires a tool.
        
        Return ONLY valid JSON.
        
        Example:
        
        User:
        list_documents
        
        Output:
        {{
            "use_tool": true,
            "tool": "list_documents",
            "arguments" : {{}}
        }}
        
        User:
        hello
        
        Output:
        {{
            "use_tool" : false
        }}
        
        User:
        What PDFs have I uploaded?
        
        Output:
        {{
            "use_tool": true,
            "tool": "list_documents",
            "arguments": {{}}
        }}
        
        USer message:
        {message}
    """
    
    
    response = ollama.chat(
        model = "qwen3:8b",
        messages = [
            {
                "role": "user",
                "content": tool_prompt
            }
        ]
    )
    
    reply = response["message"]["content"]
    
    return json.loads(reply)