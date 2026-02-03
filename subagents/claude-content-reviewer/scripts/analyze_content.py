#!/usr/bin/env python3
"""
Claude Code Content Analyzer

Analyzes skills and subagents for quality, structure, and best practices compliance.
Used by the claude-content-reviewer agent to provide detailed assessments.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Finding:
    """A single review finding."""
    priority: str  # P0-P4
    category: str
    location: str
    issue: str
    impact: str
    reference: str = ""
    effort: str = "medium"


@dataclass
class CheckResult:
    """Result of a single check."""
    item: str
    status: str  # pass/fail/partial
    details: str = ""


@dataclass
class ContentReview:
    """Complete review of a skill or subagent."""
    name: str
    type: str  # skill or subagent
    path: str
    findings: List[Finding] = field(default_factory=list)
    checks: List[CheckResult] = field(default_factory=list)


class SkillMarkdownAnalyzer:
    """Analyzes SKILL.md files for quality and completeness."""

    REQUIRED_FRONTMATTER_FIELDS = ['name', 'description']
    RECOMMENDED_FRONTMATTER_FIELDS = ['model', 'color']

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.content = None
        self.frontmatter = {}
        self.body = ""

    def read(self) -> bool:
        """Read and parse the SKILL.md file."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.content = f.read()
            self._parse_frontmatter()
            self.body = self._extract_body()
            return True
        except Exception as e:
            print(f"Error reading {self.filepath}: {e}")
            return False

    def _parse_frontmatter(self):
        """Extract YAML frontmatter from the file."""
        match = re.match(r'^---\n(.*?)\n---\n(.*)', self.content, re.DOTALL)
        if match:
            frontmatter_text = match.group(1)
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    self.frontmatter[key.strip()] = value.strip()

    def _extract_body(self) -> str:
        """Extract the body content after frontmatter."""
        match = re.match(r'^---\n.*?\n---\n(.*)', self.content, re.DOTALL)
        return match.group(1) if match else ""

    def analyze(self) -> ContentReview:
        """Perform comprehensive analysis of the SKILL.md."""
        review = ContentReview(
            name=self.frontmatter.get('name', 'Unknown'),
            type='skill' if 'skills/' in self.filepath else 'subagent',
            path=self.filepath
        )

        # Check frontmatter
        self._check_frontmatter(review)

        # Check description quality
        self._check_description(review)

        # Check body content
        self._check_body_content(review)

        # Check structure
        self._check_structure(review)

        return review

    def _check_frontmatter(self, review: ContentReview):
        """Check frontmatter completeness."""
        for field in self.REQUIRED_FRONTMATTER_FIELDS:
            if field in self.frontmatter:
                review.checks.append(CheckResult(
                    item=f"Frontmatter: {field}",
                    status="pass",
                    details=f"Found: {self.frontmatter[field]}"
                ))
            else:
                review.findings.append(Finding(
                    priority="P0",
                    category="SKILL.md Quality",
                    location=self.filepath,
                    issue=f"Missing required frontmatter field: {field}",
                    impact="Cannot properly trigger or identify the skill",
                    reference="See context7: 'SKILL.md format and frontmatter specification'",
                    effort="low"
                ))

        for field in self.RECOMMENDED_FRONTMATTER_FIELDS:
            status = "pass" if field in self.frontmatter else "partial"
            review.checks.append(CheckResult(
                item=f"Frontmatter: {field} (recommended)",
                status=status,
                details="Present" if field in self.frontmatter else "Not present (optional)"
            ))

    def _check_description(self, review: ContentReview):
        """Check description quality."""
        description = self.frontmatter.get('description', '')

        # Check length
        word_count = len(description.split())
        if word_count < 10:
            review.findings.append(Finding(
                priority="P1",
                category="SKILL.md Quality",
                location=f"{self.filepath}:description",
                issue="Description too short",
                impact="Unclear when to trigger this skill",
                reference="Description should be 10-30 words explaining when to use",
                effort="low"
            ))
        elif word_count > 50:
            review.findings.append(Finding(
                priority="P2",
                category="SKILL.md Quality",
                location=f"{self.filepath}:description",
                issue="Description too long",
                impact="Wastes context tokens in metadata",
                reference="Keep description concise; save details for body",
                effort="low"
            ))
        else:
            review.checks.append(CheckResult(
                item="Description length",
                status="pass",
                details=f"{word_count} words"
            ))

        # Check for trigger guidance
        trigger_keywords = ['when to', 'use for', 'trigger', 'after', 'before']
        has_trigger_guidance = any(kw in description.lower() for kw in trigger_keywords)

        review.checks.append(CheckResult(
            item="Description: trigger guidance",
            status="pass" if has_trigger_guidance else "partial",
            details="Explains when to trigger" if has_trigger_guidance else "Could be clearer about when to use"
        ))

    def _check_body_content(self, review: ContentReview):
        """Check body content quality."""
        line_count = len(self.body.split('\n'))

        # Check progressive disclosure (body should be under 500 lines)
        if line_count > 500:
            review.findings.append(Finding(
                priority="P1",
                category="Content Effectiveness",
                location=f"{self.filepath}:body",
                issue=f"Body too long ({line_count} lines)",
                impact="Exceeds progressive disclosure best practices",
                reference="See CLAUDE.md: Keep SKILL.md under 500 lines",
                effort="medium",
            ))
            review.checks.append(CheckResult(
                item="Body length",
                status="fail",
                details=f"{line_count} lines (should be <500)"
            ))
        else:
            review.checks.append(CheckResult(
                item="Body length",
                status="pass",
                details=f"{line_count} lines"
            ))

        # Check for trigger examples
        has_trigger_examples = '## When to Trigger' in self.body or '### Trigger Examples' in self.body
        review.checks.append(CheckResult(
            item="Trigger examples",
            status="pass" if has_trigger_examples else "partial",
            details="Present" if has_trigger_examples else "Missing trigger examples"
        ))

        # Check for tool specifications
        has_tool_specs = '## Required Tools' in self.body or '## Available Tools' in self.body
        review.checks.append(CheckResult(
            item="Tool specifications",
            status="pass" if has_tool_specs else "partial",
            details="Present" if has_tool_specs else "Should specify required tools"
        ))

    def _check_structure(self, review: ContentReview):
        """Check directory structure."""
        base_dir = Path(self.filepath).parent

        # Check for recommended directories
        for dir_name in ['scripts', 'references', 'assets']:
            dir_path = base_dir / dir_name
            if dir_path.exists():
                review.checks.append(CheckResult(
                    item=f"Directory: {dir_name}/",
                    status="pass",
                    details=f"Found with {len(list(dir_path.iterdir()))} items"
                ))

        # Check for inappropriate files
        inappropriate_files = ['README.md', 'INSTALLATION_GUIDE.md', 'QUICK_REFERENCE.md']
        for filename in inappropriate_files:
            if (base_dir / filename).exists():
                review.findings.append(Finding(
                    priority="P2",
                    category="Structure & Organization",
                    location=f"{base_dir}/{filename}",
                    issue=f"Redundant documentation file: {filename}",
                    impact="Violates progressive disclosure; content should be in SKILL.md",
                    reference="See CLAUDE.md: DO NOT include README.md, etc.",
                    effort="low"
                ))


def scan_directory(root_dir: str) -> List[str]:
    """Scan for all SKILL.md files."""
    root = Path(root_dir)
    skill_files = []

    # Scan skills directory
    skills_dir = root / 'skills'
    if skills_dir.exists():
        skill_files.extend(skills_dir.glob('**/SKILL.md'))

    # Scan subagents directory
    subagents_dir = root / 'subagents'
    if subagents_dir.exists():
        skill_files.extend(subagents_dir.glob('**/SKILL.md'))

    return [str(f) for f in skill_files]


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = os.getcwd()

    print(f"Scanning {target_dir} for Claude Code content...\n")

    skill_files = scan_directory(target_dir)

    if not skill_files:
        print("No SKILL.md files found.")
        return

    print(f"Found {len(skill_files)} skill/subagent definitions:\n")

    all_reviews = []

    for skill_file in skill_files:
        print(f"Analyzing: {skill_file}")
        analyzer = SkillMarkdownAnalyzer(skill_file)

        if analyzer.read():
            review = analyzer.analyze()
            all_reviews.append(review)

            # Print summary
            print(f"  Name: {review.name}")
            print(f"  Type: {review.type}")
            print(f"  Checks: {len(review.checks)}")
            print(f"  Findings: {len(review.findings)}")

            if review.findings:
                print(f"  Issues:")
                for finding in review.findings:
                    print(f"    [{finding.priority}] {finding.issue}")
            print()

    # Print overall summary
    total_findings = sum(len(r.findings) for r in all_reviews)
    by_priority = {}

    for review in all_reviews:
        for finding in review.findings:
            by_priority[finding.priority] = by_priority.get(finding.priority, 0) + 1

    print("\n" + "="*60)
    print("OVERALL SUMMARY")
    print("="*60)
    print(f"Total items reviewed: {len(all_reviews)}")
    print(f"Total findings: {total_findings}")

    if by_priority:
        print("\nFindings by priority:")
        for priority in sorted(by_priority.keys()):
            print(f"  {priority}: {by_priority[priority]}")


if __name__ == '__main__':
    main()
