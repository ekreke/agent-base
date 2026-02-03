# Context7 MCP Server Usage Guide

Guide for using the context7 MCP server to query Claude Code documentation.

## What is Context7?

Context7 is an MCP (Model Context Protocol) server that provides up-to-date documentation for programming libraries and frameworks, including Claude Code.

## Available Context7 Tools

### 1. resolve-library-id
Resolves a package/product name to a Context7-compatible library ID.

**Parameters:**
- `query` (required): The user's original question or task
- `libraryName` (required): Library name to search

**Usage:**
First call this to get the correct library ID, then use that ID with `query-docs`.

**Example:**
```
Query: "Claude Code skill creation"
LibraryName: "claude-code"
Returns: "/anthropic/claude-code"
```

### 2. query-docs
Queries documentation using a library ID.

**Parameters:**
- `libraryId` (required): Exact Context7-compatible library ID
  - Format: `/org/project` or `/org/project/version`
  - Must get from `resolve-library-id` first (unless user provides it)
- `query` (required): Specific question about the library

**Important:**
- Only call this 3 times per question maximum
- If you can't find what you need after 3 calls, use your best knowledge

## Claude Code Library IDs

The official Claude Code library ID is:
```
/anthropic/claude-code
```

## Useful Context7 Queries for Claude Code

### Skills and Subagents

```yaml
Query: "SKILL.md format and frontmatter specification"
Purpose: Get official SKILL.md structure requirements

Query: "Claude Code skill creation best practices"
Purpose: Learn recommended patterns for skills

Query: "Subagent vs skill differences in Claude Code"
Purpose: Understand when to use each

Query: "Progressive disclosure pattern for Claude Code extensions"
Purpose: Learn how to structure content effectively
```

### Tools and MCP

```yaml
Query: "Using MCP servers in Claude Code skills"
Purpose: How to integrate MCP tools in skills

Query: "Available tools in Claude Code"
Purpose: Complete list of built-in tools

Query: "MCP tool best practices"
Purpose: Recommended patterns for MCP usage
```

### Hooks and Configuration

```yaml
Query: "Claude Code hooks configuration"
Purpose: How to set up and use hooks

Query: "Hook patterns and examples"
Purpose: Common hook use cases

Query: "Claude Code settings and configuration"
Purpose: Available configuration options
```

## Workflow for Content Review

When reviewing Claude Code customizations:

1. **Resolve library ID** (if needed)
   ```
   resolve-library-id(
     query: "Claude Code documentation for reviewing skills",
     libraryName: "claude-code"
   )
   ```

2. **Query best practices**
   ```
   query-docs(
     libraryId: "/anthropic/claude-code",
     query: "Skill creation best practices and SKILL.md format"
   )
   ```

3. **Query specific patterns**
   ```
   query-docs(
     libraryId: "/anthropic/claude-code",
     query: "Progressive disclosure and content organization"
   )
   ```

4. **Query tools/MCP** (if reviewing tool usage)
   ```
   query-docs(
     libraryId: "/anthropic/claude-code",
     query: "MCP server integration in skills"
   )
   ```

## Tips for Effective Queries

### Be Specific
- Good: "SKILL.md frontmatter required fields"
- Bad: "skills"

### Include Context
- Good: "How to structure When to Trigger examples in SKILL.md"
- Bad: "trigger examples"

### Focus on Problems
- Good: "Common mistakes in skill description fields"
- Bad: "skill descriptions"

## Query Limits

- **Maximum 3 query-docs calls per question**
- If you exhaust queries without finding answers:
  - Use the best information you have
  - Note in the report that some validation couldn't be completed
  - Suggest manual review of official docs

## Handling Results

### When Context7 Returns Useful Info
- Incorporate into review findings
- Cite as reference in recommendations
- Use specific examples from docs

### When Context7 Returns Limited Info
- Cross-reference with your knowledge
- Note gaps in documentation
- Provide recommendations based on general principles

### When Context7 Fails
- Fall back to built-in knowledge
- Note the limitation in the report
- Suggest manual verification

## Example Review Workflow

```
1. User requests review of skills

2. Resolve library ID:
   mcp__context7__resolve-library-id(
     query: "Review Claude Code skills for best practices",
     libraryName: "claude-code"
   )
   → Returns: "/anthropic/claude-code"

3. Query SKILL.md format:
   mcp__context7__query-docs(
     libraryId: "/anthropic/claude-code",
     query: "SKILL.md required fields and format specification"
   )

4. Query best practices:
   mcp__context7__query-docs(
     libraryId: "/anthropic/claude-code",
     query: "Skill creation best practices and progressive disclosure"
   )

5. Scan and analyze content using script

6. Generate report with Context7-backed recommendations
```

## Reference

- Context7 GitHub: https://github.com/pemin/node-context7
- MCP Protocol: https://modelcontextprotocol.io/
- Claude Code Docs: https://docs.anthropic.com/en/docs/claude-code
