"""Predactiv MCP server as AI agent tools using Anthropic Claude.

This sample uses Claude's native MCP connector rather than a client-side agent
loop: the MCP server definition is handed to the Messages API, and Anthropic's
infrastructure connects to the server, discovers its tools, and runs the
tool-calling loop server-side. The script makes a single `messages.create` call
and prints the final text answer.

Required environment variables:
    ANTHROPIC_API_KEY   Anthropic API key, used to call Claude.
    CLIENT_ID           Predactiv OAuth client ID, used by oauth_token_lib.
    CLIENT_SECRET       Predactiv OAuth client secret, used by oauth_token_lib.

`ANTHROPIC_API_KEY` and the `CLIENT_ID`/`CLIENT_SECRET` pair are separate
credentials: the first authenticates to Claude, the second to the Predactiv
MCP server.

Run from inside this directory:
    pip install -r requirements.txt
    python agent.py

See README.md for full setup and troubleshooting notes.
"""

import asyncio
import os
from anthropic import Anthropic
from oauth_token_lib import get_bearer_token

# 1. Define Predactiv MCP server endpoint and the goal for the agent.
#    Edit GOAL to change the task handed to the agent.
PREDACTIV_MCP_SERVER_URL = "https://mcp.predactiv.com" # Predactiv MCP server endpoint
GOAL = "Get list of my audiences from the Predactiv MCP server and return it to me."

async def run_claude_cloud_agent():
    """Send GOAL to Claude with the Predactiv MCP toolset attached and print the answer.

    Builds a single Messages API request that declares the Predactiv MCP server
    (authenticated with a Predactiv OAuth bearer token) and enables its tools via
    an `mcp_toolset`. Claude runs the tool-calling loop server-side and returns a
    final message; the text blocks of that message are printed to stdout.
    """
    # 2. Initialize the Claude client. The API key is read from the
    #    ANTHROPIC_API_KEY environment variable.
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    print("Handing the prompt and MCP server definition directly to Claude...")
    
    # 3. Create the message using the native cloud-orchestrated MCP connector
    response = client.beta.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1000,
        # Declare the remote MCP server Claude should connect to. The
        # authorization_token is the Predactiv OAuth bearer token obtained via
        # the client-credentials exchange in oauth_token_lib.
        mcp_servers=[
            {
                "type": "url",
                "name": "predactiv_mcp_server", # Server label; must match mcp_server_name below
                "url": PREDACTIV_MCP_SERVER_URL, # Predactiv MCP server endpoint
                "authorization_token": get_bearer_token() # Bearer token passed through to the server
            }
        ],
        # Enable the declared server's tools. mcp_server_name must exactly match
        # the "name" of the mcp_servers entry above.
        tools=[
            {
                "type": "mcp_toolset",
                "mcp_server_name": "predactiv_mcp_server"
            }
        ],
        # Beta flag that enables the server-side MCP connector.
        betas=["mcp-client-2025-11-20"],
        messages=[
            {
                "role": "user", 
                "content": GOAL
            }
        ]
    )

    # 4. Extract and print the final answer — response.content is a mixed list of
    # blocks (MCP tool_use, tool_result, text); print only the text blocks.
    print("\nAgent Final Response:")
    answer = "".join(block.text for block in response.content if block.type == "text")
    print(answer)

if __name__ == "__main__":
    asyncio.run(run_claude_cloud_agent())