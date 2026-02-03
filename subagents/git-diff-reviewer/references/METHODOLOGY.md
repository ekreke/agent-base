# Git Diff Reviewer - Detailed Methodology

This document contains the comprehensive review methodology for the git-diff-reviewer agent. Refer to this for detailed guidance on conducting thorough code reviews.

## Review Methodology

### Phase 1: Diff Analysis
- Run `git diff` or `git diff HEAD~1` (or appropriate commit range) to capture the changes
- Identify all modified, added, and deleted files
- Understand the scope and scale of changes

### Phase 2: Syntax & Style Review
- Check for syntax errors in all modified code
- Verify adherence to language-specific best practices
- Identify style inconsistencies within the diff
- Look for deprecated API usage or anti-patterns

### Phase 3: Logic & Architecture Review
- Analyze control flow for logical errors
- Check for edge cases and error handling gaps
- Verify data integrity and validation
- Assess performance implications
- Look for security vulnerabilities (SQL injection, XSS, etc.)
- Evaluate test coverage implications

### Phase 4: Business Intent Analysis
- Synthesize the functional purpose of changes:
  - What feature or bug fix is being implemented?
  - What user behavior is being enabled or changed?
  - What business rule or requirement is being enforced?
- Verify that code changes align with the apparent intent
- Flag discrepancies between implementation and likely business goals

### Phase 5: Prioritization & Reporting

Organize findings into four priority levels:

**P0 - Critical** (Must fix before merge)
- Syntax errors that break compilation
- Security vulnerabilities
- Data corruption risks
- Critical logic errors that cause incorrect behavior

**P1 - High** (Should fix before merge)
- Significant performance issues
- Missing error handling for likely failure cases
- Logic bugs in edge cases
- Breaking changes without migration path

**P2 - Medium** (Consider fixing)
- Code style inconsistencies
- Minor performance optimizations
- Missing input validation for unlikely cases
- Test coverage gaps

**P3 - Low** (Nice to have)
- Cosmetic improvements
- Suggestions for cleaner code organization
- Documentation improvements

## Edge Cases & Special Handling

- **Large diffs**: If the diff exceeds 500 lines, ask if the user wants a focused review on specific files or areas
- **Multiple commits**: When reviewing a range of commits, analyze the cumulative changes and note any breaking changes across commits
- **Language-specific patterns**: Adapt your review to the idioms and best practices of the programming language(s) involved
- **Framework changes**: Pay special attention to framework-specific patterns and potential breaking changes
- **Configuration changes**: Review config file changes for security implications and breaking changes

## Quality Standards

- **Be specific**: Reference exact file paths and line numbers when possible
- **Be constructive**: Frame feedback as improvement opportunities, not criticism
- **Be actionable**: Every issue should include a clear path to resolution
- **Be concise**: Don't repeat yourself; get to the point
- **Consider context**: Understand that not all issues need immediate fixing

## Self-Verification Checklist

Before presenting your review, verify:
- [ ] I've analyzed all changed files in the diff
- [ ] All issues are prioritized appropriately
- [ ] Each issue includes a specific fix suggestion
- [ ] Business intent is clearly articulated
- [ ] Tone is constructive and helpful
- [ ] No false positives (issues that aren't actually problems)
- [ ] Code examples in fixes are syntactically correct

When uncertain about an issue, mark it as lower priority and explain your uncertainty rather than presenting it as definitive. Ask for clarification if the business intent is unclear from the code changes alone.
