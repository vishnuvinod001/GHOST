def build_tool_prompt(
    tool_name: str,
    tool_result: str
):
    return f"""
The user's request has ALREADY been fulfilled by an internal tool.

The tool has already accessed the requested resource.

You already have the complete result below.

DO NOT say:
 - you cannot access files
 - you cannot open documents
 - you do not have permission
 - you cannot view PDFs
 - you cannot browse the web
 - you cannot access websites
 
Instead, answer the user's request naturally using ONLY the information below.

Do NOT copy or repeat the retrieved content verbatim unless the user explicitly asks for the raw output.

If the user asks for:
 - an explanation, explain it in your own words.
 - a summary, summarize the information.
 - key points, extract the important points.
 - a comparison, compare using the retrieved information.
 - question about the content, answer them using the retrieved information.
 
Do NOT invent information that is not present in the retrieved content.

Tool Name:
{tool_name}

Retrieved Content:

{tool_result}

If the retrieved content is empty, politely say that no information was found.  

"""