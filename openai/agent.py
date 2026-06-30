"""Predactiv MCP server as AI agent tools using OpenAI.

This sample uses OpenAI's native MCP connector rather than a client-side agent
loop: the MCP server definition is handed to the Responses API, and OpenAI's
infrastructure connects to the server, discovers its tools, and runs the
tool-calling loop server-side. The script makes a single `responses.create` call
and prints the final text answer.

Required environment variables:
    OPENAI_API_KEY   OpenAI API key, used to call the model.
    CLIENT_ID        Predactiv OAuth client ID, used by oauth_token_lib.
    CLIENT_SECRET    Predactiv OAuth client secret, used by oauth_token_lib.

`OPENAI_API_KEY` and the `CLIENT_ID`/`CLIENT_SECRET` pair are separate
credentials: the first authenticates to OpenAI, the second to the Predactiv MCP
server.

Run from inside this directory:
    pip install -r requirements.txt
    python agent.py

See README.md for full setup and troubleshooting notes.
"""

import asyncio
import os
from openai import OpenAI
from oauth_token_lib import get_bearer_token

# 1. Define Predactiv MCP server endpoint and the goal for the agent.
#    Edit GOAL to change the task handed to the agent.
PREDACTIV_MCP_SERVER_URL = "https://mcp.predactiv.com" # Predactiv MCP server endpoint
GOAL = "Get list of my audiences from the Predactiv MCP server and return it to me."

async def run_openai_cloud_agent():
    """Send GOAL to OpenAI with the Predactiv MCP server attached and print the answer.

    Builds a single Responses API request that declares the Predactiv MCP server
    (authenticated with a Predactiv OAuth bearer token) as an `mcp` tool. OpenAI
    runs the tool-calling loop server-side and returns a final response; its text
    is printed to stdout.
    """
    # 2. Initialize the OpenAI client. The API key is read from the
    #    OPENAI_API_KEY environment variable.
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    print("Handing the prompt and MCP server configuration directly to OpenAI...")

    # 3. Request completion using the Responses API. The `mcp` tool tells OpenAI
    #    which remote MCP server to connect to; OpenAI discovers its tools and
    #    runs the tool-calling loop server-side. The Responses API uses `input`
    #    (not `messages`, which belongs to the Chat Completions API).
    response = client.responses.create(
        model="gpt-5.4-mini",
        tools=[
            {
                "type": "mcp",
                "server_label": "predactiv_mcp_server",
                "server_description": "Predactiv MCP server endpoint",
                "server_url": PREDACTIV_MCP_SERVER_URL,
                # Pass the raw OAuth access token; OpenAI adds the "Bearer " prefix
                # and the Authorization header itself. Do not prefix it here.
                "authorization": get_bearer_token(),
                # Run MCP tools without manual approval; otherwise the model emits an
                # mcp_approval_request and stops, leaving output_text empty.
                "require_approval": "never",
            }
        ],
        input=GOAL
    )

    # 4. Read the clean final text response
    print("\nAgent Final Response:")
    if response.output_text:
        print(response.output_text)
    else:
        # No final text message — show the raw output items to see what happened
        # (e.g. mcp_approval_request, mcp_call errors, or an incomplete status).
        print(f"(no text output; status={response.status})")
        for item in response.output:
            print(item)

if __name__ == "__main__":
    asyncio.run(run_openai_cloud_agent())