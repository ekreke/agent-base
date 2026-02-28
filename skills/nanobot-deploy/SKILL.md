---
name: nanobot-deploy
description: Deploy and manage nanobot clusters using Docker. Provides scripts and configurations for master bot (health monitoring, infrastructure repair, MCP management) and slave bots (custom worker bots). Use when deploying nanobot on single machines with Docker, setting up bot clusters, or managing nanobot infrastructure.
---

# Nanobot Deploy

Deploy and manage nanobot clusters with master-slave architecture using Docker.

## Quick Start

### Deploy with Docker Compose (Recommended)

```bash
# Copy example configs
cp -r assets/master/* data/master/config/
cp -r assets/slave/* data/slave-1/config/

# Edit configs with your API keys
vim data/master/config/config.json
vim data/slave-1/config/config.json

# Deploy cluster
docker compose -f assets/docker-compose.yml up -d
```

### Deploy Individual Bots

```bash
# Deploy master bot
./scripts/deploy_master.sh

# Deploy slave bot
BOT_NAME=worker-1 BOT_ID=worker-1 ./scripts/deploy_slave.sh
```

## Deployment Modes

### Master Bot

Central management bot that:
- Monitors health of all slave bots
- Restarts failed bots automatically
- Manages MCP server configurations
- Updates skills across the cluster
- Aggregates logs and sends alerts

**Deploy master:**
```bash
./scripts/deploy_master.sh
```

**Configuration:** See [references/master_config.md](references/master_config.md)

### Slave Bot

Worker bot that:
- Handles user interactions via channels
- Executes AI tasks
- Uses MCP tools for extended capabilities
- Reports health status to master

**Deploy slave:**
```bash
BOT_NAME=worker-1 BOT_ID=worker-1 ./scripts/deploy_slave.sh
```

**Configuration:** See [references/slave_config.md](references/slave_config.md)

## Cluster Management

### Check Status

```bash
./scripts/manage_cluster.sh status
```

### Restart Bots

```bash
# Restart all
./scripts/manage_cluster.sh restart all

# Restart specific bot
./scripts/manage_cluster.sh restart nanobot-slave-1
```

### View Logs

```bash
# View last 100 lines
./scripts/manage_cluster.sh logs nanobot-master

# Follow logs
./scripts/manage_cluster.sh logs nanobot-slave-1 | head -500
```

### Execute Commands

```bash
# Check nanobot status inside container
./scripts/manage_cluster.sh exec nanobot-master nanobot status

# Open shell in container
./scripts/manage_cluster.sh exec nanobot-master /bin/bash
```

## Configuration

### Required Settings

Every bot needs:
1. **Provider API key** in `providers` section
2. **Channel configuration** (Telegram, Discord, etc.)
3. **Bot identity** for cluster management

### MCP Servers

Add MCP servers for extended capabilities:

```json
{
  "tools": {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
      },
      "brave-search": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-brave-search"],
        "env": {"BRAVE_API_KEY": "your-key"}
      }
    }
  }
}
```

See [references/mcp_setup.md](references/mcp_setup.md) for common MCP servers.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BOT_NAME` | Container name | nanobot-master / nanobot-slave |
| `BOT_ID` | Unique bot ID | hostname |
| `BOT_TYPE` | Bot type (master/slave) | - |
| `NAMESPACE` | Cluster namespace | nanobot |
| `CONFIG_DIR` | Config directory | ./configs/master or ./configs/slave |
| `DATA_DIR` | Data persistence | ./data/master or ./data/slave |
| `IMAGE` | Docker image | ghcr.io/hkuds/nanobot:latest |
| `PORT` | API port | 18790 |
| `MASTER_ENDPOINT` | Master bot URL (slaves only) | - |
| `MCP_MOUNTS` | Extra directories to mount | - |

## Example Deployments

### Single Machine - Master + Worker

```bash
# Deploy master
./scripts/deploy_master.sh

# Deploy worker connected to master
BOT_NAME=worker-1 BOT_ID=worker-1 \
  MASTER_ENDPOINT=http://nanobot-master:18790 \
  ./scripts/deploy_slave.sh
```

### Custom Named Cluster

```bash
NAMESPACE=prod-bot \
CONFIG_DIR=/opt/bot-config \
DATA_DIR=/data/bot-data \
./scripts/deploy_master.sh
```

### With MCP Workspace Mount

```bash
MCP_MOUNTS=/home/user/projects:/home/user/docs \
  ./scripts/deploy_slave.sh
```

## Directory Structure

```
nanobot-deploy/
├── scripts/
│   ├── deploy_master.sh      # Deploy master bot
│   ├── deploy_slave.sh       # Deploy slave bot
│   └── manage_cluster.sh     # Cluster management commands
├── references/
│   ├── master_config.md      # Master bot configuration guide
│   ├── slave_config.md       # Slave bot configuration guide
│   └── mcp_setup.md          # MCP server setup guide
└── assets/
    ├── master/config.json    # Master config template
    ├── slave/config.json     # Slave config template
    └── docker-compose.yml    # Full cluster compose file
```

## Security Notes

1. **API Keys**: Never commit config files with API keys
2. **Allow Lists**: Restrict `channels.*.allowFrom` for production
3. **Workspace Restriction**: Set `tools.restrictToWorkspace: true` for untrusted bots
4. **Master Access**: Limit master bot channel to admin users only
