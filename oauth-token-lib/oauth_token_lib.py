"""Predactiv oauth2 authentication

Reads CLIENT_ID and CLIENT_SECRET from the environment variables, exchanges them for a
bearer access token at the Predactiv OAuth server, and returns the token
back so that agents can authenticate against the MCP server.

Usage:
    from oauth_token_lib import get_bearer_token, auth_headers

    token = get_bearer_token()                 # raw access token string
    headers = auth_headers()                   # {"Authorization": "Bearer ..."}
"""

import os
import time
import requests

PREDACTIV_TOKEN_URL = "https://platform-api.predactiv.com/v2/oauth/token"

# Simple in-process cache so repeated calls within one run reuse the token
# until shortly before it expires.
_cached_token = None
_cached_expiry = 0.0

def get_bearer_token(force_refresh=False):
    """Return a valid bearer access token using the client-credentials grant.

    CLIENT_ID and CLIENT_SECRET are read from the environment. The token is
    cached in-process and refreshed automatically once it is within 60 seconds
    of expiry (or when force_refresh=True).
    """
    global _cached_token, _cached_expiry

    if not force_refresh and _cached_token and time.time() < _cached_expiry - 60:
        return _cached_token

    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError(
            "CLIENT_ID and CLIENT_SECRET environment variables must be set."
        )

    data = {"grant_type": "client_credentials"}

    # Credentials are sent via HTTP Basic auth (client_secret_basic), the
    # OAuth2 default for the client-credentials grant.
    response = requests.post(
        PREDACTIV_TOKEN_URL,
        data=data,
        auth=(client_id, client_secret),
        headers={"Accept": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    token = payload.get("access_token")
    if not token:
        raise RuntimeError(f"Token endpoint did not return an access_token: {payload}")

    expires_in = payload.get("expires_in", 3600)
    _cached_token = token
    _cached_expiry = time.time() + float(expires_in)
    return token


def auth_headers():
    """Return a ready-to-use Authorization header dict for the MCP server."""
    return {"Authorization": f"Bearer {get_bearer_token()}"}


if __name__ == "__main__":
    # Quick manual check: prints the token (truncated) when run directly.
    tok = get_bearer_token()
    print(f"Got bearer token: {tok[:12]}... (length {len(tok)})")
