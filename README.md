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

## skill-creator

The `skill-creator` is a meta-skill that helps you create new skills. It provides:

- Guidance on creating effective skills
- `init_skill.py` - Script to initialize new skill templates
- `package_skill.py` - Script to package skills into .skill files
- Best practices and design patterns

To use skill-creator, first import it to Claude Code:

```bash
# Import to global (recommended for reuse across projects)
python3 import_skills.py

# Or import to local project only
python3 import_skills.py --local
```

Then you can use it in Claude Code by describing the skill you want to create.
