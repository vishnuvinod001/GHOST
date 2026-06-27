def format_tool_result(
    tool_name: str,
    result
):
    if tool_name == "list_documents":
        return format_list_documents(result)
    
    return str(result)

def format_list_documents(result):
    
    reply = "📁 Knowledge Base\n\n"
        
    for item in result.content:
        reply += f"• {item.text}\n"
        
    return reply