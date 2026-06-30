# Predactiv MCP — Python Samples

Sample code demonstrating how to connect AI agents to the **Predactiv MCP server**
(`https://mcp.predactiv.com`) from Python.

The [Predactiv](https://predactiv.com) data platform is exposed as a set of tools over the
[Model Context Protocol (MCP)](https://modelcontextprotocol.io). These samples show how to
authenticate, discover those tools at runtime, and let a large language model use them to
work with your audiences, datasets, datasources, destinations, and more.

## What's in this repo

Each directory is a self-contained sample built on a different framework, plus a shared
authentication helper:

| Directory | What it shows | Status |
| --- | --- | --- |
| [`langchain/`](langchain) | Agent built with [LangChain](https://python.langchain.com/) + `langchain-mcp-adapters` | ✅ Implemented |
| [`claude/`](claude) | Agent using [Anthropic Claude](https://www.anthropic.com/) via the native server-side MCP connector | ✅ Implemented |
| [`openai/`](openai) | Agent using OpenAI GPT | 🚧 Coming soon |
| [`mcp-sdk/`](mcp-sdk) | Direct use of the MCP Python SDK | 🚧 Coming soon |
| [`oauth-token-lib/`](oauth-token-lib) | Shared OAuth2 authentication helper used by all samples | ✅ Implemented |

## How the samples work

Every sample follows the same three steps:

1. **Authenticate** — [`oauth-token-lib`](oauth-token-lib) exchanges your `CLIENT_ID` and
   `CLIENT_SECRET` for an OAuth2 bearer token (client-credentials flow).
2. **Connect & discover tools** — the sample connects to the Predactiv MCP server over
   HTTP and fetches the available tools dynamically (nothing is hardcoded).
3. **Run the agent** — the MCP tools are bound to an LLM, which calls them to accomplish a
   natural-language goal.

> The [`claude/`](claude) sample is a variation on step 2–3: instead of fetching tools and
> running the loop client-side, it hands the MCP server definition to Anthropic's Messages
> API, and Claude connects to the server and runs the tool-calling loop server-side. See its
> [README](claude) for details.

## Getting started

1. **Get credentials.** You'll need a Predactiv `CLIENT_ID` and `CLIENT_SECRET`.
   Contact [Predactiv](https://predactiv.com) if you don't have them.
2. **Pick a sample.** Start with [`langchain/`](langchain), which is fully implemented.
3. **Follow that sample's README** for setup, configuration, and run instructions.

```bash
cd langchain
pip install -r requirements.txt
export CLIENT_ID=your-predactiv-client-id
export CLIENT_SECRET=your-predactiv-client-secret
python agent.py
```

## Prerequisites

- Python 3.9+
- Predactiv API credentials (`CLIENT_ID` / `CLIENT_SECRET`)
- An LLM provider API key, depending on the sample (e.g. `OPENAI_API_KEY` for the
  LangChain sample, `ANTHROPIC_API_KEY` for the Claude sample). See each sample's README
  for details.

## Learn more

- Predactiv: https://predactiv.com
- Predactiv MCP server: `https://mcp.predactiv.com`
- Predactiv OAuth2 token url: `https://platform-api.predactiv.com/v2/oauth/token`
- Model Context Protocol: https://modelcontextprotocol.io

## License

See [LICENSE](LICENSE).
