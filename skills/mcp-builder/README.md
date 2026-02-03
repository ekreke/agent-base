# MCP Builder

A comprehensive guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools.

## Overview

The MCP Builder skill provides complete guidance for building MCP servers that integrate external APIs or services. It covers both Python (FastMCP) and Node/TypeScript (MCP SDK) implementations.

## Key Topics Covered

### Phase 1: Research and Planning
- Modern MCP design principles
- Tool naming and discoverability
- Context management strategies
- API coverage vs workflow tools

### Phase 2: Implementation
- Project structure setup
- Core infrastructure (API clients, error handling)
- Tool implementation with proper schemas
- Testing and validation

### Phase 3: Deployment
- Server configuration
- Transport mechanisms (stdio, streamable HTTP)
- Production best practices

## Language-Specific Guides

- **TypeScript (Recommended)**: See [reference/node_mcp_server.md](reference/node_mcp_server.md)
- **Python**: See [reference/python_mcp_server.md](reference/python_mcp_server.md)
- **Best Practices**: See [reference/mcp_best_practices.md](reference/mcp_best_practices.md)

## Included Resources

### Scripts
- Utility scripts for MCP server development

### References
- TypeScript MCP server guide
- Python MCP server guide
- MCP best practices documentation

## Importing This Skill

```bash
# Import to global (recommended)
python3 import_skills.py

# Import to local project only
python3 import_skills.py --local
```

## License

See [LICENSE.txt](LICENSE.txt) for complete license terms.
