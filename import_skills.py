#!/usr/bin/env python3
"""
Import skills from current directory to Claude Code.

This script scans the current directory for skill folders (containing SKILL.md)
and imports them to either:
- Global: ~/.claude/skills/ (available in all Claude Code sessions)
- Local: .claude/skills/ (available only in this project)

Usage:
    python import_skills.py              # Import to global (copy mode)
    python import_skills.py --local      # Import to local project
    python import_skills.py --global-dir # Import to global directory
    python import_skills.py --copy       # Copy mode (default)
    python import_skills.py --symlink    # Symlink mode
    python import_skills.py --force      # Overwrite existing skills
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from typing import List, Tuple


def is_skill_dir(path: Path) -> bool:
    """Check if a directory is a valid skill directory."""
    return path.is_dir() and (path / "SKILL.md").exists()


def find_skill_dirs(scan_dir: Path) -> List[Path]:
    """Find all skill directories in the specified directory."""
    if not scan_dir.exists():
        print(f"Error: Directory '{scan_dir}' does not exist.")
        sys.exit(1)

    skill_dirs = [d for d in scan_dir.iterdir() if is_skill_dir(d)]

    if not skill_dirs:
        print(f"No skill directories found in '{scan_dir}'")
        print("A skill directory must contain a SKILL.md file.")
        sys.exit(1)

    return skill_dirs


def get_skill_name(skill_dir: Path) -> str:
    """Extract skill name from SKILL.md frontmatter."""
    skill_md = skill_dir / "SKILL.md"

    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Parse YAML frontmatter
        if lines and lines[0].strip() == '---':
            for line in lines[1:]:
                if line.strip() == '---':
                    break
                if line.startswith('name:'):
                    return line.split(':', 1)[1].strip()
    except Exception as e:
        print(f"Warning: Could not read SKILL.md: {e}")

    # Fallback to directory name
    return skill_dir.name


def import_skill_copy(skill_dir: Path, target_dir: Path, force: bool) -> Tuple[bool, str]:
    """Import a skill by copying it to the target directory."""
    skill_name = skill_dir.name
    target_path = target_dir / skill_name

    # Check if target already exists
    if target_path.exists():
        if not force:
            return False, f"Skipped (already exists): {skill_name}"
        shutil.rmtree(target_path)

    try:
        shutil.copytree(skill_dir, target_path)
        return True, f"Copied: {skill_name}"
    except Exception as e:
        return False, f"Error copying {skill_name}: {e}"


def import_skill_symlink(skill_dir: Path, target_dir: Path, force: bool) -> Tuple[bool, str]:
    """Import a skill by creating a symlink to the target directory."""
    skill_name = skill_dir.name
    target_path = target_dir / skill_name

    # Check if target already exists
    if target_path.exists():
        if not force:
            return False, f"Skipped (already exists): {skill_name}"
        # Remove existing file/directory/link
        if target_path.is_symlink():
            target_path.unlink()
        else:
            shutil.rmtree(target_path)

    try:
        # Create absolute symlink for reliability
        abs_source = skill_dir.resolve()
        target_path.symlink_to(abs_source)
        return True, f"Symlinked: {skill_name} -> {abs_source}"
    except Exception as e:
        return False, f"Error symlinking {skill_name}: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Import skills to Claude Code (local or global)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Import to global directory (default)
  python import_skills.py

  # Import to local project
  python import_skills.py --local

  # Import to global with symlink
  python import_skills.py --global-dir --symlink

  # Update local skills
  python import_skills.py --local --force
        """
    )
    parser.add_argument(
        '--local',
        action='store_true',
        help='Import to local project .claude/skills/ (project-specific)'
    )
    parser.add_argument(
        '--global-dir',
        action='store_true',
        help='Import to global ~/.claude/skills/ (available in all projects) [default]'
    )
    parser.add_argument(
        '--copy',
        action='store_true',
        help='Copy skills to target directory (default)'
    )
    parser.add_argument(
        '--symlink',
        action='store_true',
        help='Create symlinks to skills (useful for development)'
    )
    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Overwrite existing skills in the target directory'
    )
    parser.add_argument(
        '--source', '-s',
        type=Path,
        default=Path.cwd(),
        help='Source directory to scan for skills (default: current directory)'
    )
    parser.add_argument(
        '--target', '-t',
        type=Path,
        default=None,
        help='Custom target directory (overrides --local and --global)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without actually doing it'
    )

    args = parser.parse_args()

    # Determine mode
    use_symlink = args.symlink
    if args.copy and args.symlink:
        print("Error: --copy and --symlink are mutually exclusive")
        sys.exit(1)

    # Determine target directory
    if args.target:
        # Custom target overrides local/global
        target_dir = args.target
        location_type = "custom"
    elif args.local and args.global_dir:
        print("Error: --local and --global-dir are mutually exclusive")
        sys.exit(1)
    elif args.local:
        # Local project directory
        target_dir = args.source / '.claude' / 'skills'
        location_type = "local project"
    else:
        # Global directory (default)
        target_dir = Path.home() / '.claude' / 'skills'
        location_type = "global"

    # Setup target directory
    if not args.dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    # Find skill directories
    print(f"Scanning '{args.source}' for skills...")
    skill_dirs = find_skill_dirs(args.source)
    print(f"Found {len(skill_dirs)} skill(s)")
    print(f"Target: {target_dir} ({location_type})\n")

    # Import each skill
    success_count = 0
    skip_count = 0
    error_count = 0

    for skill_dir in skill_dirs:
        if args.dry_run:
            mode = "symlink" if use_symlink else "copy"
            print(f"Would {mode}: {skill_dir.name}")
            continue

        if use_symlink:
            success, message = import_skill_symlink(skill_dir, target_dir, args.force)
        else:
            success, message = import_skill_copy(skill_dir, target_dir, args.force)

        print(message)

        if success:
            success_count += 1
        elif "Skipped" in message:
            skip_count += 1
        else:
            error_count += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"Import complete!")
    print(f"  Location: {location_type}")
    print(f"  Imported: {success_count}")
    print(f"  Skipped:  {skip_count}")
    print(f"  Errors:   {error_count}")
    print(f"  Target:   {target_dir}")
    print(f"{'='*60}")

    if error_count > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
