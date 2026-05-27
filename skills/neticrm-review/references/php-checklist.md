# PHP Review Checklist

Applies to changes in `/CRM/` and `/api/v3/`. For full rules see `neticrm-backend` skill references.

## Code Style

| Check | What to look for | Severity |
|-------|-----------------|---------|
| Indentation | 2 spaces — no tabs | 🟡 Warning |
| Arrays | `[]` always — never `array()` | 🟡 Warning |
| Constants | `TRUE`, `FALSE`, `NULL` uppercase | 🟡 Warning |
| Equality | `===` and `!==` — no loose comparisons | 🟡 Warning |
| Visibility | All methods/properties have explicit `public`/`protected`/`private` | 🟡 Warning |
| Brace position | Opening `{` same line as declaration | 🟡 Warning |
| else/catch | Must be on next line after closing `}` | 🟡 Warning |
| Properties | Named `_camelCase` (underscore prefix) | 🔵 Suggestion |
| Type casts | Lowercase: `(int)`, `(bool)`, `(string)` — not `(Integer)` | 🟡 Warning |

## Architecture

| Check | What to look for | Severity |
|-------|-----------------|---------|
| DAO not edited | Files in `/CRM/**/DAO/` must not be manually modified | 🔴 Critical |
| BAO responsibility | BAO contains only business logic — no form/template logic | 🟡 Warning |
| Form lifecycle | Form classes use `preProcess()` → `buildForm()` → `postProcess()` order | 🟡 Warning |
| Translations | All user-facing strings wrapped in `ts()` | 🟡 Warning |
| Route definitions | Routes defined in `CRM/*/xml/Menu/*.xml`, not hardcoded | 🟡 Warning |

## Common Mistakes

| Check | What to look for | Severity |
|-------|-----------------|---------|
| Raw superglobals | Direct use of `$_GET`/`$_POST` — use `CRM_Utils_Request::retrieve()` | 🔴 Critical |
| SQL injection | String concatenation in SQL — must use `CRM_Core_DAO::executeQuery($sql, [params])` | 🔴 Critical |
| Missing permission | Data access without prior `CRM_Core_Permission::check('permission string')` | 🔴 Critical |
| Unescaped output | User data echoed without `CRM_Utils_String::escapeHtml()` | 🔴 Critical |
| New without parens | `new Foo` — must always include parentheses: `new Foo()` | 🟡 Warning |
| PHP 7.3 compat | Avoid `str_contains()`, `array_is_list()`, named arguments — requires 7.3+ compat | 🔴 Critical |
