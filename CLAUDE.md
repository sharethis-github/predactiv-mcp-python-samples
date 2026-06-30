# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

A collection of self-contained Python samples showing how to drive the **Predactiv MCP server** (`https://mcp.predactiv.com`) as a set of agent tools from different AI agent frameworks. Each top-level directory is one framework's sample and shares the same shape:

- `claude/` — Anthropic Claude as the agent (stub, not yet implemented)
- `langchain/` — LangChain `create_agent` + `langchain-mcp-adapters` (the only fully implemented sample)
- `mcp-sdk/` — raw MCP Python SDK (stub)
- `openai/` — OpenAI GPT as the agent (stub)
- `oauth-token-lib/` — shared, locally-installed package handling Predactiv OAuth2 auth

> Note: `claude/agent.py`, `mcp-sdk/agent.py`, and `openai/agent.py` are currently empty placeholders. `langchain/agent.py` is the reference implementation to model new samples on.

## Architecture

Every sample follows the same three-layer flow:

1. **Auth** — `oauth_token_lib.auth_headers()` returns `{"Authorization": "Bearer <token>"}`. It performs an OAuth2 **client-credentials** exchange against `https://platform-api.predactiv.com/v2/oauth/token` using `CLIENT_ID`/`CLIENT_SECRET` from the environment, and caches the token in-process until ~60s before expiry. This package is the single source of truth for authentication — all framework samples depend on it rather than re-implementing the token exchange.
2. **MCP connection** — the sample connects to `https://mcp.predactiv.com` over HTTP transport, passing the bearer header from step 1. The MCP server is **stateless** (no `Mcp-Session-Id`) and every tool requires the OAuth bearer token. Tools are fetched dynamically from the server (`tools/list`) rather than hardcoded.
3. **Agent loop** — the framework converts the fetched MCP tools into its native tool format, binds them to an LLM, and runs a goal prompt.

The Predactiv MCP tools expose the data platform: audiences, datasets, datasources, destinations, filters/predictors, and insights (`predactiv_*` tool families).

## Setup & Running

Each sample is run from inside its own directory. Using `langchain` as the template:

```bash
cd langchain
pip install -r requirements.txt   # also installs ../oauth-token-lib in editable mode (-e)
export CLIENT_ID=...
export CLIENT_SECRET=...
python agent.py
```

Verify auth independently (prints a truncated token):

```bash
cd oauth-token-lib && python oauth_token_lib.py
```

## Conventions for new samples

- Reuse `oauth_token_lib` for auth; do not re-implement the token exchange. Add `-e ../oauth-token-lib` to the sample's `requirements.txt`.
- Keep the MCP server URL (`https://mcp.predactiv.com`) and a `GOAL` prompt as module-level constants, mirroring `langchain/agent.py`.
- Fetch tools dynamically from the server; do not hardcode the tool list.
