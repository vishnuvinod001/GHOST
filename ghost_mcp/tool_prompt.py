def build_tool_prompt(
    tool_name: str,
    tool_result: str
):
    return f"""
    Tool Information
    
    The following tool was executed to help answer the user's request.
    
    Tool:
    
    {tool_name}
    
    Tool result:
    
    {tool_result}
    
    Answer the user's original request using ONLY this information.
    
    Do not mention:
    - tools
    - MCP
    - internal systems
    - routing
    
    If the tool result is empty, politely tell the user nothing was found. 
"""