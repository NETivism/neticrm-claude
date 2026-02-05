---
name: neticrm-frontend
description: "netiCRM/CiviCRM frontend development standards and patterns for HTML, CSS, JavaScript, and Smarty templates. Use this skill when working with frontend code in the netiCRM project to ensure code quality, maintainability, and consistency with project conventions. Apply this skill when writing, modifying, inspecting, reviewing, analyzing, or assessing code quality."
---

# netiCRM Frontend Development

## Overview

This skill provides project-specific frontend development standards for netiCRM/CiviCRM. It ensures AI-generated code follows established patterns, naming conventions, and best practices specific to this codebase.

**Key principle**: Knowing syntax ≠ Writing high-quality code. This skill bridges the gap between general CSS/JS/HTML knowledge and project-specific quality standards.

## Quick Reference

### CSS
- **Standards**: See [css-standards.md](references/css-standards.md)

### JavaScript
- **Patterns**: See [javascript-patterns.md](references/javascript-patterns.md)

### Smarty Templates
- **Guide**: See [smarty-templates.md](references/smarty-templates.md)

### HTML Structure
- **Conventions**: See [html-conventions.md](references/html-conventions.md)

## Code Quality Principles

1. **Maintainability First**: Code should be easy to understand and modify
2. **Consistency**: Follow existing patterns in the codebase
3. **Performance**: Consider CSS specificity, selector performance, and asset loading
4. **Accessibility**: Use semantic HTML and proper ARIA attributes
5. **Localization**: Always use translation functions for user-facing text

## Development Workflow

1. **Check References First**: Before writing code, review the relevant reference file
2. **Follow Patterns**: Look for similar existing code in the project
3. **Use CSS Variables**: Always use defined CSS variables for colors and dimensions
4. **Test Responsively**: Verify code works across breakpoints (`ncg-*` grid)
5. **Validate Translations**: Ensure all user-facing text uses `{ts}` or `ts()`

## Getting Started

For detailed information on any topic:
1. Identify which area you're working on (CSS/JS/Smarty/HTML)
2. Read the corresponding reference file
3. Follow the patterns and examples provided
4. Avoid the documented anti-patterns