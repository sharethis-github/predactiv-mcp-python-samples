# Predactiv MCP — AI Agent Samples in Python

Sample code demonstrating how to connect AI agents to the **Predactiv MCP server**
(`https://mcp.predactiv.com`) from Python.

The [Predactiv Data Platform](https://predactiv.com) is exposed as a set of tools over the
[Model Context Protocol (MCP)](https://modelcontextprotocol.io). These samples show how to
authenticate, discover those tools at runtime, and let a large language model use them to
work with your audiences, datasets, datasources, destinations, and more.

## What the Predactiv MCP server can do

Predactiv MCP server (`https://mcp.predactiv.com`) turns the Predactiv Data Platform into an
AI agent-native toolset over MCP, letting an LLM go from raw data to modeled, deliverable
audiences without leaving the conversation. The toolset spans a few broad areas (and grows
over time):

- **Audience intelligence** — build, preview, and refine audience segments with live size
  estimates, then deliver them to downstream platforms. Segments can be assembled from
  natural-language intent, predictive signals, and rich filters.
- **Data + ML modeling** — datasets aren't just stored, they're activated. First-party data
  feeds a library of machine-learning models that enrich and expand reach: **audience
  enrichment**, **lookalike modeling**, **URL-similarity / contextual models**, and more —
  with the catalog of model types expanding over time.
- **Signals & discovery** — explore thousands of predictor signals, filter metadata, data
  sources, and delivery destinations (e.g. LiveRamp, The Trade Desk) to target precisely.
- **Insights** — surface demographic, behavioral, and geographic breakdowns of an audience
  with share and index analytics.

Tools are discovered dynamically at runtime (`tools/list`), so agents always see the latest
capabilities, and every call is OAuth2 bearer-authenticated — see
[`oauth-token-lib`](oauth-token-lib).

## What's in this repo

Each directory is a self-contained sample built on a different framework, plus a shared
authentication helper:

| Directory | What it shows | LLM |
| --- | --- | --- |
| [`langchain/`](langchain) | Agent built with [LangChain](https://python.langchain.com/) + `langchain-mcp-adapters`, client-side tool-calling loop | OpenAI |
| [`claude/`](claude) | Agent using [Anthropic Claude](https://www.anthropic.com/) via the native server-side MCP connector | Anthropic Claude |
| [`openai/`](openai) | Agent using [OpenAI](https://platform.openai.com/) GPT via the native server-side MCP connector | OpenAI |
| [`mcp-sdk/`](mcp-sdk) | Direct use of the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk), client-side tool-calling loop with no framework | OpenAI |
| [`oauth-token-lib/`](oauth-token-lib) | Shared OAuth2 authentication helper used by all samples | — |

## How the samples work

Every sample follows the same three steps:

1. **Authenticate** — [`oauth-token-lib`](oauth-token-lib) exchanges your `CLIENT_ID` and
   `CLIENT_SECRET` for an OAuth2 bearer token (client-credentials flow).
2. **Connect & discover tools** — the sample connects to the Predactiv MCP server over
   HTTP and fetches the available tools dynamically (nothing is hardcoded).
3. **Run the agent** — the MCP tools are bound to an LLM, which calls them to accomplish a
   natural-language goal.

> The [`claude/`](claude) and [`openai/`](openai) samples are a variation on steps 2–3:
> instead of fetching tools and running the loop client-side, they hand the MCP server
> definition to the provider's API (Anthropic's Messages API / OpenAI's Responses API), and
> the provider connects to the server and runs the tool-calling loop server-side. See each
> sample's README for details.

## Getting started

1. **Get credentials.** You'll need a Predactiv `CLIENT_ID` and `CLIENT_SECRET`.
   Contact [Predactiv](https://predactiv.com/contact-us/) if you don't have them.
2. **Pick a sample.** [`langchain/`](langchain) is a good starting point.
3. **Follow that sample's README** for setup, configuration, and run instructions.

```bash
cd langchain
pip install -r requirements.txt
export CLIENT_ID=your-predactiv-client-id
export CLIENT_SECRET=your-predactiv-client-secret
python agent.py
```

## Prerequisites

- Python 3.9+ (the [`mcp-sdk/`](mcp-sdk) sample requires Python 3.10+, per the MCP Python SDK)
- Predactiv OAuth2 API credentials (`CLIENT_ID` / `CLIENT_SECRET`)
- An LLM provider API key, depending on the sample:
  - `OPENAI_API_KEY` — [`langchain/`](langchain), [`openai/`](openai), [`mcp-sdk/`](mcp-sdk)
  - `ANTHROPIC_API_KEY` — [`claude/`](claude)

  See each sample's README for details.

## Learn more

- Predactiv: https://predactiv.com
- Predactiv MCP server: `https://mcp.predactiv.com`
- Predactiv OAuth2 token url: `https://platform-api.predactiv.com/v2/oauth/token`
- Model Context Protocol: https://modelcontextprotocol.io

## License

See [LICENSE](LICENSE).
