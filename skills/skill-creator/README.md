# Skill Creator

A meta-skill for creating effective skills that extend Claude's capabilities with specialized knowledge, workflows, or tool integrations.

## Overview

Skill Creator provides comprehensive guidance for creating new skills or updating existing ones. It covers skill structure, best practices, and design patterns.

## Core Principles

### Conciseness
- Context window is a shared resource
- Default assumption: Claude is already smart
- Only add context Claude doesn't already have
- Challenge each piece: "Does this justify its token cost?"

### Degrees of Freedom
Match specificity to task fragility:
- **High freedom**: Text instructions for multiple valid approaches
- **Medium freedom**: Pseudocode/scripts with parameters
- **Low freedom**: Specific scripts for error-prone operations

## Skill Structure

```
skill-name/
├── SKILL.md          # Required: YAML frontmatter + Markdown body
├── scripts/          # Optional: Executable code (Python/Bash/etc.)
├── references/       # Optional: Documentation for context loading
└── assets/           # Optional: Output files (templates, images, etc.)
```

### SKILL.md (Required)

**YAML Frontmatter:**
```yaml
---
name: skill-name
description: Clear description of when to use this skill
license: License terms (optional)
---
```

**Important:** The `name` and `description` fields are the ONLY things Claude reads to determine when to trigger a skill. Make them clear and comprehensive.

### Optional Components

**scripts/** - Executable code for:
- Repeatedly rewritten code
- Deterministic, reliable operations

**references/** - Documentation for:
- Domain-specific information
- API documentation
- Company policies/schemas

**assets/** - Output files:
- Templates (PPTX, HTML, React boilerplate)
- Images, icons, fonts
- Sample documents

## Included Resources

### Scripts
- `init_skill.py` - Initialize new skill templates
- `package_skill.py` - Package skills into .skill files

### References
- Domain-specific guidance and patterns

## Importing This Skill

```bash
# Import to global (recommended - available in all sessions)
python3 import_skills.py

# Import to local project only
python3 import_skills.py --local
```

## Usage

After importing, use the skill in Claude Code by describing the skill you want to create. Claude will provide guidance on structure, content, and best practices.

## License

See [LICENSE.txt](LICENSE.txt) for complete license terms.
