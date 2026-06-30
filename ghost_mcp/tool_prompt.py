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

Instead, answer the user's request using ONLY the information below.

Tool Name:
{tool_name}

Retrieved Content:

{tool_result}

If the retrieved content is empty, politely say that no information was found.
"""