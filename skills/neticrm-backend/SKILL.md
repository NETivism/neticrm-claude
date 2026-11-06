---
name: neticrm-backend
description: "netiCRM/CiviCRM PHP backend standards for BAO, DAO, Form, and API classes. Use when writing PHP in /CRM/, implementing BAO business logic, Form handlers, API v3 endpoints, Menu XML routes, or checking permissions. Ensures CiviCRM class hierarchy, naming conventions, and security practices."
---

# netiCRM Backend Development

## Overview

This skill provides project-specific PHP backend standards for netiCRM/CiviCRM. It bridges the gap between general PHP knowledge and the CiviCRM-specific architecture this project requires.

**Key principle**: CiviCRM has a rigid class hierarchy (DAO → BAO → Form/Page). Knowing PHP ≠ knowing where and how to implement logic correctly.

## Quick Reference

### Class-to-File Mapping
```
CRM_Core_Transaction          → /CRM/Core/Transaction.php
CRM_Contribute_BAO_Contribution → /CRM/Contribute/BAO/Contribution.php
CRM_Contribute_Form_Contribution → /CRM/Contribute/Form/Contribution.php
```

### Layer Responsibilities
| Layer | Location | Responsibility |
|-------|----------|---------------|
| DAO | `/CRM/**/DAO/` | Auto-generated from XML — **never edit manually** |
| BAO | `/CRM/**/BAO/` | Business logic — implement here |
| Form | `/CRM/**/Form/` | Form handling: `preProcess()` → `buildForm()` → `postProcess()` |
| API | `/api/v3/` | External API endpoints |

### Code Style (summary — see [php-coding-style.md](references/php-coding-style.md) for full rules)
- **Indentation**: 2 spaces
- **Class names**: CamelCase (`CRM_Contribute_BAO_Contribution`)
- **Methods**: camelCase (`processContribution()`)
- **Properties**: `_camelCase` (underscore prefix)
- **Comparisons**: `===` and `!==`
- **Constants**: `TRUE`, `FALSE`, `NULL` — uppercase
- **Arrays**: short syntax `[]` always
- **Braces**: opening brace same line; `else`/`elseif`/`catch` on next line after `}`
- **PHP Version**: 7.3+ compatible

## Security Rules (must follow)

1. **Route permission is coarse.** `access CiviCRM` on a route does not decide which records a user may touch. Every record id taken from the request is checked against the current user in the handler, and "not found" and "not yours" return the same response.
2. **Shared data is filtered in the query.** For records shared on purpose (e.g. templates), the sharing condition is part of the lookup (`WHERE is_template = 1`), not a check after fetching by id.
3. **Return only the fields the client uses.** No `SELECT *` or full-row `json_encode()` in responses; log-like columns (`post_data`, `return_data`) leak private content.
4. **Compare tokens strictly and reject empty ones.** `CRM_Core_Key::validate()` returns NULL on failure, and `NULL == ''` is TRUE.
5. **JSON bodies are raw input.** `php://input` bypasses `CRM_Utils_Request` and PHPIDS — validate types yourself; escaping happens where the value is printed (Smarty has no auto-escaping, see neticrm-frontend).

Details and code: [php-patterns.md](references/php-patterns.md) — 8. Security, 9. Custom AJAX Endpoints.

## Development Workflow

1. **Identify the correct layer** — business logic → BAO, form handling → Form, external access → API
2. **Check existing patterns** — search for similar implementations before writing new code
3. **Review references** — consult `references/php-patterns.md` for detailed patterns
4. **Apply security checks** — permissions before data access, parameterized queries always
5. **Add translations** — all user-facing text must use `ts()`

## References

- **PHP Patterns**: See [php-patterns.md](references/php-patterns.md) — BAO/Form class structure, routing, permissions, translations, common utilities, testing, security, custom AJAX endpoints (per-record checks, tokens, response fields)
- **Hook System**: See [hook-system.md](references/hook-system.md) — form hooks, data hooks (pre/post), CRM_Utils_Hook methods, real module examples
- **Database Schema**: See [database-schema.md](references/database-schema.md) — XML schema structure, field types/attributes, naming conventions, index/FK patterns, path lookup; **includes GenCode workflow (ask developer for environment-specific command before running)**
- **PHP Coding Style**: See [php-coding-style.md](references/php-coding-style.md) — full PSR1/PSR2/PSR12 rules, brace position, constant case, array syntax, operator spacing, php-cs-fixer usage
- **API v3 Endpoints**: See [api-endpoints.md](references/api-endpoints.md) — file structure, function naming, CRUD helpers, spec functions, custom actions, return values
- **API v3 Calls**: See neticrm-api skill — entity actions, params, return values; PHP 呼叫方式見 [php-api.md](../neticrm-api/references/php-api.md)
