# Predactiv MCP — MCP Python SDK + OpenAI Agent

This sample shows how to connect an AI agent to the **Predactiv MCP server** using the
low-level [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) together with
[OpenAI](https://platform.openai.com/).

It connects to the server directly over Streamable HTTP, discovers the available tools at
runtime, converts them to OpenAI's function-calling format, and runs the agent loop
**client-side**: the model requests a tool, the script executes it against the MCP session,
returns the result, and the loop repeats until the model produces a final answer. This is the
same client-side shape as the [`langchain/`](../langchain) sample — but with no framework, so
you can see exactly how the tool-calling loop works.

> Contrast with the [`claude/`](../claude) and [`openai/`](../openai) samples, which hand the
> server definition to the provider's native MCP connector and let the provider run the loop
> server-side. Here, your code owns the connection and the loop.

## How it works

1. **Authenticate** — `oauth_token_lib.auth_headers()` exchanges your `CLIENT_ID` and
   `CLIENT_SECRET` for an OAuth2 bearer token (client-credentials flow) and returns the
   `Authorization` header.
2. **Connect & discover tools** — `streamable_http_client` + `ClientSession` connect to the
   Predactiv MCP server and `list_tools()` fetches its tools dynamically. Nothing is
   hardcoded, so the agent always sees the latest set the server exposes.
3. **Run the agent** — the tools are converted to the OpenAI function-calling schema and
   passed to the model. A manual loop calls the model, executes each requested tool via
   `session.call_tool(...)`, feeds the results back as `tool` messages, and repeats until the
   model stops calling tools.

The Predactiv MCP tools expose the data platform: audiences, datasets, datasources,
destinations, filters/predictors, and insights (`predactiv_*` tool families).

## Prerequisites

- Python 3.10+ (required by the MCP Python SDK)
- A Predactiv account with API credentials (`CLIENT_ID` and `CLIENT_SECRET`).
  Contact Predactiv if you don't have these.
- An [OpenAI API key](https://platform.openai.com/) — this sample uses `gpt-5.4-mini` as the
  agent's LLM. Set it as the `OPENAI_API_KEY` environment variable.

> **OpenAI is just the demonstration LLM — not a requirement.** Because this sample owns the
> tool-calling loop directly, it's model-agnostic: any LLM that supports tool/function calling
> works. To use a different provider, swap the `OpenAI(...)` client and the tool-call handling
> for that provider's SDK (e.g. Anthropic's `messages.create` with `tools`), set its API key,
> and update the `OPENAI_MODEL` constant at the top of [`agent.py`](agent.py). The MCP
> connection and `session.call_tool(...)` execution stay exactly the same.

> **Two separate credentials.** `OPENAI_API_KEY` authenticates your calls to OpenAI.
> `CLIENT_ID` / `CLIENT_SECRET` authenticate to the Predactiv MCP server via
> `oauth_token_lib`. Both must be set.

## Setup

From this `mcp-sdk/` directory:

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

Edit the `GOAL` constant in [`agent.py`](agent.py) to ask the agent to do something else with
your Predactiv data. The model is set by the `OPENAI_MODEL` constant (`gpt-5.4-mini`) — swap
it for any model your key can access.

## Troubleshooting

- **`CLIENT_ID and CLIENT_SECRET environment variables must be set.`** — Export both
  variables (see [Configuration](#configuration)) before running.
- **`401 Unauthorized` from the MCP server** — Your credentials are invalid or expired.
  Verify them, or run `python ../oauth-token-lib/oauth_token_lib.py` to confirm a token can
  be obtained.
- **`429 rate_limit_error` from OpenAI** — Each turn sends the full tool catalog as input
  tokens. Wait before retrying, use a model with more headroom, or raise your usage limits in
  the OpenAI dashboard.
- **OpenAI authentication errors** — Make sure `OPENAI_API_KEY` is set and valid.

## Learn more

- Predactiv MCP server: `https://mcp.predactiv.com`
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
- Model Context Protocol: https://modelcontextprotocol.io
