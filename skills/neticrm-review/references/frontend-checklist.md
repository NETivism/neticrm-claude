# Frontend Review Checklist

Applies to changes in `/templates/`, `/js/`, `/css/`. For full rules see `neticrm-frontend` skill references.

## CSS

| Check | What to look for | Severity |
|-------|-----------------|---------|
| Selector scoping | All CiviCRM-specific selectors prefixed with `.crm-container` | 🔴 Critical |
| CSS variables | Colors use `--color-*` or `--rfm-*` variables — no hardcoded hex/rgb | 🟡 Warning |
| Responsive design | Uses mobile-first `min-width` media queries, not `max-width` | 🟡 Warning |
| Grid system | Uses `ncg-row` / `ncg-col-*` classes — not custom flex/grid | 🟡 Warning |
| Browser compat | New CSS features verified against browser support policy | 🟡 Warning |

## JavaScript

| Check | What to look for | Severity |
|-------|-----------------|---------|
| jQuery alias | `$` used at top level — must use `cj()` or pass `$` via closure | 🔴 Critical |
| Closure wrapping | Code wrapped in `(function($) { 'use strict'; ... })(cj)` | 🟡 Warning |
| Event delegation | Binding directly to dynamic elements — must use `cj(document).on(event, selector, fn)` | 🟡 Warning |
| Strict equality | `==` or `!=` used — must be `===` / `!==` | 🟡 Warning |
| Semicolons | Missing semicolons at end of statements | 🟡 Warning |
| Single quotes | Double quotes in JS strings — must be single quotes | 🔵 Suggestion |

## Smarty Templates

| Check | What to look for | Severity |
|-------|-----------------|---------|
| Missing `{ts}` | User-facing text without translation wrapper | 🟡 Warning |
| JS translation | `{ts}` inside `<script>` without `escape='js'` | 🔴 Critical |
| Unescaped output | `{$var}` for user-supplied data — must be `{$var\|escape}` | 🔴 Critical |
| Hardcoded URL | URL strings instead of `{crmURL p='...' q='...'}` | 🟡 Warning |
| Bare JS braces | `{` / `}` in `<script>` without `{literal}..{/literal}` wrapper | 🔴 Critical |
| Parameter format | `{ts}Hello $name{/ts}` — must be `{ts 1=$name}Hello %1{/ts}` | 🟡 Warning |

### Translation-safe Smarty helpers (do NOT flag as Missing `{ts}`)

The following helpers call `ts()` internally in PHP. Passing a plain string literal is **correct**;
wrapping it with `{ts}` would cause double-translation. Flagging these as "Missing `{ts}`" is a
**false positive** — do not report it:

| Helper | Auto-translated params | PHP implementation |
|--------|----------------------|--------------------|
| `{docURL text="..." title="..."}` | `text`, `title` | `CRM_Utils_System::docURL()` — calls `ts($params['text'])` on output |

**Correct usage (no change needed):**
```smarty
{docURL page="CiviContribute Payment Processor Configuration" text="View Online Manual"}
```
