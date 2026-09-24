#!/usr/bin/env python3
"""Carry the LobeHub CLI session between workflow runs.

LobeHub rotates its refresh token on every refresh and refuses the old one, so a
static secret stops working after the first refresh. The workflow keeps the
CURRENT session in the Actions cache, encrypted with LOBEHUB_CREDENTIALS_KEY
(openssl AES-256, PBKDF2); LOBEHUB_CREDENTIALS_SEED only starts the chain.

    unpack   decrypt the cached session (or the seed) into ~/.lobehub-market
    due      exit 0 when the access token expires within two days (refresh it now)
    pack     encrypt the session for the cache if it changed; otherwise leave none
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys

ENCRYPTED = pathlib.Path(".lobehub-session.enc")
CREDENTIALS = pathlib.Path.home() / ".lobehub-market" / "user-credentials.json"
DIGEST = pathlib.Path.home() / ".lobehub-market" / ".unpacked.sha256"


def _openssl(extra: list[str], data: bytes) -> bytes:
    command = ["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", "200000", "-md", "sha256", *extra, "-pass", "env:LOBEHUB_CREDENTIALS_KEY"]
    return subprocess.run(command, input=data, capture_output=True, check=True).stdout


def unpack() -> int:
    source = "the cache" if ENCRYPTED.is_file() else "the seed"
    data = _openssl(["-d"], ENCRYPTED.read_bytes()) if ENCRYPTED.is_file() else os.environ["LOBEHUB_CREDENTIALS_SEED"].encode()
    json.loads(data)
    CREDENTIALS.parent.mkdir(parents=True, exist_ok=True)
    CREDENTIALS.write_bytes(data)
    os.chmod(CREDENTIALS, 0o600)
    DIGEST.write_text(hashlib.sha256(data).hexdigest(), encoding="utf-8")
    print("LobeHub session restored from", source)
    return 0


def due() -> int:
    expires = json.loads(CREDENTIALS.read_text(encoding="utf-8"))["expiresAt"].replace("Z", "+00:00")
    left = datetime.datetime.fromisoformat(expires) - datetime.datetime.now(datetime.timezone.utc)
    return 0 if left < datetime.timedelta(days=2) else 1


def pack() -> int:
    data = CREDENTIALS.read_bytes()
    if DIGEST.is_file() and DIGEST.read_text(encoding="utf-8") == hashlib.sha256(data).hexdigest():
        ENCRYPTED.unlink(missing_ok=True)
        print("LobeHub session unchanged; nothing to save")
        return 0
    ENCRYPTED.write_bytes(_openssl(["-salt"], data))
    print("LobeHub session rotated; saving it for the next run")
    return 0


if __name__ == "__main__":
    sys.exit({"unpack": unpack, "due": due, "pack": pack}[sys.argv[1]]())
