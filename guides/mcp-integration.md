# MCP Integration Guide

*Connecting your AI agent to the world through the Model Context Protocol.*

---

## What You'll Learn

- What MCP is and why it matters (brief recap)
- How to configure MCP servers in Hermes Agent
- Recommended MCP servers for every AgentLife persona
- How to use MCP servers from the Life Ops persona
- How to build your own MCP server (if you need something custom)

> **New to MCP?** Start with [What Is MCP?](concepts/what-is-mcp.md) for the conceptual overview.

---

## How MCP Works in Hermes

Hermes Agent has a **built-in MCP client**. When Hermes starts, it reads `mcp_servers` from its config, connects to each server, discovers its tools, and makes them available to the agent automatically.

**Tools are auto-prefixed** with `mcp_{server_name}_`. For example:

| MCP Server | Tool Name | Agent Sees As |
|---|---|---|
| `time` | `get_current_time` | `mcp_time_get_current_time` |
| `filesystem` | `read_file` | `mcp_filesystem_read_file` |
| `github` | `list_issues` | `mcp_github_list_issues` |

The agent knows how to use these tools just like any built-in tool. No manual registration needed.

## Configuration

All MCP servers go under `mcp_servers` in `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  server_name:
    command: "command"          # stdio transport (local)
    args: ["arg1", "arg2"]      # optional arguments
    env:                        # optional environment variables
      TOKEN: "sk-..."
    timeout: 120                # optional per-call timeout (seconds)
```

### Stdio vs. HTTP Transport

**Stdio (local)** — Hermes runs the server as a subprocess. Most secure, best performance.

```yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]
```

**HTTP (remote)** — Hermes connects to a server over HTTP. Good for shared services.

```yaml
mcp_servers:
  company_api:
    url: "https://mcp.example.com/mcp"
    headers:
      Authorization: "Bearer sk-..."
```

## Prerequisites

Different MCP servers need different runtimes:

| Runtime | Install Command | Used By |
|---------|----------------|---------|
| **Python + uvx** | `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh \| sh` | Python-based MCP servers |
| **Node.js + npx** | `npm install -g npx` (comes with Node.js) | Most community MCP servers |
| **Python mcp SDK** | `pip install mcp` | Required by Hermes to connect to MCP servers |

Install the Hermes MCP dependency:

```bash
pip install mcp
```

## Recommended MCP Servers

### Essential — Every Installation

| Server | What It Does | Install |
|--------|-------------|---------|
| **Time** | Current time in any timezone | `uvx mcp-server-time` |
| **Filesystem** | Read/write files, list directories | `npx -y @modelcontextprotocol/server-filesystem /path` |

```yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]

  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/you/data"]
```

### For Life Ops Persona

| Server | What It Does | Life Ops Use Case | Install |
|--------|-------------|-------------------|---------|
| **Puppeteer** | Browser automation | Fetch account balances, scrape data | `npx -y @modelcontextprotocol/server-puppeteer` |
| **Web Search** | Search the web | Research, news, market info | `npx -y @anthropic-extra/servers-web-search` |
| **SQLite** | Query local databases | Portfolio history, expense DB | `uvx mcp-server-sqlite --db ~/agentlife/data.db` |
| **Google Calendar** (via CalDAV) | Read calendar events | Calendar Ops time audit | `uvx mcp-server-caldav` |
| **GitHub** | Manage repos/issues | Track feature requests, roadmap | `npx -y @modelcontextprotocol/server-github` |

```yaml
mcp_servers:
  puppeteer:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-puppeteer"]

  web_search:
    command: "npx"
    args: ["-y", "@anthropic-extra/servers-web-search"]
    env:
      ANTHROPIC_API_KEY: "${ANTHROPIC_API_KEY}"   # or your search API key

  sqlite:
    command: "uvx"
    args: ["mcp-server-sqlite", "--db", "/home/you/agentlife/data.db"]
```

### For Development / Contributors

| Server | What It Does | Install |
|--------|-------------|---------|
| **GitHub** | Issues, PRs, repos | `npx -y @modelcontextprotocol/server-github` |
| **PostgreSQL** | Database queries | `uvx mcp-server-postgres --connection-string postgresql://...` |
| **Memory** | Persistent key-value store | `npx -y @modelcontextprotocol/server-memory` |

## MCP in Life Ops: Detailed Examples

### Portfolio Tracking with MCP

Instead of writing custom scripts to fetch stock prices, use an MCP server:

```yaml
mcp_servers:
  yahoo_finance:
    command: "npx"
    args: ["-y", "mcp-server-yahoo-finance"]   # hypothetical — swap for real server
```

The agent can then ask for real-time prices and calculate portfolio value directly.

### Calendar Ops with MCP

For calendar integration, use a CalDAV MCP server:

```yaml
mcp_servers:
  caldav:
    command: "npx"
    args: ["-y", "mcp-server-caldav"]
    env:
      CALDAV_URL: "https://caldav.icloud.com/"
      CALDAV_USERNAME: "your@email.com"
      CALDAV_PASSWORD: "app-specific-password"
```

The agent can then read your calendar, check for conflicts, and provide time audit data.

### Subscriptions with MCP

For subscription tracking, combine an SQLite MCP server (for your local subscription database) with a Puppeteer MCP server (to check renewal status on vendor sites).

## Life Ops Use Case: How MCP Powers Each One

Below is how MCP fits into each Life Ops use case. Each use case can work **without** MCP (using the included shell/Python scripts), or **with** MCP for richer data.

| Use Case | Without MCP | With MCP |
|----------|-------------|----------|
| **Portfolio** | Manual balance entry, CSV imports | Auto-fetch prices, real-time values |
| **Expenses** | Manual entry, CSV from bank | Browser automation to pull statements |
| **Calendar** | Manual event entry | Direct CalDAV sync |
| **Subscriptions** | Manual list tracking | Auto-check renewal status via browser |

### How to Switch an Existing Use Case to MCP

Each use case has a `config.yaml` with an `mcp` section. Enable it:

```yaml
# packs/life-ops/use-cases/portfolio-tracking.yaml
mcp:
  enabled: true
  servers:
    - yahoo_finance
  # Falls back to manual CSV import if MCP is unavailable
  fallback_mode: csv_import
```

Set `mcp.enabled: true` and make sure the corresponding MCP server is configured in Hermes.

## Security Notes

### Environment Variable Filtering

Hermes does NOT pass your full shell environment to MCP server subprocesses. Only safe baseline variables are passed (PATH, HOME, USER, etc.). All API keys and tokens are excluded unless you explicitly add them via the `env` config key:

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      # Only this token is passed to the subprocess
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxxxxxxxxxxx"
```

### Credential Stripping

If an MCP tool returns an error containing credential-like patterns, Hermes automatically redacts them before showing the output to the AI model. Covers: API keys, tokens, passwords, secrets.

### Trusting MCP Servers

MCP servers have full access to whatever resources you give them. Only install servers from:
- The official [MCP server list](https://github.com/modelcontextprotocol/servers)
- Verified open-source packages (check GitHub stars, recent commits, code reviews)
- Servers you build yourself

## Building Your Own MCP Server

If you need a tool that doesn't exist yet, building an MCP server is straightforward.

### Python Example

```python
# my_server.py
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent
import mcp.server.stdio

server = Server("my-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="hello",
            description="Say hello to someone",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name to greet"}
                },
                "required": ["name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "hello":
        return [TextContent(
            type="text",
            text=f"Hello, {arguments['name']}!"
        )]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(server_name="my-server")
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

Run it with:

```bash
uvx my_server.py
```

Then add to Hermes config:

```yaml
mcp_servers:
  my_server:
    command: "uvx"
    args: ["path/to/my_server.py"]
```

## Troubleshooting

### Server won't connect

```bash
# Check if the command works standalone
uvx mcp-server-time

# Check Hermes startup logs
tail -50 ~/.hermes/logs/gateway.log
```

### Tools not appearing

1. Verify the server is listed under `mcp_servers` (not `mcp` or `servers`)
2. Check YAML indentation (2 spaces per level)
3. Restart Hermes (MCP discovery happens at startup)

### "MCP SDK not available"

```bash
pip install mcp
```

### HTTP server not connecting

1. Verify the URL is reachable: `curl -v https://your-mcp-server.com/mcp`
2. Check headers — many MCP servers require auth
3. Increase timeout: `connect_timeout: 60`

---

**Next:** [Getting Started Guide](getting-started.md) — set up AgentLife from scratch.