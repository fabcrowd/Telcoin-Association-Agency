#!/usr/bin/env python3
"""
ONE-TIME step to connect the Restream account for the analytics puller
(scripts/restream_analytics_pull.py). Standard OAuth2 authorization-code flow per
developers.restream.io/guide/getting-started - no PKCE documented, so none is used
here (unlike scripts/x_oauth_setup.py, which does need it for X's API).

Requires a Restream App (developers.restream.io/apps) with a registered
Callback/Redirect URI. Set as env vars first:
  RESTREAM_CLIENT_ID, RESTREAM_CLIENT_SECRET   - from the app's credentials page
  RESTREAM_REDIRECT_URI                        - must exactly match the app's
                                                  registered redirect URI
                                                  (nothing needs to be listening
                                                  there)

Usage:
  Step 1: python3 scripts/restream_oauth_setup.py authorize
          -> prints a URL. Open it, log in, click Authorize.
             The browser redirects to a URL that fails to load - expected,
             nothing is listening at RESTREAM_REDIRECT_URI. Copy the full
             resulting address-bar URL (or just its code=... value).

  Step 2: python3 scripts/restream_oauth_setup.py exchange "<code or full redirect url>"
          -> exchanges the code for tokens and prints the refresh token to store
             as RESTREAM_REFRESH_TOKEN. Last manual step, ever - the puller
             refreshes automatically from here on (if Restream's tokens don't
             rotate/expire the way X's do; verify this on first live run - see
             the note in restream_analytics_pull.py).
"""
import os
import re
import sys
import json
import urllib.parse
import urllib.request
import urllib.error

AUTH_URL = "https://api.restream.io/login"
TOKEN_URL = "https://api.restream.io/oauth/token"
SCOPES = ""  # Restream's docs page didn't enumerate discrete scope strings in
             # what this research could render (JS-rendered docs site) - leave
             # blank (app-level default scopes) unless a live test shows otherwise.


def env(name):
    v = os.environ.get(name)
    if not v:
        print(f"Missing required env var: {name}", file=sys.stderr)
        sys.exit(1)
    return v


def cmd_authorize():
    client_id = env("RESTREAM_CLIENT_ID")
    redirect_uri = env("RESTREAM_REDIRECT_URI")
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
    }
    if SCOPES:
        params["scope"] = SCOPES
    url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    print("\nOpen this URL, log in, and click Authorize:\n")
    print(url)
    print("\nThe browser will then redirect to a URL that fails to load - that's "
          "expected, nothing is listening at RESTREAM_REDIRECT_URI. Copy the FULL "
          "resulting URL from the address bar (or just the code=... value) and run:\n")
    print(f'  python3 {sys.argv[0]} exchange "<paste here>"\n')
    print("NOTE: AUTH_URL (api.restream.io/login) is a best-effort guess from "
          "general OAuth2 docs, not confirmed against Restream's exact endpoint - "
          "this research could not fully render developers.restream.io's JS-based "
          "docs. If this 404s, check developers.restream.io/guide/getting-started "
          "directly in a browser for the exact authorize URL.", file=sys.stderr)


def cmd_exchange(raw):
    client_id = env("RESTREAM_CLIENT_ID")
    client_secret = env("RESTREAM_CLIENT_SECRET")
    redirect_uri = env("RESTREAM_REDIRECT_URI")

    m = re.search(r"[?&]code=([^&]+)", raw)
    code = urllib.parse.unquote(m.group(1)) if m else raw.strip()

    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()

    req = urllib.request.Request(TOKEN_URL, data=data, method="POST", headers={
        "Content-Type": "application/x-www-form-urlencoded",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            tokens = json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"Token exchange failed ({e.code}): {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

    print("\nConnected. Store these as persistent secrets:\n")
    print(f"RESTREAM_ACCESS_TOKEN={tokens.get('access_token')}")
    if "refresh_token" in tokens:
        print(f"RESTREAM_REFRESH_TOKEN={tokens.get('refresh_token')}")
    else:
        print("NOTE: no refresh_token in the response - Restream's access tokens "
              "may not expire the way X's do (unconfirmed). If restream_analytics_pull.py "
              "starts failing with 401s later, this token needs re-issuing via this "
              "script again - there may be no refresh flow to automate that away.")
    print(f"\n(expires_in: {tokens.get('expires_in', 'not specified')}s)")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("authorize", "exchange"):
        print(__doc__)
        sys.exit(1)
    if sys.argv[1] == "authorize":
        cmd_authorize()
    else:
        if len(sys.argv) < 3:
            print('Usage: exchange "<code or full redirect url>"', file=sys.stderr)
            sys.exit(1)
        cmd_exchange(sys.argv[2])
