# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agent Base is a repository for managing extensions for Claude Code, including both skills and subagents.

**Skills** are modular, self-contained packages that extend Claude's capabilities with specialized knowledge, workflows, and tools. They use progressive disclosure: metadata (always in context) → SKILL.md body (when triggered) → bundled resources (as needed).

**Subagents** are more complex autonomous workflows that combine instructions, executable scripts, references, and templates to perform complete multi-step tasks. Subagents differ from skills in scope: skills provide guidance for Claude to follow, while subagents provide complete automation with executable scripts.

**Key Concept:** Both skills and subagents transform Claude from a general-purpose agent into a specialized agent equipped for specific domains or tasks.

## Development Commands

### Importing Skills

```bash
# Import to global directory (default) - available in all Claude Code sessions
python3 import_skills.py

# Import to local project - project-specific skills only
python3 import_skills.py --local

# Symlink mode (development - changes sync automatically)
python3 import_skills.py --symlink
python3 import_skills.py --local --symlink

# Force overwrite existing skills
python3 import_skills.py --force

# Dry run - preview without executing
python3 import_skills.py --dry-run

# Custom source/target directories
python3 import_skills.py --source ./my-skills --target ~/.claude/skills/
```

### Creating Skills

Use the `skill-creator` skill (located in `skills/skill-creator/`) to create new skills. It provides:
- Guidance on skill structure and best practices
- Templates and patterns for effective skills
- Progressive disclosure design principles

Import skill-creator first:
```bash
python3 import_skills.py  # or --local for project-only
```

### Creating Subagents

Subagents are more complex than skills - they include executable scripts for complete automation workflows. To create a new subagent:

1. Create a directory under `subagents/agent-name/`
2. Include a `SKILL.md` with proper frontmatter describing the agent
3. Add `scripts/` for executable automation
4. Add `references/` for documentation and patterns
5. Add `templates/` for output formats

Import subagents using the same script:
```bash
python3 import_skills.py --source ./subagents --local
```

See `subagents/README.md` for details on available subagents.

## Architecture

### Skill Structure

```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + Markdown body
├── scripts/          # Optional: Executable code (Python/Bash/etc.)
├── references/       # Optional: Documentation for context loading
└── assets/           # Optional: Output files (templates, images, etc.)
```

### SKILL.md Format

**Required YAML frontmatter:**
```yaml
---
name: skill-name
description: Clear description of when to use this skill
license: License terms (optional)
---
```

**Important:** The `name` and `description` fields are the ONLY things Claude reads to determine when to trigger a skill. Make them clear and comprehensive.

### Progressive Disclosure System

1. **Metadata Level** (~100 words) - Always in context; just name + description from frontmatter
2. **Body Level** (<5k words) - SKILL.md content loaded when skill triggers
3. **Resource Level** (unlimited) - Scripts, references, assets loaded conditionally

### Import Locations

- **Global:** `~/.claude/skills/` - Available in all Claude Code sessions
- **Local:** `.claude/skills/` - Project-specific only (excluded from git)

### Import Modes

- **Copy mode** (default): Duplicates skills to target directory
- **Symlink mode**: Creates symlinks for development workflow

## Core Design Principles

### Conciseness
- Context window is a shared resource
- Default assumption: Claude is already smart
- Only add context Claude doesn't already have
- Challenge each piece: "Does this justify its token cost?"

### Degrees of Freedom
Match specificity to task fragility:
- **High freedom** (text instructions): Multiple valid approaches, context-dependent
- **Medium freedom** (pseudocode/scripts with parameters): Preferred pattern exists
- **Low freedom** (specific scripts): Error-prone operations, consistency critical

### File Organization Rules

**DO include:**
- `SKILL.md` (required)
- `scripts/` for repeatedly rewritten code or deterministic operations
- `references/` for documentation loaded as needed
- `assets/` for files used in output (templates, images, etc.)

**DO NOT include:**
- README.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md, CHANGELOG.md
- Any auxiliary documentation not directly needed by the AI agent
- Duplicate content between SKILL.md and references/

### Code Organization

- `import_skills.py` - Main utility for skill/subagent deployment
- `skills/` - Source directory for skill definitions
- `subagents/` - Source directory for complex autonomous agents
  - `subagents/stress-test/` - Comprehensive stress testing agent
- `.claude/skills/` - Local deployment target (git-ignored)

## Skill Development Workflow

1. Import skill-creator to understand best practices
2. Plan skill contents (scripts, references, assets needed)
3. Create skill directory with SKILL.md (frontmatter + body)
4. Add optional resources (scripts/, references/, assets/)
5. Test import with `--dry-run`
6. Import with desired mode (copy/symlink, local/global)

## Key Patterns

### Progressive Disclosure in SKILL.md

Keep SKILL.md under 500 lines. Split content when:
- Supporting multiple variations/frameworks/options
- Domain-specific information needed
- Reference material grows large

Reference files from SKILL.md with clear usage guidance:
```markdown
## Advanced Features
- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
```

### Script Usage

Scripts should be:
- Deterministic and reliable
- Used for repeatedly rewritten code
- Executable without full context load (when possible)
- Read by Claude only for patching or environment adjustments
