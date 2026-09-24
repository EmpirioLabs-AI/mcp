#!/usr/bin/env python3
"""Decide whether server.json holds a version the official MCP registry lacks.

The registry keeps every published version permanently and refuses to publish
the same version twice, so the workflow publishes only when this reports a new
one. It never publishes by itself and needs no credential.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = "https://registry.modelcontextprotocol.io/v0.1/servers"


def main() -> int:
    manifest = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))
    name, version = manifest["name"], manifest["version"]
    url = f"{REGISTRY}/{urllib.parse.quote(name, safe='')}/versions"
    request = urllib.request.Request(url, headers={"User-Agent": "EmpirioLabs-listing-follow/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        published = {entry.get("server", {}).get("version") for entry in json.load(response).get("servers", [])}
    new = version not in published
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(f"publish={'true' if new else 'false'}\nversion={version}\n")
    print(f"{name} {version}: " + ("new, will publish" if new else "already in the registry"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
