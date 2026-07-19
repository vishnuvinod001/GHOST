def format_tool_result(
    tool_name: str,
    result
):
    if tool_name == "list_documents":
        return format_list_documents(result)
    
    if tool_name == "read_file":
        return format_read_file(result)
    
    if tool_name == "fetch_url":
        return format_fetch_url(result)
    
    return str(result)


def format_list_documents(result):
    
    reply = "📁 Knowledge Base\n\n"
        
    for item in result.content:
        reply += f"• {item.text}\n"
        
    return reply


def format_read_file(result):
    
    return result.content[0].text

def format_fetch_url(result):
    
    return result.content[0].text