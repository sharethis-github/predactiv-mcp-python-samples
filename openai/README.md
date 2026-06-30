# Predactiv MCP — OpenAI GPT AI Agent

This sample shows how to connect an AI agent to the **Predactiv MCP server** using
[OpenAI](https://platform.openai.com/) and its [Responses API](https://platform.openai.com/docs/api-reference/responses).

Unlike a client-side agent loop, this sample uses OpenAI's **native MCP connector**: the
MCP server definition is handed to the Responses API, and OpenAI's infrastructure connects
to the server, discovers its tools, and runs the tool-calling loop server-side. Your code
makes a single `responses.create` call and reads back the final answer.

## How it works

1. **Authenticate** — `oauth_token_lib.get_bearer_token()` exchanges your `CLIENT_ID` and
   `CLIENT_SECRET` for an OAuth2 bearer token (client-credentials flow).
2. **Connect & discover tools** — the request declares the Predactiv server as an `mcp`
   tool (`server_label`, `server_url`, `authorization`). OpenAI connects to the server and
   discovers its tools dynamically. No tools are hardcoded.
3. **Run the agent** — GPT connects to the MCP server, calls its tools as needed, and
   returns a final response. `require_approval: "never"` lets the model call the tools
   without a manual approval round-trip.

The Predactiv MCP tools expose the data platform: audiences, datasets, datasources,
destinations, filters/predictors, and insights (`predactiv_*` tool families).

## Prerequisites

- Python 3.9+
- A Predactiv account with API credentials (`CLIENT_ID` and `CLIENT_SECRET`).
  Contact Predactiv if you don't have these.
- An [OpenAI API key](https://platform.openai.com/) — this sample uses `gpt-5.4-mini` as
  the agent's LLM. Set it as the `OPENAI_API_KEY` environment variable.

> **Two separate credentials.** `OPENAI_API_KEY` authenticates your calls to OpenAI.
> `CLIENT_ID` / `CLIENT_SECRET` authenticate to the Predactiv MCP server via
> `oauth_token_lib`. Both must be set.

## Setup

From this `openai/` directory:

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

Edit the `GOAL` constant in [`agent.py`](agent.py) to ask the agent to do something else
with your Predactiv data. The model is set in the `responses.create` call
(`model="gpt-5.4-mini"`) — swap it for any model your key can access.

## Troubleshooting

- **`Responses.create() got an unexpected keyword argument 'messages'`** — The Responses
  API uses `input`, not `messages` (that's the Chat Completions API). Pass `input=GOAL`.
- **`401 Unauthorized` from the MCP server** — The `authorization` field expects the raw
  access token; OpenAI adds the `Authorization: Bearer …` header itself. Don't prefix the
  token with `Bearer ` (a double prefix causes a 401). If it persists, verify your
  credentials with `python ../oauth-token-lib/oauth_token_lib.py`.
- **`output_text` is empty** — The model likely stopped on an `mcp_approval_request`
  without calling the tool. Set `require_approval: "never"` on the MCP tool. The sample
  also dumps `response.output` items when there's no text, so you can see what came back.
- **OpenAI authentication errors** — Make sure `OPENAI_API_KEY` is set and valid.

## Learn more

- Predactiv MCP server: `https://mcp.predactiv.com`
- OpenAI Responses API: https://platform.openai.com/docs/api-reference/responses
- Model Context Protocol: https://modelcontextprotocol.io
