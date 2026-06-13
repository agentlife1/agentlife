# AgentLife — Docker Install Guide

Run AgentLife in a Docker container for a clean, isolated setup.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system
- Docker Compose (included with Docker Desktop, install separately on Linux)

## Quick Start with Docker Compose (Recommended)

Create a `docker-compose.yml`:

```yaml
version: "3.9"

services:
  hermes:
    image: nousresearch/hermes-agent:latest
    container_name: agentlife
    restart: unless-stopped
    ports:
      - "9119:9119"
    volumes:
      - ./hermes-config:/home/user/.hermes
      - ./agentlife-config:/home/user/.hermes/agentlife
    environment:
      - HERMES_PROVIDER=openrouter
      - HERMES_MODEL=deepseek/deepseek-v4-flash
```

Then:

```bash
docker compose up -d
docker compose logs -f
```

## Manual Docker Run

```bash
docker run -d \
  --name agentlife \
  --restart unless-stopped \
  -p 9119:9119 \
  -v hermes-data:/home/user/.hermes \
  nousresearch/hermes-agent:latest
```

## Install AgentLife Inside the Container

```bash
docker exec -it agentlife bash
pip install agentlife
agentlife setup
exit
```

## Verify

```bash
docker exec agentlife agentlife verify
```

## Dashboard

Access your Hermes dashboard at `http://localhost:9119`

---

*Need help? Open an issue on GitHub or join the community Discord.*