#!/usr/bin/env python3
"""
Update (or create) a single GitHub Actions repository secret via the REST API.
Generic, not Restream-specific - built for the rotating-refresh-token problem
(scripts/restream_analytics_pull.py) but reusable for any secret a workflow
needs to persist back to itself after a run.

Why this exists: some OAuth providers (Restream confirmed 2026-08-23) rotate
the refresh token on every use - the value a workflow starts with is dead by
the time it finishes, so the newly-issued one must be written back somewhere
persistent. GitHub Actions secrets are the obvious store, but the default
GITHUB_TOKEN a workflow run gets cannot manage secrets (no such permission
scope) - this requires a separate PAT with Secrets: read-and-write access to
this one repo (a fine-grained PAT scoped to just this repo is the least-
privilege option; a classic PAT needs the broader `repo` scope). Create it once
at github.com/settings/personal-access-tokens, store it as its own secret
(e.g. GH_SECRETS_PAT), and never let it appear in logs - this script never
prints it.

Per GitHub's documented API (docs.github.com/en/rest/actions/secrets): the
secret value must be encrypted client-side with the repo's public key
(libsodium sealed box) before it's sent - GitHub never sees the plaintext in
transit. Requires PyNaCl (pip install pynacl).

Usage:
    python3 scripts/gh-update-secret.py <SECRET_NAME> <value>
    echo -n "value" | python3 scripts/gh-update-secret.py <SECRET_NAME> -

Requires env vars:
    GH_SECRETS_PAT     - PAT with Secrets: read-and-write on this repo
    GH_REPO_OWNER      - e.g. fabcrowd
    GH_REPO_NAME       - e.g. Telcoin-Association-Agency
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request

try:
    from nacl import encoding, public
except ImportError:
    sys.exit(
        "FATAL: PyNaCl is not installed. Run: pip install pynacl\n"
        "(GitHub's own documented method for encrypting secrets for this API - "
        "see docs.github.com/en/rest/guides/encrypting-secrets-for-the-rest-api)"
    )


def env(name):
    v = os.environ.get(name)
    if not v:
        sys.exit(f"FATAL: {name} is not set.")
    return v


def api_request(url, pat, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode()) if r.length != 0 else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:400]
        hint = ""
        if e.code == 403:
            hint = (" - the PAT likely lacks 'Secrets: read and write' permission "
                     "on this repo (fine-grained PATs) or the 'repo' scope "
                     "(classic PATs).")
        sys.exit(f"FATAL: GitHub API {method} {url} failed ({e.code}): {detail}{hint}")


def encrypt_secret(public_key_b64, plaintext):
    public_key = public.PublicKey(public_key_b64.encode(), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(plaintext.encode())
    return base64.b64encode(encrypted).decode()


def main():
    if len(sys.argv) != 3:
        sys.exit(f"Usage: {sys.argv[0]} <SECRET_NAME> <value|->")

    secret_name = sys.argv[1]
    value = sys.stdin.read().rstrip("\n") if sys.argv[2] == "-" else sys.argv[2]
    if not value:
        sys.exit("FATAL: empty secret value - refusing to write an empty secret.")

    pat = env("GH_SECRETS_PAT")
    owner = env("GH_REPO_OWNER")
    repo = env("GH_REPO_NAME")

    base = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets"
    key_info = api_request(f"{base}/public-key", pat)
    encrypted_value = encrypt_secret(key_info["key"], value)

    api_request(f"{base}/{secret_name}", pat, method="PUT", body={
        "encrypted_value": encrypted_value,
        "key_id": key_info["key_id"],
    })
    print(f"Updated secret {secret_name} on {owner}/{repo}.")


if __name__ == "__main__":
    main()
