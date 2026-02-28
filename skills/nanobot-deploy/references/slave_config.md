# Slave Bot Configuration

Slave (worker) bots are functional nanobot instances that perform specific tasks.

## Role and Responsibilities

Slave bots provide:

1. **Task Execution**: Run user-defined AI tasks
2. **Channel Integration**: Connect to chat platforms (Telegram, Discord, etc.)
3. **MCP Tool Access**: Use MCP services for extended capabilities
4. **Heartbeat Reporting**: Report status to master bot
5. **Local Logging**: Maintain local logs for debugging

## Configuration Structure

```json
{
  "botIdentity": {
    "id": "worker-1",
    "type": "slave",
    "namespace": "nanobot",
    "masterEndpoint": "http://nanobot-master:18790"
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
      "token": "SLAVE_BOT_TOKEN",
      "allowFrom": []
    }
  },
  "tools": {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
      }
    }
  },
  "skills": {
    "enabled": [
      "github",
      "weather",
      "tmux"
    ]
  }
}
```

## Key Configuration Options

### botIdentity

- `id`: Unique identifier for this bot (use hostname or custom name)
- `type`: Always "slave" for worker bots
- `namespace`: Grouping identifier (e.g., "nanobot")
- `masterEndpoint`: URL of master bot for registration and health reporting

### channels

Slave bots typically handle user-facing channels:

- **Telegram**: Personal assistant
- **Discord**: Community server bot
- **Slack**: Workspace automation
- **Email**: Email processing

### tools.mcpServers

MCP servers provide extended capabilities:

```json
{
  "tools": {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
      },
      "git": {
        "command": "uvx",
        "args": ["mcp-server-git", "--repository", "/workspace"]
      },
      "brave-search": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-brave-search"]
      }
    }
  }
}
```

## Health Check

Slave bots expose health endpoint at `http://<bot-host>:18790/health`

The health endpoint is automatically served by the nanobot gateway when running.

## Registration with Master

On startup, slave bot registers with master:

```bash
curl -X POST http://master:18790/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "id": "worker-1",
    "type": "slave",
    "endpoint": "http://worker-1:18790",
    "capabilities": ["telegram", "filesystem", "git"]
  }'
```

## Custom Slave Types

Different slave configurations for different purposes:

### Code Review Bot
```json
{
  "botIdentity": {"id": "code-reviewer"},
  "channels": {"github": {"enabled": true}},
  "skills": {"enabled": ["github", "code-review"]}
}
```

### Data Processing Bot
```json
{
  "botIdentity": {"id": "data-processor"},
  "tools": {
    "mcpServers": {
      "postgres": {"command": "npx", "args": ["@modelcontextprotocol/server-postgres"]}
    }
  }
}
```

### DevOps Bot
```json
{
  "botIdentity": {"id": "devops-helper"},
  "tools": {
    "restrictToWorkspace": false,
    "exec": {"allowedCommands": ["kubectl", "docker", "terraform"]}
  }
}
```
