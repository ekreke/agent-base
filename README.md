# Agent Base

AI skills and subagents baseline project.

## Project Structure

```
agent-base/
├── skill-creator/       # Tool for creating other skills
├── import_skills.py     # Script to import skills to Claude Code
└── README.md           # This file
```

## Importing Skills

This project includes a script to import skills to Claude Code's global skills directory (`~/.claude/skills/`).

### Usage

```bash
# Default: Copy skills from current directory
python3 import_skills.py

# Symlink mode (useful for development - changes sync automatically)
python3 import_skills.py --symlink

# Force overwrite existing skills
python3 import_skills.py --force

# Dry run - preview what would be done
python3 import_skills.py --dry-run

# Custom source directory
python3 import_skills.py --source ./my-skills

# Custom target directory
python3 import_skills.py --target ~/.claude/skills/
```

### Examples

```bash
# Import all skills from current directory
python3 import_skills.py

# Import from a subdirectory
python3 import_skills.py --source ./skills

# Update existing skills (force mode)
python3 import_skills.py --force --symlink
```

## skill-creator

The `skill-creator` is a meta-skill that helps you create new skills. It provides:

- Guidance on creating effective skills
- `init_skill.py` - Script to initialize new skill templates
- `package_skill.py` - Script to package skills into .skill files
- Best practices and design patterns

To use skill-creator, first import it to Claude Code:

```bash
python3 import_skills.py
```

Then you can use it in Claude Code by describing the skill you want to create.
