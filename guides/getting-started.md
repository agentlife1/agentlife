# Getting Started with AgentLife

*A step-by-step walkthrough for your first AI agent — no prior experience needed.*

---

This guide assumes you're **tech-savvy but new to AI agents**. You've used the terminal before. You know what an API key is. But you've never run your own agent.

**Time required:** ~30 minutes

## Step 0: What You'll Have at the End

By the time you finish this guide, you will have:

- ✅ An AI agent running on your machine
- ✅ Connected to an AI model (via OpenRouter)
- ✅ A daily morning brief checking your portfolio and calendar
- ✅ The agent sending updates to Telegram (or your preferred platform)
- ✅ Understanding of what each piece does and why

Let's go.

---

## Step 1: Get an API Key

Your AI agent needs a brain. The brain is an AI model running somewhere on the internet. You access it through an **API key**.

**Recommended provider:** [OpenRouter](https://openrouter.ai)

OpenRouter gives you access to 200+ models (Claude, GPT, DeepSeek, Gemini, and more) with a single API key. You pay per-use — typically pennies per day for personal use.

1. Go to [openrouter.ai/keys](https://openrouter.ai/keys)
2. Sign up (or sign in)
3. Click **"Create Key"**
4. Copy the key (starts with `sk-or-v1-...`)

> 💡 **Why OpenRouter?** One key. Any model. No vendor lock-in. If one model goes down, you switch with one config change.

**Alternative:** You can also use Anthropic directly, OpenAI, Google Gemini, or any of the 20+ providers Hermes supports. The setup is different for each — OpenRouter is the easiest starting point.

## Step 2: Install Hermes Agent

Hermes Agent is the **runtime** — the software that turns an API key + a model into an agent that can do things.

Open your terminal and run:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

**What this does:** Downloads the Hermes installer, sets up a Python virtual environment, installs Hermes and its dependencies, and launches the setup wizard.

### The Setup Wizard

The wizard will ask you a few questions:

1. **Choose a provider** — select `openrouter`
2. **Enter your API key** — paste the key from Step 1
3. **Choose a model** — `deepseek/deepseek-v4-flash` is a great starting point (fast, cheap, capable)
4. **Enable tools** — accept the defaults
5. **Platform setup** — skip for now (you can add Telegram/Discord later)

When the wizard finishes, test it:

```bash
hermes chat -q "Hello, what can you do?"
```

You should get a response. If you do, Hermes is working.

> **Troubleshooting:** If the install fails, check:
> - Python 3.10+ is installed: `python3 --version`
> - You have internet access
> - The API key is valid (paste it at [openrouter.ai/keys](https://openrouter.ai/keys) to verify)

## Step 3: Install AgentLife

Now we install the persona framework on top of Hermes.

```bash
git clone https://github.com/agentlife1/agentlife.git
cd agentlife
pip install -e .
```

**What this does:**
- Clones the AgentLife repository
- Installs the `agentlife` CLI as a Python package ("editable" mode — `-e` — so changes are live immediately)
- Makes the `agentlife` command available in your terminal

### Run Setup

```bash
agentlife setup
```

This copies persona pack configs to your Hermes directory and validates everything.

### Verify

```bash
agentlife verify
```

You should see all checks passing (green checkmarks). If any fail, the output tells you what's missing.

## Step 4: Configure Your First Persona (Life Ops)

The Life Ops persona turns your agent into a personal operations engineer. Let's start with the portfolio tracking use case — it's the simplest to demo.

### 4a: Enable Portfolio Tracking

```bash
agentlife setup --persona life-ops --use-cases portfolio
```

This tells AgentLife to enable the portfolio tracking configuration within the Life Ops persona.

### 4b: Configure Your Accounts

AgentLife comes with a **manual account mode** — you list your accounts and their balances. No API keys needed for banks or brokers (though you can add automated connections later).

Edit your persona config:

```bash
# The setup wizard will prompt you, or edit manually:
# ~/.hermes/config.yaml or the persona pack config
```

Add your accounts:

```yaml
life-ops:
  portfolio:
    accounts:
      - name: "401(k)"
        type: retirement
        provider: fidelity
      - name: "Robinhood"
        type: brokerage
        provider: robinhood
      - name: "Checking"
        type: cash
        provider: chase
```

### 4c: Run a Net Worth Check

```bash
hermes chat -q "Check my portfolio and tell me my net worth"
```

The agent will use the portfolio tracking skill to calculate your position. The first time, it may ask you for current balances. Over time, it builds up a history.

## Step 5: Add MCP Servers (Optional But Recommended)

MCP servers give your agent more tools. Let's add the **time server** — the simplest example.

Edit `~/.hermes/config.yaml` and add:

```yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]
```

Restart Hermes:

```bash
hermes chat -q "What time is it in Tokyo and London?"
```

The agent will now use the MCP time server to answer instead of guessing.

📖 See the **[MCP Integration Guide](mcp-integration.md)** for more servers (filesystem, GitHub, calendars, finance).

## Step 6: Set Up the Daily Brief

The Daily Brief is the crown jewel — a cron job that runs every weekday morning and sends you a summary.

First, connect a messaging platform so you get the brief delivered. The easiest is Telegram:

1. Create a bot: message [@BotFather](https://t.me/botfather) on Telegram and create a new bot
2. Copy the bot token
3. Configure Hermes gateway:

```bash
hermes gateway setup
```

Select Telegram, paste your bot token, and add your Telegram user ID.

Then enable the daily brief cron:

```bash
hermes cron list
# Should show "daily-brief" — if not, enable it:
hermes cron create "30 6 * * 1-5" \
  --prompt "Run the Life Ops daily brief" \
  --skills life-ops-daily-brief
```

**What this does:** Every weekday at 6:30 AM, your agent runs the daily brief skill, collects portfolio, spending, calendar, and subscription data, and sends you a morning summary on Telegram.

## Step 7: Test Everything

Run a manual brief to see the full output:

```bash
hermes chat -q "Run my daily brief"
```

You should get something like:

```
📊 Morning Brief — June 13, 2026

Portfolio
  Net Worth: $2,849,312 (+0.07% today)

Budget
  Dining: $487/$400 (22% over — alert)
  Groceries: $320/$350 (on track)

Calendar
  3 meetings today, 1 focus block (2h)
  Next: Standup @ 9:30 AM

Subscriptions
  Netflix ($15.99) — renews in 7 days
  iCloud ($2.99) — renews in 14 days
```

## What Now?

You have a working AI agent with:
- ✅ Hermes Agent runtime
- ✅ AgentLife persona framework
- ✅ Life Ops persona with portfolio tracking
- ✅ Morning brief cron job
- ✅ MCP server for time data

**Next steps:**

| Goal | Do This |
|------|---------|
| Add more use cases | `agentlife setup --persona life-ops --use-cases expenses,calendar,subscriptions` |
| Understand MCP better | Read [What Is MCP?](concepts/what-is-mcp.md) |
| Explore the architecture | Read [How Hermes Works](concepts/how-hermes-works.md) |
| Connect more MCP servers | See the [MCP Integration Guide](mcp-integration.md) |
| Build your own persona | Use the [template pack](../packs/template/) |
| Contribute to the framework | Open an issue or PR on GitHub |

---

**Need help?** Open a [GitHub Issue](https://github.com/agentlife1/agentlife/issues) or start a Discussion.