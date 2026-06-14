# AgentLife — Docker Install Guide
#
# What this guide does: Walks you through running AgentLife inside a
# Docker container. Docker is a way to package an application and all
# its dependencies into a single isolated "container" that runs the
# same way on any host. This is the cleanest install option if you
# don't want Python or systemd touching your host system.

# Comments prefixed with `#` are beginner-friendly explanations of what
# each command does. Lines that are NOT comments are the actual commands
# to run — copy-paste them into your terminal.

Run AgentLife in a Docker container for a clean, isolated setup.

## Prerequisites

# What this does: You need the Docker engine installed. Docker Desktop
# (Mac/Windows) bundles docker + docker compose. On Linux servers you
# usually install docker-ce and docker-compose-plugin separately.
- [Docker](https://docs.docker.com/get-docker/) installed on your system
- Docker Compose (included with Docker Desktop, install separately on Linux)

## Quick Start with Docker Compose (Recommended)

# What this does: Docker Compose is a tool for declaring multi-container
# setups in a single YAML file. We'll write a `docker-compose.yml` that
# defines ONE service (the hermes agent), then start it.
Create a `docker-compose.yml`:

```yaml
# What this does: A "compose file" describes the containers Docker
# should run. This block defines one service called `hermes` that
# uses the official image from Docker Hub.
version: "3.9"   # The compose-file format version. 3.9 is current.

services:        # Each top-level key under `services` is a container.
  hermes:
    # What this does: The image to pull. `latest` always refers to the
    # most recent published version of hermes-agent.
    image: nousresearch/hermes-agent:latest

    # What this does: A friendly name to refer to this container by
    # (used in `docker ps`, logs, etc.).
    container_name: agentlife

    # What this does: Tells Docker to restart the container
    # automatically (except when you explicitly stop it). Keeps the
    # agent up after a host reboot.
    restart: unless-stopped

    # What this does: Maps port 9119 inside the container to port
    # 9119 on the host, so you can reach the dashboard at
    # http://localhost:9119.
    ports:
      - "9119:9119"

    # What this does: "Volumes" mount a host directory into the
    # container so data persists across container restarts/rebuilds.
    # `./hermes-config` is a relative path — Docker will create it.
    volumes:
      - ./hermes-config:/home/user/.hermes
      - ./agentlife-config:/home/user/.hermes/agentlife

    # What this does: Environment variables passed into the container.
    # These tell Hermes which AI provider/model to talk to. You can
    # add more (e.g. TAVILY_API_KEY, PLAID_CLIENT_ID) here later.
    environment:
      - HERMES_PROVIDER=openrouter
      - HERMES_MODEL=deepseek/deepseek-v4-flash
```

# What this does: Starts the container in detached mode (`-d`) so the
# command returns immediately and the container runs in the background.
# `-f` (follow) tails the logs so you can watch startup.
Then:
```bash
docker compose up -d
docker compose logs -f
```

## Manual Docker Run

# What this does: The exact same thing as the compose file above, but
# expressed as a single `docker run` command line. Useful when you
# only need one container and don't want to maintain a YAML file.
```bash
# What this does: -d runs detached (in the background).
docker run -d \

  # What this does: Names the container "agentlife" (otherwise Docker
  # assigns a random adjective-noun pair).
  --name agentlife \

  # What this does: Restart automatically unless we explicitly stop it.
  --restart unless-stopped \

  # What this does: Map host port 9119 to container port 9119.
  -p 9119:9119 \

  # What this does: Mount a NAMED volume (`hermes-data`) at the path
  # Hermes uses for its config + data, so it persists across rebuilds.
  -v hermes-data:/home/user/.hermes \

  # What this does: The image to run. `:latest` is implicit.
  nousresearch/hermes-agent:latest
```

## Install AgentLife Inside the Container

# What this does: The base hermes-agent image ships with Hermes but
# not the AgentLife framework. We shell into the running container,
# install agentlife, and run setup once. The setup persists into the
# volume, so subsequent restarts pick it up.
```bash
# What this does: `docker exec -it` runs a command inside an already-
# running container. `-i` keeps stdin open, `-t` allocates a TTY so
# you get an interactive bash session.
docker exec -it agentlife bash

# What this does: Installs the agentlife framework on top of the
# image's Python environment.
pip install agentlife

# What this does: Runs the interactive setup wizard (API keys, persona
# selection, channels). Persisted to the volume.
agentlife setup

# What this does: Exits the bash session; the container keeps running.
exit
```

## Verify

# What this does: Runs the verify command inside the container without
# opening a shell. Useful in CI/scripts.
```bash
docker exec agentlife agentlife verify
```

## Dashboard

# What this does: Now that the container is running and ports are
# mapped, you can reach the Hermes dashboard from any browser on
# the host at the URL below.
Access your Hermes dashboard at `http://localhost:9119`

---

*Need help? Open an issue on GitHub or join the community Discord.*
