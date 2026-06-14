# MCP Server Configs — Quick Start

This directory contains ready-to-copy YAML snippets for the most commonly
used [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers.
Each file is a self-contained, heavily-commented config block for **one**
MCP server.

> New to MCP? Read the full guide:
> [`../../../guides/mcp-integration.md`](../../guides/mcp-integration.md)
> — it covers the conceptual overview, security model, and how to build
> your own server.

---

## What's in this directory

| File | Server | Runtime | Needs a key? | What it's for |
|------|--------|---------|--------------|---------------|
| [`time.yaml`](time.yaml)         | `mcp-server-time` (PyPI)           | `uvx` (Python) | No  | Current time + timezone conversions |
| [`filesystem.yaml`](filesystem.yaml) | `@modelcontextprotocol/server-filesystem` (npm) | `npx` (Node)   | No  | Sandboxed read/write to chosen directories |
| [`web-search.yaml`](web-search.yaml) | `tavily-mcp` (npm)                | `npx` (Node)   | **Yes** — `TAVILY_API_KEY` | Live web search + URL extraction |
| [`puppeteer.yaml`](puppeteer.yaml)   | `@modelcontextprotocol/server-puppeteer` (npm) | `npx` (Node)   | No  | Headless browser automation, scraping, logins |
| [`github.yaml`](github.yaml)         | `@modelcontextprotocol/server-github` (npm)     | `npx` (Node)   | **Yes** — `GITHUB_PERSONAL_ACCESS_TOKEN` | Issues, PRs, repos, file contents |

All five are official / widely-used MCP servers. None of them are fictional —
they all live in the upstream [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers)
repo or are published by the maintainers of the underlying service (Tavily).

---

## Prerequisites — install once

You need three things before any of these will work.

### 1. The Hermes MCP SDK dependency

Hermes itself talks to MCP servers using the Python `mcp` SDK. Install it
once, in the same Python environment where Hermes is installed:

```bash
pip install mcp
```

If you forget this, Hermes will log `MCP SDK not available` on startup.

### 2. `uvx` — for Python-based servers (`time.yaml`)

`uvx` is a zero-install runner for Python packages, shipped with
[uv](https://docs.astral.sh/uv/). Install uv:

```bash
# Linux / macOS / WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# macOS via Homebrew
brew install uv

# Or via pip (works everywhere)
pip install uv
```

After install, `uvx` is on your `PATH`. Verify with `uvx --version`.

### 3. `npx` — for Node-based servers (everything else)

`npx` ships with Node.js. Install Node 18 or newer:

```bash
# Linux (Debian/Ubuntu) — via NodeSource
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# macOS — via Homebrew
brew install node

# Or use nvm (works on Linux, macOS, WSL)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
nvm install --lts
```

Verify with `node --version` (should be ≥18) and `npx --version`.

### Linux-only: headless-browser system libraries

`puppeteer.yaml` runs a real Chromium. On a fresh Linux server you may
need Chrome's runtime libraries. The full apt command is in the comment
block at the top of [`puppeteer.yaml`](puppeteer.yaml). On macOS and most
desktop Linux installs these are already present.

---

## How to use these configs

Each `.yaml` file in this directory is a **snippet**, not a full
`config.yaml`. To actually enable a server:

### Option A — manual paste (simplest)

1. Open the file you want (e.g. `time.yaml`).
2. **Copy the YAML block at the bottom** — everything from the server
   name (e.g. `time:`) downward, NOT the top comment header.
3. Open `~/.hermes/config.yaml` in your editor.
4. Find or create the `mcp_servers:` key.
5. Paste the block **indented 2 spaces** under `mcp_servers:`.

   Result for `time.yaml`:

   ```yaml
   mcp_servers:
     time:                       # ← 2 spaces of indent
       command: "uvx"            # ← 4 spaces of indent
       args:                     # ← 4 spaces of indent
         - "mcp-server-time"     # ← 6 spaces of indent
   ```

6. Repeat for any other servers you want to enable.
7. Restart Hermes (MCP discovery happens at startup).

### Option B — merge with `yq` (cleaner for several at once)

If you have [`yq`](https://github.com/mikefarah/yq) installed, you can
merge an entire snippet file in one shot. First wrap it in a `mcp_servers:`
key temporarily, or use a tool like `yq` to splice it under the right key:

```bash
# Example: merge filesystem.yaml into your config
yq eval-all '. as $item ireduce ({}; . *+ $item)' \
    ~/.hermes/config.yaml filesystem.yaml > /tmp/config.merged.yaml
mv /tmp/config.merged.yaml ~/.hermes/config.yaml
```

(Adjust the merge strategy to taste — `yq` has several.)

### Verifying it worked

After restarting Hermes, check that the tools are registered:

```bash
# Hermes CLI — should list tools prefixed with mcp_<servername>_
hermes tools list | grep mcp_

# Or, the equivalent in your client of choice.
```

You can also run the server manually to confirm the command works on its
own (Hermes spawns the exact same command):

```bash
uvx mcp-server-time              # Python-based
npx -y @modelcontextprotocol/server-filesystem /tmp   # Node-based
```

If the command produces a JSON-RPC handshake on stdout and waits for
input, it's working. Press `Ctrl-C` to exit.

---

## Security checklist before you enable a server

- **Never** pass the filesystem server a path containing private keys
  (`~/.ssh`, `~/.gnupg`, `~/.aws`), password managers, or your entire
  home directory. The sandbox is only as safe as the roots you give it.
- **Never** commit a real API key or GitHub PAT to git. Use
  `${VAR_NAME}` references and keep the actual values in your shell
  profile or a secrets manager.
- **Treat deprecated packages as still-functional but unmaintained.**
  `puppeteer.yaml` and `github.yaml` use packages that are archived in
  the official MCP servers repo. They still work for most use cases —
  comments at the top of each file call out the modern alternatives
  (Playwright, community GitHub forks) if you need active maintenance.
- Only install servers from sources you trust. The full trust list is in
  [`../../../guides/mcp-integration.md`](../../guides/mcp-integration.md#trusting-mcp-servers).

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `MCP SDK not available` on startup | The `mcp` Python package isn't installed in Hermes's env | `pip install mcp` |
| Server starts then exits immediately | Wrong command/args, or missing API key | Run the command manually (see above) and read its stderr |
| `tool not found: mcp_time_*` | The server isn't in `mcp_servers:`, OR indentation is wrong | Re-check YAML — 2 spaces per level, key must be exactly `mcp_servers` |
| Puppeteer crashes with `Missing X server` or `$DISPLAY` errors | You need a headless browser config | Add `--headless=new` to `launchOptions.args` at call time, or run the official Chromium headless build |
| `GitHub 401 Unauthorized` | Token is wrong, expired, or lacks the required scope | Regenerate the PAT with the right scopes (see top of `github.yaml`) |

For deeper debugging, watch Hermes's startup log:

```bash
tail -f ~/.hermes/logs/gateway.log
```

---

**Next:** once you've picked the servers you want, head to the
[full MCP integration guide](../../guides/mcp-integration.md) to learn
how the agent uses these tools and how to write your own MCP server.
