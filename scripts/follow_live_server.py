#!/usr/bin/env python3
"""Mirror this repository's listing from the live EmpirioLabs MCP server.

The server (https://mcp.empiriolabs.ai) follows the EmpirioLabs documentation by
itself and renders these files at /listing.json from its live tool surface. This
script writes them here; the workflow commits any change and refreshes the stores
that keep their own copy of the tools (Smithery, LobeHub, the MCP registry).

The stores, plugin directories and the registry act on these files without a
human in between, so a listing is refused unless every link in it points at
EmpirioLabs, its GitHub organisation or a fixed schema host, and server.json
names our server at our endpoint.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import sys
import urllib.parse
import urllib.request

URL = os.environ.get("LISTING_URL", "https://mcp.empiriolabs.ai/listing.json")
MIN_TOOLS = 20
ROOT = pathlib.Path(__file__).resolve().parents[1]
PROTECTED = {".git", ".github", "scripts", "node_modules"}
SERVER_NAME = "ai.empiriolabs/mcp"
SERVER_ENDPOINT = "https://mcp.empiriolabs.ai/mcp"
OWN_DOMAIN = "empiriolabs.ai"
# Schema, consent and protocol hosts the listing links to on purpose.
OTHER_HOSTS = {
    "agent-plugins.org",
    "global.consent.azure-apim.net",
    "modelcontextprotocol.io",
    "registry.modelcontextprotocol.io",
    "static.modelcontextprotocol.io",
}
LINK = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*://[^\s()<>\"'`\]]+")


def foreign_link(link: str) -> bool:
    parts = urllib.parse.urlsplit(link.rstrip(".,;:!?"))
    host = (parts.hostname or "").rstrip(".").lower()
    if parts.scheme != "https":
        return True
    if host == OWN_DOMAIN or host.endswith("." + OWN_DOMAIN) or host in OTHER_HOSTS:
        return False
    return not (host == "github.com" and parts.path.startswith("/EmpirioLabs-AI/"))


def server_problem(text: str) -> str:
    """Why server.json cannot be ours, or an empty string."""
    try:
        manifest = json.loads(text)
    except ValueError:
        return "server.json is not JSON"
    remotes = manifest.get("remotes") or []
    if manifest.get("name") != SERVER_NAME:
        return f"server.json names {manifest.get('name')!r}"
    if not remotes or any(not isinstance(r, dict) or r.get("url") != SERVER_ENDPOINT for r in remotes):
        return "server.json points somewhere other than " + SERVER_ENDPOINT
    if manifest.get("packages"):
        return "server.json lists packages; the server is remote only"
    return ""


def main() -> int:
    request = urllib.request.Request(URL, headers={"User-Agent": "EmpirioLabs-listing-follow/1.0", "Cache-Control": "no-cache"})
    with urllib.request.urlopen(request, timeout=60) as response:
        body = json.load(response)
    files, tools = body.get("files"), body.get("tools")
    if not isinstance(files, dict) or not files or type(tools) is not int or tools < MIN_TOOLS:
        print(f"refusing an implausible listing (tools={tools!r})")
        return 1
    for relative, content in sorted(files.items()):
        path = pathlib.PurePosixPath(relative)
        if not path.parts or path.is_absolute() or ".." in path.parts or path.parts[0] in PROTECTED or not isinstance(content, str):
            print(f"refusing path {relative!r}")
            return 1
        foreign = sorted({link for link in LINK.findall(content) if foreign_link(link)})
        if foreign:
            print(f"refusing {relative}: links outside EmpirioLabs: {', '.join(foreign[:5])}")
            return 1
    problem = server_problem(files.get("server.json", ""))
    if problem:
        print(f"refusing the listing: {problem}")
        return 1
    changed = []
    for relative, content in sorted(files.items()):
        target = ROOT / pathlib.PurePosixPath(relative)
        if target.is_file() and target.read_text(encoding="utf-8") == content:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        changed.append(relative)
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(f"changed={'true' if changed else 'false'}\ntools={tools}\n")
    print(f"{len(changed)} file(s) changed; the live server has {tools} tools" + (": " + ", ".join(changed) if changed else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
