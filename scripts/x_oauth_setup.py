#!/usr/bin/env python3
"""
ONE-TIME step to connect @telcoinTAO's X account for fully automated performance
data - the only manual action anywhere in this pipeline. It's the same "Connect
your X account" click every competitor product (Buffer, Typefully, Hootsuite)
requires during onboarding - a platform-level requirement for releasing private
analytics data to any third party, not something this agency can shortcut.

After this one grant, scripts/x_api_fetch.py refreshes and rotates the token on
every run, forever, with zero human involvement.

Requires an X Developer App (developer.x.com) with OAuth 2.0 enabled, "Read"
permissions, and a registered Callback URI. Set as env vars first:
  X_CLIENT_ID, X_CLIENT_SECRET   - from the app's "Keys and tokens" page
  X_REDIRECT_URI                 - must exactly match the app's registered
                                    Callback URI, e.g. http://localhost:8080/callback
                                    (nothing needs to actually be listening there)

Usage:
  Step 1: python3 scripts/x_oauth_setup.py authorize
          -> prints a URL. Open it, log in as @telcoinTAO, click Authorize.
             The browser will redirect to a URL that fails to load - that's
             expected, nothing is listening at X_REDIRECT_URI. Copy the full
             resulting address-bar URL (or just its code=... value).

  Step 2: python3 scripts/x_oauth_setup.py exchange "<code or full redirect url>"
          -> exchanges the code for a refresh token and prints it. Store that as
             X_REFRESH_TOKEN (a persistent secret/env var). This is the last
             manual step, ever.
"""
import base64
import hashlib
import os
import re
import secrets
import sys
import urllib.parse
import urllib.request
import json

AUTH_URL = "https://x.com/i/oauth2/authorize"
TOKEN_URL = "https://api.x.com/2/oauth2/token"
SCOPES = "tweet.read users.read offline.access"
VERIFIER_FILE = ".x_oauth_verifier"


def env(name):
    v = os.environ.get(name)
    if not v:
        print(f"Missing required env var: {name}", file=sys.stderr)
        sys.exit(1)
    return v


def make_pkce():
    verifier = secrets.token_urlsafe(64)[:128]
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    return verifier, challenge


def cmd_authorize():
    client_id = env("X_CLIENT_ID")
    redirect_uri = env("X_REDIRECT_URI")
    verifier, challenge = make_pkce()
    with open(VERIFIER_FILE, "w") as f:
        f.write(verifier)
    state = secrets.token_urlsafe(16)
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": SCOPES,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    print("\nOpen this URL, log in as the account to connect, and click Authorize:\n")
    print(url)
    print("\nThe browser will then redirect to a URL that fails to load (nothing is "
          "listening there) - that's expected. Copy the FULL resulting URL from the "
          "address bar (or just the code=... value) and run:\n")
    print(f'  python3 {sys.argv[0]} exchange "<paste here>"\n')


def cmd_exchange(raw):
    client_id = env("X_CLIENT_ID")
    client_secret = env("X_CLIENT_SECRET")
    redirect_uri = env("X_REDIRECT_URI")
    if not os.path.exists(VERIFIER_FILE):
        print("No verifier on disk - run the 'authorize' step first, in this same "
              "working directory.", file=sys.stderr)
        sys.exit(1)
    verifier = open(VERIFIER_FILE).read().strip()

    m = re.search(r"[?&]code=([^&]+)", raw)
    code = urllib.parse.unquote(m.group(1)) if m else raw.strip()

    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": verifier,
    }).encode()

    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    req = urllib.request.Request(TOKEN_URL, data=data, method="POST", headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_header}",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            tokens = json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"Token exchange failed ({e.code}): {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

    os.remove(VERIFIER_FILE)
    print("\nConnected. Store this as X_REFRESH_TOKEN (a persistent secret/env var) - "
          "this is the last manual step. scripts/x_api_fetch.py refreshes and rotates "
          "it automatically from every run on:\n")
    print(tokens["refresh_token"])
    print(f"\n(An access token was also issued, expires in {tokens.get('expires_in')}s - "
          "that one was just a smoke test; the daily fetcher gets its own each run.)")


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
