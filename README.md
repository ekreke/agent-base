# Agent Base

AI skills and subagents baseline project.

## Project Structure

```
agent-base/
├── skills/              # Source directory for skill definitions
│   ├── skill-creator/  # Meta-skill for creating new skills
│   └── mcp-builder/    # MCP server building skill
├── subagents/           # Source directory for complex autonomous agents
│   ├── stress-test/    # Comprehensive stress testing agent
│   └── git-diff-reviewer/  # Git diff review agent
├── nanobot/            # AI 服务部署配置
│   └── k3s/           # k3s 集群部署配置和文档
├── .claude/            # Local deployment target (git-ignored)
│   ├── skills/         # Local skill imports
│   └── agents/         # Local agent configurations
├── import_skills.py    # Script to import skills/subagents
├── CLAUDE.md          # Project instructions for Claude Code
└── README.md          # This file
```

## Importing Skills

This project includes a script to import skills to Claude Code.

### Import Locations

The script supports two import locations:

- **Global** (`~/.claude/skills/`): Skills are available in all Claude Code sessions
- **Local** (`.claude/skills/`): Skills are available only in this project

### Usage

```bash
# Import to global directory (default)
python3 import_skills.py

# Import to local project directory
python3 import_skills.py --local

# Symlink mode (useful for development - changes sync automatically)
python3 import_skills.py --symlink
python3 import_skills.py --local --symlink

# Force overwrite existing skills
python3 import_skills.py --force

# Dry run - preview what would be done
python3 import_skills.py --dry-run
python3 import_skills.py --local --dry-run

# Custom source directory
python3 import_skills.py --source ./my-skills

# Custom target directory (overrides --local/--global-dir)
python3 import_skills.py --target ~/.claude/skills/
```

### Examples

```bash
# Import skills to global directory (available everywhere)
python3 import_skills.py

# Import skills to local project (project-specific)
python3 import_skills.py --local

# Development setup with symlinks
python3 import_skills.py --symlink
python3 import_skills.py --local --symlink

# Update existing skills
python3 import_skills.py --force --local

# Preview before importing
python3 import_skills.py --local --dry-run
```

## Skills

See [skills/README.md](skills/README.md) for detailed information about available skills.

### skill-creator

The `skill-creator` is a meta-skill that helps you create new skills. It provides:

- Guidance on creating effective skills
- `init_skill.py` - Script to initialize new skill templates
- `package_skill.py` - Script to package skills into .skill files
- Best practices and design patterns

See [skills/skill-creator/README.md](skills/skill-creator/README.md) for more details.

### mcp-builder

The `mcp-builder` skill provides comprehensive guidance for creating MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools.

See [skills/mcp-builder/README.md](skills/mcp-builder/README.md) for more details.

## Subagents

See [subagents/README.md](subagents/README.md) for detailed information about available subagents.

To use skill-creator, first import it to Claude Code:

```bash
# Import to global (recommended for reuse across projects)
python3 import_skills.py

# Or import to local project only
python3 import_skills.py --local
```

Then you can use it in Claude Code by describing the skill you want to create.

## Deployments

部署配置和文档，用于快速部署 AI 相关服务到 k3s 集群。

### nanobot/k3s

Nanobot AI 服务的 k3s 部署配置，包含：

- **deployment.yaml** - 2 副本部署配置
- **service.yaml** - NodePort 服务暴露 (30090)
- **kustomization.yaml** - Kustomize 配置
- **README.md** - 完整的部署指南和问题排查

快速开始：

```bash
# 1. 构建镜像
cd /path/to/nanobot
docker build -t nanobot:latest .

# 2. 导入到 k3s
docker save nanobot:latest | sudo k3s ctr images import -

# 3. 部署
cd /path/to/agent-base/nanobot/k3s
kubectl apply -k .

# 详细文档参见: nanobot/k3s/README.md
```

**参见:** [nanobot/k3s/README.md](nanobot/k3s/README.md)
