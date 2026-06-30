# Sample code to demonstrate how to use Predactiv MCP 
# using LangChain's agent framework.

import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from oauth_token_lib import auth_headers

PREDACTIV_MCP_SERVER_URL = "https://mcp.predactiv.com" # Predactiv MCP server endpoint
GOAL = "Get list of my audiences from the Predactiv MCP server and return it to me."

async def run_agent():
    # 1. Connect to your existing HTTP MCP server.
    #    auth_headers() performs the client-credentials token exchange using
    #    CLIENT_ID / CLIENT_SECRET and returns a Bearer Authorization header.
    client = MultiServerMCPClient({
        "my_http_server": {
            "transport": "http",
            "url": PREDACTIV_MCP_SERVER_URL, # Predactiv MCP server endpoint
            "headers": auth_headers(),
        }
    })

    # 2. Fetch and dynamically convert the server's tools
    print("Fetching tools from MCP server...")
    tools = await client.get_tools()

    # 3. Initialize your LLM
    llm = ChatOpenAI(model="gpt-4o")

    # 4. Create the LangChain agent with your server's tools
    agent = create_agent(llm, tools)

    # 5. Invoke the agent
    print("Asking the agent...")
    response = await agent.ainvoke({
        "messages": [{"role": "user", "content": GOAL}]
    })
    
    print("\nAgent Response:")
    print(response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(run_agent())