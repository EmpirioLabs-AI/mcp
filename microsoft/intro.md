# EmpirioLabs AI

## Overview

[EmpirioLabs AI](https://empiriolabs.ai) is one account for 180+ AI models, image, video and speech generation, web search and research with citations, batch jobs, GPU Cloud and hosted agents. This connector brings the EmpirioLabs AI MCP server into Microsoft Copilot Studio and Power Automate over the Model Context Protocol (Streamable HTTP, `x-ms-agentic-protocol: mcp-streamable-1.0`). Agents discover the tools at runtime, so every model and feature EmpirioLabs adds is available as it launches, at the same final prices as the API.

## Publisher

EmpirioLabs.ai LLC

## Prerequisites

- An EmpirioLabs account with prepaid credits. Create one at https://platform.empiriolabs.ai.
- A Copilot Studio license to use the connector as an agent tool, or a Power Automate Premium license to call it from cloud flows.

## Supported operations

| Operation | Description |
|---|---|
| Invoke MCP server | Sends a Model Context Protocol request to `https://mcp.empiriolabs.ai/mcp` and returns the response. Tools are discovered dynamically. |
| Check service status | Returns the current status of the EmpirioLabs AI service. Use it in a cloud flow to confirm the connection works. |

The tools are grouped into these areas. The sign-in screen lets you choose which areas the agent may use.

| Area | What it covers |
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

Workflow prompts included with the server:

| Prompt | Purpose |
|---|---|
| `choose_model` | Compare EmpirioLabs models for a task and recommend one, with a cheaper fallback and final prices. |
| `research_with_citations` | Answer a question from live web research and cite every source. |
| `generate_media` | Create an image, video, audio track or 3D asset from a description and return the finished files. |
| `deploy_gpu_workload` | Rent a GPU on EmpirioLabs GPU Cloud, start a workload on it and report the endpoints and hourly cost. |
| `spend_report` | Summarise the account balance, recent usage and everything that is still running and billing. |

## Obtaining credentials

The connector uses OAuth 2.0. When you create a connection, sign in with your EmpirioLabs account, review the requested areas and choose **Allow access**. No API key is needed. You can disconnect the app at any time under **Settings** in the EmpirioLabs dashboard.

## Getting started

1. In Copilot Studio, open your agent, choose **Tools**, then **Add a tool**, and pick **Model Context Protocol**.
2. Select **EmpirioLabs AI**, create a connection and sign in with your EmpirioLabs account.
3. Add the tools you want the agent to use and publish the agent.

## Known issues and limitations

- Requests use the prepaid credits of the signed-in EmpirioLabs account; usage appears under **Usage** in the dashboard.
- Generated media is returned as short-lived links.

## Frequently asked questions

**Which models are available?** The live catalog is at https://empiriolabs.ai/models. The `models` tools list them with prices.

**Where is the documentation?** https://docs.empiriolabs.ai/mcp

**Who do I contact for support?** support@empiriolabs.ai

Server version 1.2.0.
