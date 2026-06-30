# Predactiv MCP — Anthropic Claude AI Agent

This sample shows how to connect an AI agent to the **Predactiv MCP server** using
[Anthropic Claude](https://www.anthropic.com/) directly.

Unlike a client-side agent loop, this sample uses Claude's **native MCP connector**: the MCP
server definition is handed to the Messages API, and Anthropic's infrastructure connects to
the server, discovers its tools, and runs the tool-calling loop server-side. Your code makes
a single `messages.create` call and reads back the final answer.

> Contrast with the [`mcp-sdk/`](../mcp-sdk) sample, which uses the raw MCP Python SDK and
> runs the tool-calling loop client-side. Here, Anthropic owns the connection and the loop.

## How it works

1. **Authenticate** — `oauth_token_lib.get_bearer_token()` performs the Predactiv OAuth2
   client-credentials exchange and returns a bearer token, passed to the MCP server as
   `authorization_token`.
2. **Connect & discover tools** — the `mcp_servers` parameter declares the Predactiv server
   (`type`, `name`, `url`, `authorization_token`). The matching `mcp_toolset` entry in
   `tools` (linked by `mcp_server_name`) enables those tools for the model.
3. **Run the agent** — Claude connects to the MCP server, lists its tools, calls them as
   needed, and returns a final response. The `mcp-client-2025-11-20` beta flag enables the
   connector.

The Predactiv MCP tools expose the data platform: audiences, datasets, datasources,
destinations, filters/predictors, and insights (`predactiv_*` tool families).

## Prerequisites

- Python 3.9+
- A Predactiv account with API credentials (`CLIENT_ID` and `CLIENT_SECRET`).
  Contact Predactiv if you don't have these.
- An [Anthropic API key](https://console.anthropic.com/) — this sample uses `claude-haiku-4-5`
  as the agent's LLM. Set it as the `ANTHROPIC_API_KEY` environment variable.

> **Two separate credentials.** `ANTHROPIC_API_KEY` authenticates your calls to Claude.
> `CLIENT_ID` / `CLIENT_SECRET` authenticate to the Predactiv MCP server via
> `oauth_token_lib`. Both must be set.

## Setup

From this `claude/` directory:

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
export ANTHROPIC_API_KEY=your-anthropic-api-key
```

## Run

```bash
python agent.py
```

The sample's default goal is:

> *Get list of my audiences from the Predactiv MCP server and return it to me.*

Edit the `GOAL` constant in [`agent.py`](agent.py) to ask the agent to do something else with
your Predactiv data. The model is set in the `messages.create` call (`model="claude-haiku-4-5"`)
— swap it for a more capable model (e.g. `claude-sonnet-4-6`, `claude-opus-4-8`) if your task
needs it.

## Troubleshooting

- **`CLIENT_ID and CLIENT_SECRET environment variables must be set.`** — Export both
  variables (see [Configuration](#configuration)) before running.
- **`401 Unauthorized` from the MCP server** — Your credentials are invalid or expired.
  Verify them, or run `python ../oauth-token-lib/oauth_token_lib.py` to confirm a token can
  be obtained.
- **`429 rate_limit_error` from Anthropic** — The MCP connector injects the server's full
  tool catalog into each request as input tokens, so a single call can be large. If you hit a
  `429`, wait ~60 seconds between runs, use a model with more headroom, or request an increase
  at <https://console.anthropic.com/settings/limits>.
- **`AttributeError` reading the response** — `response.content` is a mixed list of blocks
  (MCP tool-use, tool-result, and text). The sample joins only the `text` blocks to build the
  final answer — don't assume `content[0]` is text.
- **Anthropic authentication errors** — Make sure `ANTHROPIC_API_KEY` is set and valid.

## Learn more

- Predactiv MCP server: `https://mcp.predactiv.com`
- Anthropic MCP connector: https://docs.claude.com/en/docs/agents-and-tools/mcp-connector
- Model Context Protocol: https://modelcontextprotocol.io
