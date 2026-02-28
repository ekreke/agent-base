# Master Bot Configuration

Master bot is the central management bot that monitors and controls other nanobot instances.

## Role and Responsibilities

The master bot provides:

1. **Health Monitoring**: Periodically checks status of all slave bots
2. **Infrastructure Repair**: Restarts failed bots, fixes MCP services
3. **Configuration Management**: Updates skills and config across the cluster
4. **Log Aggregation**: Collects and analyzes logs from slave bots
5. **Alert System**: Notifies operators of critical issues

## Configuration Structure

```json
{
  "botIdentity": {
    "id": "nanobot-master",
    "type": "master",
    "namespace": "nanobot"
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5",
      "provider": "openrouter"
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "MASTER_BOT_TOKEN",
      "allowFrom": ["ADMIN_USER_ID"]
    }
  },
  "tools": {
    "restrictToWorkspace": true,
    "exec": {
      "allowedCommands": [
        "docker",
        "systemctl",
        "journalctl",
        "curl"
      ]
    }
  },
  "cluster": {
    "slaves": [
      {
        "id": "worker-1",
        "host": "worker-1.example.com",
        "port": 18790,
        "enabled": true
      }
    ],
    "healthCheckInterval": 300,
    "alertChannel": "telegram"
  }
}
```

## Required Permissions

Master bot needs elevated permissions for cluster management:

- Docker socket access (`/var/run/docker.sock`)
- System control (`systemctl`, `service`)
- Log access (`journalctl`, `/var/log`)
- Network access to reach slave bots

## Master-Slave Communication

### Health Check Endpoint

Slave bots expose a health endpoint:

```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "uptime": 12345,
  "version": "0.1.4",
  "lastActivity": "2024-02-28T10:30:00Z"
}
```

### RPC Commands

Master can send commands to slaves via:

```
POST /api/command
{
  "command": "restart",
  "timestamp": "2024-02-28T10:30:00Z"
}
```

Supported commands:
- `restart` - Restart the bot
- `update_config` - Update configuration
- `reload_skills` - Reload skills
- `get_logs` - Fetch recent logs

## Monitoring Tasks

Create these tasks in master's HEARTBEAT.md:

```markdown
## Periodic Tasks

- [ ] Check health of all slave bots every 5 minutes
- [ ] Restart any failed slave bots
- [ ] Check MCP service status on all nodes
- [ ] Aggregate error logs from last hour
- [ ] Send daily summary report
```
