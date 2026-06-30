"""Predactiv MCP server as AI agent tools using the raw MCP Python SDK + OpenAI.

This sample drives the Predactiv MCP server with the low-level MCP Python SDK
and runs the agent loop client-side with an OpenAI model. It connects to the
server over Streamable HTTP, lists the available tools, converts them to the
OpenAI function-calling format, and then loops: the model requests a tool, the
script executes it against the MCP session, feeds the result back, and repeats
until the model produces a final answer.

Like the `langchain/` sample, the agent loop runs client-side — but here your
code owns the connection and the tool-calling loop directly, without the
framework. (Contrast with the `claude/` and `openai/` samples, which hand the
server to the provider's native MCP connector and run the loop server-side.)

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
import json
import os

from openai import OpenAI
from mcp import ClientSession
from mcp.client.streamable_http import create_mcp_http_client, streamable_http_client
from oauth_token_lib import auth_headers

# 1. Define Predactiv MCP server endpoint and the goal for the agent.
#    Edit GOAL to change the task handed to the agent.
PREDACTIV_MCP_SERVER_URL = "https://mcp.predactiv.com" # Predactiv MCP server endpoint
GOAL = "Get list of my audiences from the Predactiv MCP server and return it to me."
OPENAI_MODEL = "gpt-5.4-mini" # Swap for any model your key can access

async def run_agent():
    """Connect to the Predactiv MCP server, then run an OpenAI tool-use loop on GOAL.

    Lists the MCP server's tools, converts them to the OpenAI function-calling
    schema, and drives a manual agentic loop: the model calls tools, the script
    executes them via the MCP session and returns the results, until the model
    finishes its answer.
    """
    # 2. Initialize the OpenAI client. The API key is read from the
    #    OPENAI_API_KEY environment variable.
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # 3. Connect to the Predactiv MCP server over Streamable HTTP. auth_headers()
    #    performs the client-credentials token exchange using CLIENT_ID /
    #    CLIENT_SECRET and returns a Bearer Authorization header. The headers are
    #    attached to the httpx client, which streamable_http_client then uses.
    print("Connecting to MCP server...")
    async with create_mcp_http_client(headers=auth_headers()) as http_client:
        async with streamable_http_client(
            PREDACTIV_MCP_SERVER_URL, http_client=http_client
        ) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # 4. Fetch the server's tools and convert them to the OpenAI
                #    function-calling format. Nothing is hardcoded — the agent
                #    always sees the latest tool set.
                print("Fetching tools from MCP server...")
                tools_result = await session.list_tools()
                openai_tools = [
                    {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description or "",
                            "parameters": tool.inputSchema,
                        },
                    }
                    for tool in tools_result.tools
                ]

                # 5. Run the agentic loop: call the model, execute any requested
                #    tools against the MCP session, feed results back, repeat.
                print("Asking the agent...")
                messages = [{"role": "user", "content": GOAL}]
                while True:
                    response = client.chat.completions.create(
                        model=OPENAI_MODEL,
                        messages=messages,
                        tools=openai_tools,
                    )
                    message = response.choices[0].message

                    # The model is done once it stops requesting tools.
                    if not message.tool_calls:
                        break

                    # Record the assistant turn (including its tool_calls).
                    messages.append(message)

                    # Execute each requested tool via the MCP session and append
                    # one "tool" message per call, keyed by tool_call_id.
                    for tool_call in message.tool_calls:
                        print(f"  -> calling tool: {tool_call.function.name}")
                        args = json.loads(tool_call.function.arguments or "{}")
                        result = await session.call_tool(tool_call.function.name, args)
                        # Flatten the MCP result's content blocks into a plain string.
                        text = "".join(b.text for b in result.content if b.type == "text")
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": text,
                        })

                # 6. Print the final answer.
                print("\nAgent Final Response:")
                print(message.content)


if __name__ == "__main__":
    asyncio.run(run_agent())
