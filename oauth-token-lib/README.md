# Predactiv OAuth2 Token Library

A small, dependency-light Python helper that authenticates to Predactiv using the
OAuth2 **client-credentials** flow and returns a bearer token for calling the
[Predactiv MCP server](https://mcp.predactiv.com).

The other samples in this repository (e.g. [`../langchain`](../langchain)) depend on
this package for authentication, so they don't have to re-implement the token exchange.

## What it does

- Reads your `CLIENT_ID` and `CLIENT_SECRET` from environment variables.
- Exchanges them for an access token at the Predactiv token endpoint
  (`https://platform-api.predactiv.com/v2/oauth/token`) using HTTP Basic auth
  (`client_secret_basic`).
- Caches the token in-process and automatically refreshes it once it is within
  60 seconds of expiry, so repeated calls in the same run reuse the same token.

## Installation

```bash
pip install -e .
```

Installing in editable mode (`-e`) is what the framework samples do via their
`requirements.txt`. The only runtime dependency is [`requests`](https://pypi.org/project/requests/).

## Configuration

Set your Predactiv API credentials as environment variables:

```bash
export CLIENT_ID=your-predactiv-client-id
export CLIENT_SECRET=your-predactiv-client-secret
```

Don't have credentials? Contact Predactiv to obtain them.

## Usage

```python
from oauth_token_lib import get_bearer_token, auth_headers

# Raw access token string
token = get_bearer_token()

# Ready-to-use Authorization header for HTTP / MCP requests
headers = auth_headers()
# -> {"Authorization": "Bearer eyJhbGciOi..."}
```

### API

| Function | Description |
| --- | --- |
| `get_bearer_token()` | Returns a valid access token string. Pass `force_refresh=True` to bypass the cache and fetch a new token. |
| `auth_headers()` | Returns `{"Authorization": "Bearer <token>"}`, ready to pass as request headers. |

## Verify your setup

Run the module directly to confirm your credentials work. It prints a truncated
token on success:

```bash
python oauth_token_lib.py
# Got bearer token: eyJhbGciOi... (length 1234)
```

## Troubleshooting

- **`CLIENT_ID and CLIENT_SECRET environment variables must be set.`** — Export both
  variables before running.
- **`401 Unauthorized` / HTTP error from the token endpoint** — Your `CLIENT_ID` or
  `CLIENT_SECRET` is incorrect or revoked. Double-check the values with Predactiv.
- **`Token endpoint did not return an access_token`** — The credentials were accepted
  but no token was issued; contact Predactiv if this persists.
