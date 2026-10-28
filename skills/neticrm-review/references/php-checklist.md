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
| Raw superglobals | Direct use of `$_GET`/`$_POST`/`$_REQUEST` — use `CRM_Utils_Request::retrieve()` with a type. Reading alone is not a vulnerability; when the value reaches SQL or HTML unsanitized, report it under the SQL/XSS rules instead | 🟡 Warning |
| SQL injection | User-controlled value concatenated into SQL (see `security-checklist.md`) — use `CRM_Core_DAO::executeQuery($sql, [params])` | 🔴 Critical |
| Missing permission | Page/Form/API entry point exposes data without a permission gate (see `security-checklist.md`) — not applicable to BAO methods | 🔴 Critical |
| Unescaped output | User data echoed without `htmlspecialchars()` (or `CRM_Utils_String::htmlPurifier()` when rich HTML is allowed) | 🔴 Critical |
| New without parens | `new Foo` — must always include parentheses: `new Foo()` | 🟡 Warning |
| PHP 7.4 compat | `CRM/`, `api/`, `templates/` are shared by the 7.x (PHP 7.4) and 10.x branches. Flag PHP 8-only features: `str_contains()`/`str_starts_with()`/`str_ends_with()`, `array_is_list()`, `match`, nullsafe `?->`, named arguments, constructor property promotion, union or `mixed` types, `throw` as an expression, trailing comma in parameter lists | 🔴 Critical |
