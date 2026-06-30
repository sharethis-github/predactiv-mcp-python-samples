# Predactiv MCP - Anthropic Claude as AI Agent

Drives the [Predactiv MCP server](https://mcp.predactiv.com) as a set of agent tools using **Anthropic Claude** directly.

Unlike a client-side agent loop, this sample uses Claude's **native MCP connector**: the MCP server definition is handed to the Messages API, and Anthropic's infrastructure connects to the server, discovers its tools, and runs the tool-calling loop server-side. Your code makes a single `messages.create` call and reads back the final answer.

## How it works

1. **Auth** — `oauth_token_lib.get_bearer_token()` performs the Predactiv OAuth2 client-credentials exchange and returns a bearer token. This token is passed to the MCP server as `authorization_token`.
2. **MCP connection** — the `mcp_servers` parameter declares the Predactiv server (`type`, `name`, `url`, `authorization_token`). The matching `mcp_toolset` entry in `tools` (linked by `mcp_server_name`) enables those tools for the model.
3. **Agent loop** — Claude connects to the MCP server, lists its tools, calls them as needed, and returns a final response. The `mcp-client-2025-11-20` beta flag enables the connector.

The Predactiv MCP tools expose the data platform: audiences, datasets, datasources, destinations, filters/predictors, and insights (`predactiv_*` tool families).

## Setup

Run from inside this directory:

```bash
cd claude
pip install -r requirements.txt   # also installs ../oauth-token-lib in editable mode (-e)
```

Set the required environment variables:

```bash
export ANTHROPIC_API_KEY=sk-ant-...   # Anthropic API key (for calling Claude)
export CLIENT_ID=...                   # Predactiv OAuth client ID (for the MCP server)
export CLIENT_SECRET=...               # Predactiv OAuth client secret
```

> **Two separate credentials.** `ANTHROPIC_API_KEY` authenticates your calls to Claude. `CLIENT_ID` / `CLIENT_SECRET` authenticate to the Predactiv MCP server via `oauth_token_lib`. Both must be set.

## Running

```bash
python agent.py
```

The script sends the `GOAL` prompt (defined at the top of `agent.py`) and prints Claude's final text response. Edit `GOAL` to change the task.

Verify Predactiv auth independently:

```bash
cd ../oauth-token-lib && python oauth_token_lib.py
```

## Configuration

Both constants live at the top of `agent.py`:

- `PREDACTIV_MCP_SERVER_URL` — the MCP server endpoint (`https://mcp.predactiv.com`).
- `GOAL` — the prompt sent to the agent.

The Claude model is set in the `messages.create` call (`model="claude-haiku-4-5"`). Use a more capable model (e.g. `claude-sonnet-4-6`, `claude-opus-4-8`) if your task needs it.

## Notes

- **`response.content` is a mixed list of blocks** (MCP tool-use, tool-result, and text). The sample joins only the `text` blocks to build the final answer — don't assume `content[0]` is text.
- **Rate limits are per input-token-per-minute (ITPM).** The MCP connector injects the server's full tool catalog into each request as input tokens, so a single call can be large. If you hit a `429`, wait ~60 seconds between runs, restrict the loaded tools, or request a limit increase at <https://console.anthropic.com/settings/limits>.
