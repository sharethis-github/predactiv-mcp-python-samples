# Predactiv MCP — LangChain AI Agent

This sample shows how to connect an AI agent to the **Predactiv MCP server** using
[LangChain](https://python.langchain.com/) and
[`langchain-mcp-adapters`](https://github.com/langchain-ai/langchain-mcp-adapters).

The agent authenticates to Predactiv, discovers the available tools from the MCP
server at runtime, and lets a large language model call those tools to work with your
Predactiv data platform (audiences, datasets, datasources, destinations, and more).

## How it works

1. **Authenticate** — `oauth_token_lib.auth_headers()` exchanges your `CLIENT_ID` and
   `CLIENT_SECRET` for an OAuth2 bearer token (client-credentials flow) and returns the
   `Authorization` header.
2. **Connect & discover tools** — `MultiServerMCPClient` connects to the Predactiv MCP
   server over HTTP and fetches its tools dynamically. No tools are hardcoded, so your
   agent always sees the latest set the server exposes.
3. **Run the agent** — the MCP tools are bound to an LLM via `create_agent`, and the
   agent is invoked with a natural-language goal.

## Prerequisites

- Python 3.9+
- A Predactiv account with API credentials (`CLIENT_ID` and `CLIENT_SECRET`).
  Contact Predactiv if you don't have these.
- An [OpenAI API key](https://platform.openai.com/) — this sample uses `gpt-4o` as the
  agent's LLM. Set it as the `OPENAI_API_KEY` environment variable.

## Setup

From this `langchain/` directory:

```bash
# (recommended) create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate

# install dependencies (also installs the shared oauth-token-lib package)
pip install -r requirements.txt
```

## Configuration

Set the following environment variables:

```bash
export CLIENT_ID=your-predactiv-client-id
export CLIENT_SECRET=your-predactiv-client-secret
export OPENAI_API_KEY=your-openai-api-key
```

## Run

```bash
python agent.py
```

The sample's default goal is:

> *Get list of my audiences from the Predactiv MCP server and return it to me.*

Edit the `GOAL` constant in [`agent.py`](agent.py) to ask the agent to do something
else with your Predactiv data.

## Troubleshooting

- **`CLIENT_ID and CLIENT_SECRET environment variables must be set.`** — Export both
  variables (see [Configuration](#configuration)) before running.
- **`401 Unauthorized` from the MCP server** — Your credentials are invalid or expired.
  Verify them, or run `python ../oauth-token-lib/oauth_token_lib.py` to confirm a token
  can be obtained.
- **OpenAI authentication errors** — Make sure `OPENAI_API_KEY` is set and valid.

## Learn more

- Predactiv MCP server: `https://mcp.predactiv.com`
- Model Context Protocol: https://modelcontextprotocol.io
