"""Drive the Predactiv MCP server as agent tools using LangChain.

This sample connects to the Predactiv MCP server over HTTP, dynamically
converts its tools into LangChain tools, binds them to an LLM, and runs a goal
prompt through a LangChain agent. The agent loop runs client-side: LangChain
calls the LLM, executes any requested tools against the MCP server, and feeds
the results back until the agent produces a final answer.

Required environment variables:
    OPENAI_API_KEY   API key for the OpenAI model used as the agent LLM.
    CLIENT_ID        Predactiv OAuth client ID, used by oauth_token_lib.
    CLIENT_SECRET    Predactiv OAuth client secret, used by oauth_token_lib.

The OpenAI key and the CLIENT_ID/CLIENT_SECRET pair are separate credentials:
the first authenticates to the LLM provider, the second to the Predactiv MCP
server.

Run from inside this directory:
    pip install -r requirements.txt
    python agent.py

See README.md for full setup and troubleshooting notes.
"""

import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from oauth_token_lib import auth_headers

PREDACTIV_MCP_SERVER_URL = "https://mcp.predactiv.com" # Predactiv MCP server endpoint
GOAL = "Get list of my audiences from the Predactiv MCP server and return it to me."

async def run_agent():
    """Connect to the Predactiv MCP server, build a LangChain agent, and run GOAL.

    Fetches the MCP server's tools, binds them to the LLM, invokes the agent with
    the GOAL prompt, and prints the agent's final message.
    """
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

    # 3. Initialize your LLM. Reads OPENAI_API_KEY from the environment.
    #    Swap the model (or provider) here to use a different LLM.
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