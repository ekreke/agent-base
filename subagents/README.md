# Subagents

This directory contains agent definitions - specialized agent personas for autonomous task execution.

## Purpose

Subagents define specialized agent personas that can perform complex multi-step tasks autonomously. Each subagent includes:
- **Role Definition**: The agent's expertise and responsibilities
- **Triggering Criteria**: When to invoke this agent
- **Methodology**: Step-by-step approach for the agent's domain
- **Quality Standards**: Expected output quality and completeness

## Difference from Skills

| Skills | Subagents |
|--------|-----------|
| Teaching materials that guide Claude | Autonomous agent personas |
| Provide instructions and patterns | Define complete workflows and methodologies |
| User works through the problem with guidance | Agent works autonomously to complete the task |
| "How to do X" | "An agent that does X for you" |

## Available Subagents

### git-diff-reviewer

**Purpose**: Comprehensive code review via git diff analysis.

**Expertise**:
- Syntax and style verification across multiple languages
- Logic problem identification (race conditions, edge cases, data flow)
- Business intent analysis and alignment
- Security vulnerability detection
- Prioritized, actionable feedback

**Trigger this agent when**:
- After making commits and wanting feedback before pushing
- Before merging pull requests
- When requesting code review on recent changes
- After user runs git commands (proactive review)

**Example usage**:
```
"I just committed some changes. Can you review them?"
"Here's my PR for the new payment integration"
"git commit -m 'Fix race condition in order processing'"
```

### stress-test-orchestrator

**Purpose**: Comprehensive stress testing and performance analysis for codebase functionality.

**Expertise**:
- Performance testing architecture
- Load testing across diverse technology stacks
- Bottleneck identification and breaking point analysis
- Actionable performance recommendations

**Trigger this agent when**:
- User requests stress testing, load testing, or performance testing
- Validating system behavior under high load or extreme conditions
- Identifying performance bottlenecks in specific features
- Generating complete stress test reports with metrics

**Example usage**:
```
"Can you stress test the authentication API?"
"I need to validate our database can handle 1000 concurrent users"
"We're deploying soon - stress test the payment system"
```

## Structure

```
subagents/
└── agent-name/
    └── SKILL.md    # Complete agent definition with role, methodology, and standards
```

## Agent Definition Format

Each subagent's SKILL.md contains:

1. **Frontmatter**:
   - `name`: Agent identifier
   - `description`: Triggering criteria with examples
   - `model`: Preferred model (sonnet/opus/haiku)
   - `color`: Display color

2. **Role Definition**:
   - Agent's expertise and background
   - Core responsibilities
   - Quality standards

3. **Methodology**:
   - Step-by-step workflow
   - Technology-specific approaches
   - Metrics and success criteria

4. **Communication Style**:
   - How to present findings
   - Report structure and format

## Creating New Subagents

To create a new subagent:

1. Create a directory: `subagents/agent-name/`
2. Add a comprehensive `SKILL.md` with:
   - Clear triggering criteria (with examples)
   - Agent role and expertise definition
   - Complete methodology for the domain
   - Quality standards and output expectations
3. Import the subagent:
   ```bash
   python3 import_skills.py --source ./subagents --local
   ```
