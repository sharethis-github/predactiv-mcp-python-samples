# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

A collection of self-contained Python samples showing how to drive the **Predactiv MCP server** (`https://mcp.predactiv.com`) as a set of AI-agent tools from different frameworks and SDKs. Each top-level directory is one sample. All samples are implemented.

- `claude/` — Anthropic Claude via its **native server-side MCP connector** (LLM: Claude)
- `openai/` — OpenAI GPT via its **native server-side MCP connector** (Responses API; LLM: OpenAI)
- `langchain/` — LangChain `create_agent` + `langchain-mcp-adapters`, **client-side** loop (LLM: OpenAI)
- `mcp-sdk/` — raw MCP Python SDK with a hand-written **client-side** tool-calling loop (LLM: OpenAI)
- `oauth-token-lib/` — shared, locally-installed package handling Predactiv OAuth2 auth

> Two architectural patterns are represented. **Client-side** samples (`langchain/`, `mcp-sdk/`) connect to the MCP server themselves, fetch tools, and run the tool-calling loop in your process. **Server-side connector** samples (`claude/`, `openai/`) hand the MCP server definition to the provider's API and let the provider run the loop. `langchain/agent.py` is the simplest client-side reference; `mcp-sdk/agent.py` shows the same loop without a framework.

## Architecture

All samples share the same auth layer; they differ in **who runs the MCP connection and tool loop**.

1. **Auth (shared)** — `oauth_token_lib` performs an OAuth2 **client-credentials** exchange against `https://platform-api.predactiv.com/v2/oauth/token` using `CLIENT_ID`/`CLIENT_SECRET` from the environment, and caches the token in-process until ~60s before expiry. It exposes `get_bearer_token()` (raw token string) and `auth_headers()` (`{"Authorization": "Bearer <token>"}`). This package is the single source of truth for authentication — all samples depend on it rather than re-implementing the token exchange. The MCP server is **stateless** (no `Mcp-Session-Id`) and every tool requires the OAuth bearer token.

2. **MCP connection + agent loop** — two patterns:
   - **Client-side** (`langchain/`, `mcp-sdk/`) — the sample connects to `https://mcp.predactiv.com` over HTTP, fetches tools dynamically (`tools/list`), converts them to the LLM's tool format, and runs the call → execute-tool → feed-result loop in-process. `mcp-sdk/` uses `streamable_http_client` + `ClientSession` and a hand-written loop; `langchain/` uses `MultiServerMCPClient` + `create_agent`, which hide the loop.
   - **Server-side connector** (`claude/`, `openai/`) — the sample passes the MCP server definition (URL + bearer token) to the provider's API (Anthropic Messages API `mcp_servers`/`mcp_toolset` + `mcp-client-2025-11-20` beta; OpenAI Responses API `mcp` tool), and the provider connects to the server and runs the tool loop. The sample makes a single API call and reads the final answer.

The Predactiv MCP tools expose the data platform: audiences, datasets, datasources, destinations, filters/predictors, and insights (`predactiv_*` tool families).

## Setup & Running

Each sample is run from inside its own directory. Using `langchain` as the template:

```bash
cd langchain
pip install -r requirements.txt   # also installs ../oauth-token-lib in editable mode (-e)
export CLIENT_ID=...               # Predactiv OAuth (all samples)
export CLIENT_SECRET=...
export OPENAI_API_KEY=...          # langchain/, openai/, mcp-sdk/
# export ANTHROPIC_API_KEY=...     # claude/ instead of OPENAI_API_KEY
python agent.py
```

Each sample needs the Predactiv `CLIENT_ID`/`CLIENT_SECRET` **plus** its LLM provider key: `OPENAI_API_KEY` for `langchain/`, `openai/`, and `mcp-sdk/`; `ANTHROPIC_API_KEY` for `claude/`. Note `mcp-sdk/` requires Python 3.10+ (MCP Python SDK); the others run on 3.9+.

Verify auth independently (prints a truncated token):

```bash
cd oauth-token-lib && python oauth_token_lib.py
```

## Conventions for new samples

- Reuse `oauth_token_lib` for auth; do not re-implement the token exchange. Add `-e ../oauth-token-lib` to the sample's `requirements.txt`. Use `auth_headers()` for client-side HTTP connections and `get_bearer_token()` when a connector wants the raw token.
- Keep the MCP server URL (`https://mcp.predactiv.com`) and a `GOAL` prompt as module-level constants, mirroring the existing samples.
- For client-side samples, fetch tools dynamically from the server (`tools/list`); do not hardcode the tool list. For connector samples, let the provider discover the tools.
- Each sample directory has its own `README.md` following a shared structure (How it works → Prerequisites → Setup → Configuration → Run → Troubleshooting → Learn more). Keep new samples consistent with it, and update the root `README.md` sample table.
