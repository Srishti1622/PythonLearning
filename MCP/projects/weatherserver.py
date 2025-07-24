from mcp.server.fastmcp import FastMCP
from typing import Any
import httpx

# initialize the mcp server
mcp=FastMCP("Weather")

# open-source api
NWS_API_BASE='https://api.weather.gov'
USER_AGENT='weather-app/1.0'

@mcp.tool()
async def get_weather(location:str)->str:
    """Get the weather location and provide weather report"""
    return "It's always raining in {location}"


async def make_nws_request(url:str)->dict[str,Any] | None:
    """Make a request to the NWS API with proper error handling"""
    headers={
        "User-Agent":USER_AGENT,
        "Accept":"application/geo+json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response=await client.get(url,headers=headers,timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None
        
def format_alert(feature:dict)-> str:
    """Format an alert feature into a readable string"""
    props=feature['properties']
    return f"""
        Event: {props.get('event','Unknown')}
        Area: {props.get('areaDesc','Unknown')}
        Severity: {props.get('severity','Unknown')}
        Description: {props.get('description','No description available')}
        Instructions: {props.get('instruction','No specific instructions provided')}
        """


# defining services/tools
@mcp.tool()
async def get_alerts(state:str)->str:
    """Get weather alerts for a US state.
    
    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url=f'{NWS_API_BASE}/alerts/active/area/{state}'
    data=await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or No alerts found."
    
    if not data['features']:
        return "No active alerts for this state."
    
    alerts=[format_alert(feature) for feature in data['features']]
    return "\n----\n".join(alerts)


@mcp.resource('echo://{message}')
def echo_resource(message: str)->str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"

# it will run the server as an API service itself
# it should be running when client make request
if __name__=="__main__":
    mcp.run(transport='streamable-http')