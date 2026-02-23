---
name: neticrm-frontend
description: "netiCRM/CiviCRM frontend development standards and patterns for HTML, CSS, JavaScript, and Smarty templates. Use when editing .tpl/.css/.js files, fixing CSS layout or responsiveness issues, writing jQuery code, implementing Smarty template logic, checking browser compatibility, or reviewing frontend code quality. Ensures code consistency and avoids anti-patterns specific to this project."
---

# netiCRM Frontend Development

## Overview

This skill provides project-specific frontend development standards for netiCRM/CiviCRM. It ensures AI-generated code follows established patterns, naming conventions, and best practices specific to this codebase.

**Key principle**: Knowing syntax ≠ Writing high-quality code. This skill bridges the gap between general CSS/JS/HTML knowledge and project-specific quality standards.

## Quick Reference

### CSS
- **Standards**: See [css-standards.md](references/css-standards.md)
- **Browser Support**: See [browser-support-policy.md](references/browser-support-policy.md)

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
2. **Check Browser Support (MANDATORY for CSS)**: Before using any new or uncommon CSS technology, **you MUST consult [browser-support-policy.md](references/browser-support-policy.md)** to verify compatibility with the company's browser support policy. This includes:
   - Any CSS technology that appears "new," "experimental," or "uncommon"
   - Any technique using `::` pseudo-elements or `@` rules (except basic @media)
   - Technologies containing keywords like `scroll-`, `container-`, `@layer`, `@property`, etc.
   - **You MUST perform a WebSearch or WebFetch** to check current browser support - do NOT rely solely on your knowledge cutoff
3. **Follow Patterns**: Look for similar existing code in the project
4. **Use CSS Variables**: Always use defined CSS variables for colors and dimensions
5. **Test Responsively**: Verify code works across breakpoints (`ncg-*` grid)
6. **Validate Translations**: Ensure all user-facing text uses `{ts}` or `ts()`

## Examples

### Example 1: CSS — Fix mobile layout on a form

User says: "The contribution form looks broken on mobile"

Actions:
1. Read `references/css-standards.md` — Responsive Design and Grid System sections
2. Replace any `max-width` media queries with mobile-first `min-width`
3. Use `ncg-row` / `ncg-col-*` classes instead of custom flex/grid
4. Scope all selectors under `.crm-container`
5. Replace hardcoded colors with CSS variables (`--color-*`, `--rfm-*`)

Result: Responsive layout that follows netiCRM standards and won't leak styles to the host site

---

### Example 2: jQuery + JS — Add event handler for dynamic elements

User says: "Add a handler when user changes the payment method select"

Actions:
1. Read `references/javascript-patterns.md` — jQuery Usage and Event Handling sections
2. Use event delegation `cj(document).on('change', '#selector', fn)` — never bind directly to dynamic elements
3. Wrap code in `(function($) { 'use strict'; ... })(cj)` closure
4. If fetching CiviCRM data, use `.crmAPI()` with both `success` and `error` callbacks

Result: Correct jQuery pattern that avoids `$` conflicts and works with dynamically rendered markup

---

### Example 3: Smarty — Display translated text with dynamic values and a CRM link

User says: "Show a help message with the contact's name and a link to their profile"

Actions:
1. Read `references/smarty-templates.md` — Translation System, Security, and `{crmURL}` sections
2. Use `{ts 1=$var}text %1{/ts}` for parameterized strings — never interpolate variables inside `{ts}`
3. Escape user-supplied output: `{$var|escape}`
4. Generate URLs with `{crmURL p='...' q='...'}` — never hardcode paths
5. If adding inline JS, wrap in `{literal}` and use `{ts escape='js'}` for translated strings

Result: Properly translated, escaped, and CMS-portable template

## Common Issues

### CSS styles leaking to the host website
Cause: Selectors written without `.crm-container` prefix
Solution: Prefix all CiviCRM-specific selectors with `.crm-container`; use `body:has(.crm-container)` for body-level styles. See `references/css-standards.md` — CSS Selector Scoping section.

### Layout breaks on mobile
Cause: Desktop-first `max-width` media queries, or custom breakpoints instead of `ncg-*` variables
Solution: Rewrite using mobile-first `min-width` with `--ncg-breakpoint-*` variables; use `ncg-row` / `ncg-col-*` grid classes. See `references/css-standards.md` — Responsive Design section.

### jQuery `$` is not defined / conflict with other libraries
Cause: Using `$` directly instead of `cj()` outside a closure
Solution: Use `cj()` at the top level; pass `$` as a parameter inside `(function($) { ... })(cj)` or `cj(document).ready(function($) { ... })`. See `references/javascript-patterns.md` — jQuery Usage section.

### Event handler not firing on dynamically added elements
Cause: Binding events directly to elements that don't exist at DOM-ready time
Solution: Use event delegation — `cj(document).on('event', '.selector', fn)`. See `references/javascript-patterns.md` — Event Handling section.

### Smarty parse error with JavaScript `{ }` braces
Cause: Smarty interprets `{` and `}` inside `<script>` blocks
Solution: Wrap all inline JavaScript in `{literal}...{/literal}`. See `references/smarty-templates.md` — Asset Loading section.

### Translated string breaks JavaScript
Cause: `{ts}` output in JS context without escaping quotes
Solution: Always use `{ts escape='js'}` inside JavaScript strings. See `references/smarty-templates.md` — Translation System section.