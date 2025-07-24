from mcp.server.fastmcp import FastMCP

# initialize MCP and server name
mcp=FastMCP("Math") 

# create first tool inside server
# provide doc string in """based on doc string, LLM will able to understand which tool to use and call"""
@mcp.tool()
def add(a:int,b:int)->int:
    """_summary_
    Add two numbers
    """
    return a+b

@mcp.tool()
def multiple(a:int,b:int)->int:
    """Multiple two numbers"""
    return a*b

# here we are using stdio transport protocol which basically take input and provide ouput in command prompt itself
# transport='stdio' argument tells the server to use standard input output (stdin/stdout) to receive and respond to tool function calls
if __name__=="__main__":
    mcp.run(transport='stdio')