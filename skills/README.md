# Skills

This directory contains skill definitions that extend Claude Code's capabilities.

## What are Skills?

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. They transform Claude from a general-purpose agent into a specialized agent equipped for specific domains or tasks.

## Skill Structure

```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + Markdown body
├── scripts/          # Optional: Executable code (Python/Bash/etc.)
├── references/       # Optional: Documentation for context loading
└── assets/           # Optional: Output files (templates, images, etc.)
```

## Available Skills

### skill-creator

Meta-skill for creating new skills. It provides guidance on:
- Skill structure and best practices
- Templates and patterns for effective skills
- Progressive disclosure design principles

**See:** [skill-creator/README.md](skill-creator/README.md)

### mcp-builder

Comprehensive guide for creating MCP (Model Context Protocol) servers that enable LLMs to interact with external services.

**See:** [mcp-builder/README.md](mcp-builder/README.md)

## Importing Skills

Skills can be imported from this directory using the import script:

```bash
# Import to global directory (available in all sessions)
python3 import_skills.py

# Import to local project (project-specific)
python3 import_skills.py --local
```

For more import options, see the [main README](../README.md#importing-skills).

## Creating New Skills

1. Use the `skill-creator` skill for guidance
2. Create a new directory under `skills/`
3. Add a `SKILL.md` with proper frontmatter and body content
4. Optionally add `scripts/`, `references/`, or `assets/` directories
5. Import using the script above
