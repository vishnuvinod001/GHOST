import asyncio

from mcp import ClientSession

async def main():
    
    from mcp.client.stdio import (
        stdio_client,
        StdioServerParameters
    )
    
    server_params = StdioServerParameters(
        command = "python",
        args = ["mcp_experiments/test_server.py"]
    ) 
    
    async with stdio_client(server_params) as (read, write):
       
        async with ClientSession(read, write) as session:
          
            await session.initialize()
            
            tools = await session.list_tools()
            
            print(tools)

asyncio.run(main())