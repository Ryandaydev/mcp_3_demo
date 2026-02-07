from fastmcp import Client
from fastmcp.client.auth import OAuth
import asyncio

async def call_tool():
    oauth = OAuth(
        # Most MCP clients should be public + PKCE
        additional_client_metadata={
            "token_endpoint_auth_method": "none",
        }
    )

    async with Client(
        "https://football-mcp3-server.fastmcp.app/mcp",   
        auth=oauth                     
    ) as client:
        result = await client.call_tool("get_counts")
        print(result)

asyncio.run(call_tool())