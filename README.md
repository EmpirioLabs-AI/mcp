<p align="center">
  <img src="icon-dark-256.png" width="128" height="128" alt="EmpirioLabs AI">
</p>

# EmpirioLabs AI MCP server

Remote [Model Context Protocol](https://modelcontextprotocol.io) server for [EmpirioLabs AI](https://empiriolabs.ai). It lets any MCP client run the whole platform as tools: chat with more than 180 text and multimodal models, generate images, video, music, speech, 3D assets and transcripts, run web search and research with citations, start long-running agent tasks, submit batch jobs, deploy and manage GPU Cloud instances, clusters and volumes, and create hosted agents. It is a remote server, so there is nothing to install.

| | |
|---|---|
| Server URL | `https://mcp.empiriolabs.ai/mcp` (Streamable HTTP) |
| Authentication | OAuth 2.1 (sign in with your EmpirioLabs account) or an EmpirioLabs API key as a bearer token |
| Registry name | `ai.empiriolabs/mcp` in the [official MCP Registry](https://registry.modelcontextprotocol.io) |
| Documentation | https://docs.empiriolabs.ai/mcp |
| Support | support@empiriolabs.ai |

Every model and feature EmpirioLabs adds is available here as it launches, at the same final prices and limits as the API. Connections use your prepaid credits, and you can disconnect any app under **Settings** in the dashboard.

## Connect

### Claude (web, desktop, mobile)

1. Open **Settings**, then **Connectors**, and choose **Add custom connector**.
2. Enter `https://mcp.empiriolabs.ai/mcp` as the URL. Leave the OAuth client fields empty.
3. Click **Connect**, sign in to EmpirioLabs, review the request, and choose **Allow access**.

Claude Code:

```bash
claude mcp add --transport http empiriolabs https://mcp.empiriolabs.ai/mcp
```

Run `/mcp` inside Claude Code to complete the sign-in the first time.

### ChatGPT

1. Open **Settings**, then **Plugins**, and turn on **Developer mode**.
2. Choose **Create app**, enter `https://mcp.empiriolabs.ai/mcp` as the server URL with **OAuth** authentication, and create it.
3. Finish the sign-in and choose **Allow access**. The server also provides the `search` and `fetch` tools ChatGPT uses for connectors, so it works in chat and in deep research.

### Cursor, VS Code, Windsurf, Cline and other editors

Remote servers are configured with a URL. Sign in through OAuth when the editor prompts, or add an API key header:

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

VS Code reads the same shape from `.vscode/mcp.json` with a `servers` key and `"type": "http"`. Codex CLI: `codex mcp add empiriolabs --url https://mcp.empiriolabs.ai/mcp`. Gemini CLI and Windsurf accept the JSON block above in their MCP settings. Cline: see [llms-install.md](llms-install.md).

### Any HTTP client

The server speaks JSON-RPC over `POST https://mcp.empiriolabs.ai/mcp`. Send `Authorization: Bearer <API key or OAuth access token>` and `Accept: application/json, text/event-stream` on every request.

```bash
curl "https://mcp.empiriolabs.ai/mcp" \
  -H "Authorization: Bearer $EMPIRIOLABS_API_KEY" \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_models","arguments":{"modality":"image","limit":5}}}'
```

## Tools

78 tools in ten toolsets. The complete reference with every parameter is on the [documentation page](https://docs.empiriolabs.ai/mcp).

| Toolset | What it covers |
|---|---|
| Models | Browse the catalog, model schemas, prices and platform status |
| Text | Chat completions, embeddings, reranking, image analysis, AI-text detection |
| Search | Web search, grounded answers and multi-step research with citations |
| Media | Image, video, 3D, music, speech and transcription, plus generation templates and Compose recipes |
| Jobs | Asynchronous job status and results |
| Agents | Long-running agent tasks |
| Account | Credit balance and usage history |
| Batch | Batch files and batch runs |
| GPU Cloud | GPU types, instances, clusters, volumes and workloads |
| Hosted Agents | Private hosted agents, channels, skills and connectors |

### Profiles

Profiles expose a subset of toolsets at a shorter URL:

| URL | Toolsets |
|---|---|
| `https://mcp.empiriolabs.ai/mcp` | all |
| `https://mcp.empiriolabs.ai/mcp/inference` | models, text, search, jobs, account |
| `https://mcp.empiriolabs.ai/mcp/media` | models, media, jobs, account |
| `https://mcp.empiriolabs.ai/mcp/cloud` | models, account, gpu, hosted_agents |
| `https://mcp.empiriolabs.ai/mcp/no-media` | everything except media |

Combine toolsets with `+`, for example `https://mcp.empiriolabs.ai/mcp/models+text+jobs`.

## Access and privacy

- Read-only tools (catalog, jobs, usage) use no credits. Tools that run models, searches, agent tasks, batches or infrastructure use the prepaid credits of the connected account.
- OAuth connections are listed under **Settings > Connected applications** in the [dashboard](https://platform.empiriolabs.ai), where **Disconnect** ends access right away.
- [Privacy policy](https://empiriolabs.ai/privacy-policy) and [terms of service](https://empiriolabs.ai/terms-of-service).

## About this repository

This repository holds the public listing material for the hosted server: the registry `server.json`, the icons, and the install notes. The server itself is operated by EmpirioLabs.ai LLC at `mcp.empiriolabs.ai`.
