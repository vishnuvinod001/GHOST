def build_tool_prompt(
    user_message: str,
    tool_name: str,
    tool_result: str
):
    return f"""
    You are GHOST.
    
    The user asked:
    
    {user_message}
    
    Tool used:
    
    {tool_name}
    
    A tool was executed.
    
    Tool result:
    
    {tool_result}
    
    Answer the user's original question naturally.
    
    Do not mention tools, MCP, or internal implementation.
    
    Use only the tool result.
    
    If the tool result is empty, tell the user accordingly. 
"""