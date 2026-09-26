<p align="center">
  <img src="icon-dark-256.png" width="128" height="128" alt="EmpirioLabs AI">
</p>

# EmpirioLabs AI MCP server

Remote [Model Context Protocol](https://modelcontextprotocol.io) server for [EmpirioLabs AI](https://empiriolabs.ai). Run 180+ AI models, image, video and speech generation, web search, batch jobs, GPU Cloud and hosted agents as tools with your EmpirioLabs account. It is a remote server, so there is nothing to install.

| | |
|---|---|
| Server URL | `https://mcp.empiriolabs.ai/mcp` (Streamable HTTP) |
| Authentication | OAuth 2.1 (sign in with your EmpirioLabs account) or an EmpirioLabs API key as a bearer token |
| Registry name | `ai.empiriolabs/mcp` in the [official MCP Registry](https://registry.modelcontextprotocol.io), version 1.2.0 |
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

Run `/mcp` inside Claude Code to complete the sign-in the first time. The repository is also a Claude Code plugin (`.claude-plugin/plugin.json`), so it can be installed from a plugin marketplace.

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

### Google Antigravity

Antigravity names the endpoint field `serverUrl`, not `url`. Put this in
`~/.gemini/config/mcp_config.json`, or in `plugins/<name>/mcp_config.json` to
ship it with a plugin:

```json
{
  "mcpServers": {
    "empiriolabs": {
      "serverUrl": "https://mcp.empiriolabs.ai/mcp",
      "headers": {
        "Authorization": "Bearer sk-empiriolabs-your_key_here"
      }
    }
  }
}
```

A server that fails to connect is silently absent from Antigravity's tool list
rather than reported as an error, so check the key first if the tools do not
appear.

### Grok, Perplexity, Le Chat and Gemini

These assistants take the server as a custom connector; paste `https://mcp.empiriolabs.ai/mcp` and sign in when asked.

- **Grok**: open `grok.com/connectors`, choose **New Connector**, then **Custom**, and enter the URL.
- **Perplexity**: open **Settings**, then **Connectors**, choose **Custom connector**, then **Remote**, enter the URL with the **Streamable HTTP** transport and **OAuth 2.0**.
- **Le Chat**: open **Connectors**, choose **Add Connector**, then the **Custom MCP Connector** tab, give it a name and enter the URL.
- **Gemini**: open **Settings & help**, then **Connected Apps**, and add a custom app with the URL.

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

81 tools in 10 toolsets. The complete reference with every parameter is on the [documentation page](https://docs.empiriolabs.ai/mcp).

| Toolset | What it covers |
|---|---|
| Models | Browse the model catalog, prices, capabilities, and parameters |
| Text | Run chat, embeddings, reranking, and AI text detection (uses credits) |
| Search | Run web search, grounded answers, and research (uses credits) |
| Media | Generate and edit images, video, audio, speech, transcription, and 3D (uses credits) |
| Jobs | Check, wait for, and cancel generation jobs |
| Agents | Run and manage agent tasks (uses credits) |
| Account | Read usage history and the current balance |
| Batch | Upload batch files and manage batch jobs (uses credits) |
| GPU Cloud | Deploy and manage GPU instances, clusters, and volumes (billable) |
| Hosted Agents | Create and manage hosted agents (billable) |

### Profiles

Profiles expose a subset of toolsets at a shorter URL:

| URL | Toolsets |
|---|---|
| `https://mcp.empiriolabs.ai/mcp` | all |
| `https://mcp.empiriolabs.ai/mcp/inference` | models, text, search, jobs, account |
| `https://mcp.empiriolabs.ai/mcp/media` | models, media, jobs, account |
| `https://mcp.empiriolabs.ai/mcp/cloud` | models, account, gpu, hosted_agents |
| `https://mcp.empiriolabs.ai/mcp/no-media` | models, text, search, jobs, agents, account, batch, gpu, hosted_agents |

Combine toolsets with `+`, for example `https://mcp.empiriolabs.ai/mcp/models+text+jobs`.

### Prompts

Ready-made requests that chain several tools; clients that support MCP prompts list them next to the tools.

| Prompt | What it does | Arguments |
|---|---|---|
| `choose_model` | Compare EmpirioLabs models for a task and recommend one, with a cheaper fallback and final prices. | task, modality (optional), priority (optional) |
| `research_with_citations` | Answer a question from live web research and cite every source. | question, depth (optional) |
| `generate_media` | Create an image, video, audio track or 3D asset from a description and return the finished files. | description, kind (optional), model (optional) |
| `deploy_gpu_workload` | Rent a GPU on EmpirioLabs GPU Cloud, start a workload on it and report the endpoints and hourly cost. | workload, gpu (optional), max_hourly_price (optional) |
| `spend_report` | Summarise the account balance, recent usage and everything that is still running and billing. | period (optional) |

## Access and privacy

- Read-only tools (catalog, jobs, usage) use no credits. Tools that run models, searches, agent tasks, batches or infrastructure use the prepaid credits of the connected account.
- OAuth connections are listed under **Settings > Connected applications** in the [dashboard](https://platform.empiriolabs.ai), where **Disconnect** ends access right away.
- [Privacy policy](https://empiriolabs.ai/privacy-policy) and [terms of service](https://empiriolabs.ai/terms-of-service).

## About this repository

This repository holds the public listing material for the hosted server: the registry `server.json`, the LobeHub and Claude plugin manifests, the icons, and the install notes. Every file that describes the tool surface is generated from the server's own definition, so it always matches what `https://mcp.empiriolabs.ai/mcp` serves. The server itself is operated by EmpirioLabs.ai LLC.

The files in this repository are licensed only for installing and connecting to EmpirioLabs AI; see `LICENSE`. The EmpirioLabs name and logos are trademarks of EmpirioLabs.ai LLC.
