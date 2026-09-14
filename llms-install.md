# Installing the EmpirioLabs AI MCP server

This is a remote (hosted) MCP server. Nothing is downloaded or built; the client connects to `https://mcp.empiriolabs.ai/mcp` over Streamable HTTP.

## Credentials

Use either of these:

1. **OAuth** (recommended for Claude, ChatGPT and other clients with a browser sign-in): connect the URL and approve the request on the EmpirioLabs consent screen. No client id or secret is needed.
2. **API key**: create a key at https://platform.empiriolabs.ai (API keys page) and send it as a bearer token.

The API key must never be pasted into chat. Put it in the client's configuration file or an environment variable.

## Cline

Add the server to `cline_mcp_settings.json` (open it from the MCP Servers panel, **Configure MCP Servers**):

```json
{
  "mcpServers": {
    "empiriolabs": {
      "type": "streamableHttp",
      "url": "https://mcp.empiriolabs.ai/mcp",
      "headers": {
        "Authorization": "Bearer ${EMPIRIOLABS_API_KEY}"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Replace `${EMPIRIOLABS_API_KEY}` with the key, or export it in the environment Cline runs in. Reload the MCP servers list; the tools appear under `empiriolabs`.

## Cursor, Windsurf, Gemini CLI

```json
{
  "mcpServers": {
    "empiriolabs": {
      "url": "https://mcp.empiriolabs.ai/mcp",
      "headers": {
        "Authorization": "Bearer sk-empiriolabs-your_key_here"
      }
    }
  }
}
```

## VS Code (`.vscode/mcp.json`)

```json
{
  "servers": {
    "empiriolabs": {
      "type": "http",
      "url": "https://mcp.empiriolabs.ai/mcp",
      "headers": {
        "Authorization": "Bearer sk-empiriolabs-your_key_here"
      }
    }
  }
}
```

## Claude Code and Codex CLI

```bash
claude mcp add --transport http empiriolabs https://mcp.empiriolabs.ai/mcp
codex mcp add empiriolabs --url https://mcp.empiriolabs.ai/mcp
```

## Verify

Call `get_platform_status` (no credits) and `list_models` (no credits). A tool that runs a model, for example `chat`, uses the account's prepaid credits.

Documentation: https://docs.empiriolabs.ai/mcp. Support: support@empiriolabs.ai.
