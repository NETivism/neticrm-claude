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

### Code Style
- **Indentation**: 2 spaces
- **Class names**: CamelCase (`CRM_Contribute_BAO_Contribution`)
- **Methods**: camelCase (`processContribution()`)
- **Properties**: `_camelCase` (underscore prefix for Form/Page instances)
- **Comparisons**: `===` and `!==`
- **PHP Version**: 7.3+ compatible

## Development Workflow

1. **Identify the correct layer** — business logic → BAO, form handling → Form, external access → API
2. **Check existing patterns** — search for similar implementations before writing new code
3. **Review references** — consult `references/php-patterns.md` for detailed patterns
4. **Apply security checks** — permissions before data access, parameterized queries always
5. **Add translations** — all user-facing text must use `ts()`

## References

- **PHP Patterns**: See [php-patterns.md](references/php-patterns.md) — BAO/Form class structure, routing, permissions, translations, common utilities, testing, security
- **API v3 Patterns**: See [api-v3-patterns.md](references/api-v3-patterns.md) — file structure, CRUD helpers, spec functions, custom actions, return values, internal API calls
- **Hook System**: See [hook-system.md](references/hook-system.md) — form hooks, data hooks (pre/post), CRM_Utils_Hook methods, real module examples
- **Database Schema**: See [database-schema.md](references/database-schema.md) — XML schema structure, field types/attributes, naming conventions, index/FK patterns, path lookup
