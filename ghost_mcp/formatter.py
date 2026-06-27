def format_tool_result(
    tool_name: str,
    result
):
    
    if tool_name == "list_documents":
        
        reply = "📁 Knowledge Base\n\n"
        
        for item in result.content:
            reply += f"• {item.text}\n"
            
        return reply
    return str(result)