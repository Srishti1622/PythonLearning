from mcp.server.fastmcp import FastMCP

mcp=FastMCP("Weather")

@mcp.tool()
async def get_weather(location:str)->str:
    """Get the weather location and provide weather report"""
    return "It's always raining in {location}"


# it will run the server as an API service itself
# it should be running when client make request
if __name__=="__main__":
    mcp.run(transport='streamable-http')