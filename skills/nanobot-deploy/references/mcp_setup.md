# MCP Server Setup for Nanobot

MCP (Model Context Protocol) servers extend nanobot capabilities with external tools.

## Common MCP Servers

### Filesystem Access

```json
{
  "tools": {
    "mcpServers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"]
      }
    }
  }
}
```

For Docker deployment, mount the directory:

```bash
-v /host/path:/workspace
```

Then use `/workspace` in MCP config.

### Git Operations

```json
{
  "tools": {
    "mcpServers": {
      "git": {
        "command": "uvx",
        "args": ["mcp-server-git", "--repository", "/workspace"]
      }
    }
  }
}
```

### Web Search (Brave)

```json
{
  "tools": {
    "mcpServers": {
      "brave-search": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-brave-search"],
        "env": {
          "BRAVE_API_KEY": "your-api-key"
        }
      }
    }
  }
}
```

### Postgres Database

```json
{
  "tools": {
    "mcpServers": {
      "postgres": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:pass@host:5432/db"]
      }
    }
  }
}
```

### HTTP/SSE Remote MCP

```json
{
  "tools": {
    "mcpServers": {
      "remote-mcp": {
        "url": "https://example.com/mcp/",
        "headers": {
          "Authorization": "Bearer xxxxx"
        },
        "toolTimeout": 60
      }
    }
  }
}
```

## Docker MCP Deployment

For MCP servers that need host access, use Docker bind mounts:

```bash
docker run -d \
  -v ~/.nanobot:/root/.nanobot \
  -v /home/user/projects:/workspace \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name nanobot-worker \
  nanobot gateway
```

Then configure filesystem MCP to use `/workspace`.

## MCP Timeout Configuration

Increase timeout for slow servers:

```json
{
  "tools": {
    "mcpServers": {
      "slow-server": {
        "command": "python",
        "args": ["mcp_server.py"],
        "toolTimeout": 120
      }
    }
  }
}
```

## Common MCP Issues

1. **Path Not Found**: Ensure directory exists in container
2. **Permission Denied**: Check file permissions on mounted volumes
3. **Command Not Found**: Use `npx -y` or `uvx` for auto-installation
4. **Timeout**: Increase `toolTimeout` for slow operations
