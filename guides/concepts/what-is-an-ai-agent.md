# What Is an AI Agent?

*The 5-minute primer for anyone who's used ChatGPT and wondered "what comes next?"*

---

If you've used ChatGPT, Claude, or Gemini, you've used an AI **chatbot**. You type a question, it gives you an answer. You ask for a recipe, it writes one. Useful, but passive — it only acts when you're sitting there typing.

An **AI agent** is the next step. Think of it as a chatbot that also has:

1. **Memory** — it remembers who you are, what you've asked, and what you care about
2. **Tools** — it can run code, read files, search the web, check your email, and control apps
3. **Initiative** — it can do things on a schedule without you asking every time

## The Analogy: A Chef vs. a Kitchen

A chatbot is like having a chef who'll write you a recipe card whenever you ask. Great, but you still have to shop for ingredients, prep, cook, and clean.

An AI agent is like having that same chef **in your kitchen**. They can open the fridge to see what's there, turn on the oven, set timers, and serve you dinner at 6 PM every day — without you telling them to preheat first.

## What Makes Something an Agent?

An agent has four capabilities that a chatbot doesn't:

### 1. Tool Access
A chatbot can only **talk**. An agent can **do**. It can run terminal commands, query APIs, read and write files, browse websites, and control software. This turns "write me a budget spreadsheet" (a chatbot can generate the CSV) into "build me a budget spreadsheet with my actual bank data" (the agent can fetch transactions, categorize them, and write the file).

### 2. Persistent Context
When you close a chatbot conversation, it's gone. An agent keeps working memory — your name, your preferences, your accounts, your goals. It carries this context across days and weeks, so every interaction builds on the last one.

### 3. Scheduled Autonomy
You can tell an agent "send me a portfolio summary every morning at 7 AM" and it will — without you being there. This is the difference between a tool you use and a system that works for you.

### 4. Multi-Step Reasoning
A chatbot answers one query. An agent can take a complex goal like "optimize my monthly spending" and break it into steps: fetch transactions, categorize them, compare to budget, suggest cuts, and email you a report. It uses tools along the way, not just text generation.

## A Concrete Example

**Chatbot:**
> You: "What did I spend on dining out last month?"
> Bot: "I don't have access to your spending data. You could check your bank app."

**Agent (with tool access):**
> You: "What did I spend on dining out last month?"
> Agent: *[fetches transactions from connected accounts, categorizes them, sums dining]*
> Agent: "You spent $487 on dining out in May — 22% over your $400 budget. Top merchants: Uber Eats ($187), Olive Garden ($89), local sushi spot ($76). Want me to suggest a dining budget for June?"

The difference isn't the AI — it's the tool access.

## The Ecosystem

An AI agent doesn't run on magic. It needs:

- **A model** — the AI brain (like Claude, GPT, DeepSeek)
- **A framework** — the software that gives the brain tools and memory (like Hermes Agent)
- **Tool connections** — ways to reach your data and apps (APIs, MCP servers, scripts)
- **A persona pack** — the configuration that tunes everything to your specific needs (this is where AgentLife comes in)

AgentLife is the **persona layer** that configures Hermes Agent for your life — finances, schedule, tasks, and more. It doesn't reinvent the framework; it makes the framework useful for a real human being.

## What an Agent Is Not

- **Not magic** — it's software. It makes mistakes. You should verify important actions.
- **Not a person** — it doesn't have intentions or feelings. It follows instructions.
- **Not always correct** — AI models hallucinate. Trust but verify, especially with financial data.
- **Not a replacement for you** — it's an assistant. You're still in charge.

---

**Next:** Learn how agents connect to your tools via [MCP — Model Context Protocol](what-is-mcp.md).
