#!/usr/bin/env python3
"""Mirror this repository's listing from the live EmpirioLabs MCP server.

The server (https://mcp.empiriolabs.ai) follows the EmpirioLabs documentation by
itself and renders these files at /listing.json from its live tool surface. This
script writes them here; the workflow commits any change and refreshes the stores
that keep their own copy of the tools (Smithery, LobeHub).
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
import urllib.request

URL = os.environ.get("LISTING_URL", "https://mcp.empiriolabs.ai/listing.json")
MIN_TOOLS = 20
ROOT = pathlib.Path(__file__).resolve().parents[1]
PROTECTED = {".git", ".github", "scripts"}


def main() -> int:
    request = urllib.request.Request(URL, headers={"User-Agent": "EmpirioLabs-listing-follow/1.0", "Cache-Control": "no-cache"})
    with urllib.request.urlopen(request, timeout=60) as response:
        body = json.load(response)
    files, tools = body.get("files"), body.get("tools")
    if not isinstance(files, dict) or not files or not isinstance(tools, int) or tools < MIN_TOOLS:
        print(f"refusing an implausible listing (tools={tools!r})")
        return 1
    changed = []
    for relative, content in sorted(files.items()):
        path = pathlib.PurePosixPath(relative)
        if path.is_absolute() or ".." in path.parts or path.parts[0] in PROTECTED or not isinstance(content, str):
            print(f"refusing path {relative!r}")
            return 1
        target = ROOT / path
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
