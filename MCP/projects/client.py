from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

async def main():
    client=MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathserver.py"], # provide full path
                "transport":"stdio",
            },
            "weather":{
                "url":"http://localhost:8000/mcp", # make sure that server is running here else will get error all connection failed
                "transport":"streamable_http",
            }
        }
    )

    os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

    tools=await client.get_tools()
    model=ChatGroq(model='gemma2-9b-it')
    agent=create_react_agent(
        model,tools
    )

    math_response=await agent.ainvoke(
        {"messages":[{"role":"user","content":"what's (3+5)x12?"}]}
    )

    print("Math response:",math_response['messages'][-1].content)
    
    weather_response=await agent.ainvoke(
        {"messages":[{"role":"user","content":"what's the weather in bindki?"}]}
    )

    print("Weather response:",weather_response['messages'][-1].content)


# as the function which we create is async, so we need to run that using
asyncio.run(main())