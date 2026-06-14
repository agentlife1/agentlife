# What Is MCP? (Model Context Protocol)

*The universal "USB-C" for AI agent tools — explained in plain English.*

---

## The Problem MCP Solves

Before MCP, connecting an AI agent to a tool looked like this:

- Every agent framework had its own way of adding tools
- Every service (Google Calendar, GitHub, your bank) had its own API
- If you switched agent frameworks, you rewrote all your tool connections

It was like having a drawer full of phone chargers — each one only fit one device.

## What MCP Is

**MCP (Model Context Protocol)** is an open standard created by Anthropic. It's a common language that any AI agent can use to talk to any tool or service. Think of it as **USB-C for AI agents** — one connector that works everywhere.

**How it works:**

```
┌─────────────┐     MCP Protocol      ┌──────────────┐
│  AI Agent   │ ◄──────────────────►  │  MCP Server  │
│  (Hermes)   │     (stdio or HTTP)   │  (tool host) │
└─────────────┘                       └──────────────┘
```

The agent (the **MCP client**) connects to an **MCP server** — a small program that exposes tools. The agent discovers what tools are available, what inputs they need, and calls them on demand. The server handles the actual API calls, file access, or computation.

## MCP vs. Regular APIs

| | Regular API | MCP Server |
|---|---|---|
| **Discovery** | You read docs, write code | Agent discovers tools automatically |
| **Setup** | Install SDK, handle auth, parse responses | Run one command, agent handles the rest |
| **Switching** | Rewrite everything for a new framework | Same MCP server works with any MCP-compatible agent |
| **Your effort** | Manual integration per tool | Configure once, use everywhere |

## Real Example: Getting the Time

**Without MCP** — you'd need to write a Python script, parse the output, handle errors, and register it as a custom tool in your agent.

**With MCP** — you add this to your config:

```yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]
```

That's it. The agent now has a `get_current_time` tool. Ask "what time is it in Tokyo?" and the agent discovers the tool, calls it with the right parameters, and returns the answer.

## What MCP Servers Can Do

There are already hundreds of MCP servers for:

- **File system** — read, write, search your files
- **GitHub** — manage issues, PRs, repos
- **Databases** — PostgreSQL, SQLite, MySQL queries
- **Web search** — Google, Brave, DuckDuckGo
- **Email** — Gmail, IMAP
- **Calendar** — Google Calendar
- **Maps** — geocoding, directions, places
- **Puppeteer** — browser automation
- **Financial data** — stock prices, market data
- **... and many more**

## MCP in the AgentLife Stack

In the AgentLife architecture:

```
┌─────────────────────────────────────┐
│         AgentLife Persona           │
│  (your config + skills + cron)      │
├─────────────────────────────────────┤
│         Hermes Agent                │
│  (agent framework with MCP client)  │
├─────────────────────────────────────┤
│         MCP Servers                 │
│  (time, filesystem, github, ...)    │
├─────────────────────────────────────┤
│     External Services / APIs        │
│  (Google, GitHub, banks, ...)       │
└─────────────────────────────────────┘
```

Each persona pack (like Life Ops) can recommend or automatically configure the MCP servers it needs. Install the Life Ops pack, and your agent automatically gets calendar, financial, and file system tools.

## MCP Transports

MCP servers connect two ways:

### Stdio (local)
The agent runs the server as a local subprocess — fastest and most secure. Your data never leaves your machine.

```yaml
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/me/data"]
```

### HTTP (remote)
The agent connects to a server running on another machine or in the cloud. Good for shared services.

```yaml
mcp_servers:
  company_api:
    url: "https://mcp.mycompany.com/mcp"
    headers:
      Authorization: "Bearer sk-..."
```

## What This Means for You

As a beginner, you don't need to build MCP servers. You need to:

1. **Use them** — configure existing MCP servers in your Hermes config
2. **Choose persona packs** that include the MCP servers you need
3. **Eventually create your own** — when you want to connect a service that doesn't have an MCP server yet

AgentLife handles most of this for you. When you install a persona pack, it brings the MCP servers that persona needs.

---

**Next:** Understand how the agent framework behind all this works → [How Hermes Agent Works](how-hermes-works.md)