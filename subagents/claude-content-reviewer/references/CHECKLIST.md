# Claude Code Content Review Checklist

Complete checklist for reviewing skills and subagents against best practices.

## SKILL.md Frontmatter

### Required Fields
- [ ] **name** - Short, descriptive identifier (kebab-case recommended)
- [ ] **description** - 10-30 words explaining when to trigger
  - Should answer "When should Claude use this?"
  - Include trigger scenarios (after/before/when patterns)
  - Avoid implementation details

### Recommended Fields
- [ ] **model** - Preferred model (sonnet/opus/haiku)
- [ ] **color** - UI accent color
- [ ] **license** - License terms if applicable

## Description Quality

- [ ] **Clear trigger guidance** - Indicates when to use
  - Keywords: "when", "after", "before", "use for"
  - Action-oriented language
- [ ] **Appropriate length** - 10-30 words (not too short, not too long)
- [ ] **Unique identification** - Distinguishes from similar skills
- [ ] **No redundant info** - Doesn't repeat what's obvious from name

## Body Content Structure

### Required Sections
- [ ] **When to Trigger** - Clear usage examples with triggers
  - Multiple scenarios (3-5 examples)
  - Shows user request → assistant response pattern
  - Demonstrates Task tool usage (for subagents)
- [ ] **Required Tools** or **Available Tools** - Tool specifications
  - Uses YAML format for clarity
  - Lists specific tools with usage notes
- [ ] **Core Responsibilities** - What the agent/skill does

### Recommended Sections
- [ ] **Output Format** - Expected output structure
- [ ] **Edge Cases** - Special scenarios to handle
- [ ] **References** - Links to additional resources

## Progressive Disclosure

- [ ] **Metadata Level** (~100 words)
  - Frontmatter only
  - Always in context
  - Just name + description
- [ ] **Body Level** (<5k words, <500 lines)
  - SKILL.md content
  - Loaded on trigger
  - Focused instruction
- [ ] **Resource Level** (unlimited)
  - Scripts, references, assets
  - Conditionally loaded
  - Detailed implementation

## Content Quality

### Conciseness
- [ ] **No redundant content** - Each section adds unique value
- [ ] **No duplicate info** - SKILL.md vs references/
- [ ] **Token efficient** - Challenges each piece for justification
- [ ] **Assumes Claude intelligence** - Doesn't over-explain basics

### Degrees of Freedom
- [ ] **Appropriate specificity** for task type:
  - High freedom (text): Context-dependent, multiple valid approaches
  - Medium freedom (pseudocode/parameters): Preferred pattern exists
  - Low freedom (specific scripts): Error-prone, consistency critical
- [ ] **Balanced guidance** - Not too rigid, not too vague

### Tool Specifications
- [ ] **Accurate tool list** - All required tools specified
- [ ] **Clear usage notes** - How each tool is used
- [ ] **MCP integration** - Proper MCP server tools referenced
- [ ] **No unnecessary tools** - Only what's actually needed

## Directory Structure

### Required
- [ ] **SKILL.md** - Must exist in root
- [ ] **Valid YAML frontmatter** - Properly formatted

### Optional (but recommended when applicable)
- [ ] **scripts/** - For executable code
  - Scripts should be deterministic
  - Used for repeatedly rewritten code
- [ ] **references/** - For documentation
  - Should be conditionally referenced
  - Not duplicating SKILL.md content
- [ ] **assets/** - For output files
  - Templates, images, examples

### Should NOT Include
- [ ] **README.md** - Violates progressive disclosure
- [ ] **INSTALLATION_GUIDE.md** - Redundant
- [ ] **QUICK_REFERENCE.md** - Redundant
- [ ] **CHANGELOG.md** - Not needed for AI consumption
- [ ] Any auxiliary docs not directly needed by agent

## Script Quality (if scripts/ present)

- [ ] **Deterministic** - Same input → same output
- [ ] **Well-documented** - Clear purpose and usage
- [ ] **Error handling** - Robust failure modes
- [ ] **Executable independently** - Minimal dependencies
- [ ] **Patching-friendly** - Structure allows for modifications

## Reference Quality (if references/ present)

- [ ] **Clear citation in SKILL.md** - "See [X.md] for details"
- [ ] **No duplication** - Content not in SKILL.md
- [ ] **Domain-specific** - Focused, detailed information
- [ ] **Proper organization** - Easy to navigate

## Common Issues to Watch For

### Frontmatter Issues
- Missing required fields (name, description)
- Description too short (<10 words) or too long (>50 words)
- Unclear trigger guidance

### Structure Issues
- SKILL.md >500 lines
- Redundant documentation files (README.md, etc.)
- Missing scripts/references when they would help

### Content Issues
- Missing trigger examples
- Over-specified (too rigid)
- Under-specified (too vague)
- Duplicate content across files
- Explains things Claude already knows

### Progressive Disclosure Violations
- Implementation details in description
- Reference material in body
- Body content in frontmatter

## Context7 Query Patterns

When reviewing, use these context7 queries to validate against official docs:

### Skill Creation
- "Claude Code skill creation best practices"
- "SKILL.md format and frontmatter specification"
- "Progressive disclosure pattern for Claude Code extensions"

### Subagent Creation
- "Subagent vs skill differences in Claude Code"
- "Subagent structure and conventions"
- "When to use subagents vs skills"

### Tools & MCP
- "Using MCP servers in Claude Code skills"
- "MCP tool best practices"
- "Available tools in Claude Code"

## Priority Assessment

### P0 - Critical (Fix Immediately)
- Missing required frontmatter fields
- Cannot function as intended
- Breaking errors

### P1 - High (Fix Soon)
- Significant deviation from best practices
- Impacts effectiveness
- Missing trigger examples

### P2 - Medium (Fix When Convenient)
- Minor inconsistencies
- Optimization opportunities
- Redundant files

### P3 - Low (Nice to Have)
- Cosmetic improvements
- Minor documentation gaps
- Style inconsistencies

### P4 - Enhancement (Future)
- Advanced features
- Major refactor opportunities
- New capabilities
