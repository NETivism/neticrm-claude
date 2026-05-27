---
name: neticrm-review
description: "netiCRM project code review workflow covering PHP backend, frontend (JS/CSS/Smarty), database schema/migrations, Drupal integration, and security. Use when reviewing a git diff or PR before pushing, doing a self-check on your own changes, auditing a specific technical layer, performing a security-focused review, or when given a specific issue number with commit hash range (e.g. '#45339 abc1234 def5678'). Checks compliance with netiCRM conventions (CiviCRM class hierarchy, 2-space indent, Smarty translation rules, idempotent migrations, D7/D10 API differences). Output: 🔴 Critical / 🟡 Warning / 🔵 Suggestion layered report."
---

# netiCRM Code Review

Review flow:

1. **Parse input** — determine diff range from arguments or ask
2. **Load checklists** — read only the relevant reference files
3. **Review** — diff scan first, escalate to function/class context only on trigger
4. **Report** — grouped by severity with file path, line, and fix suggestion
5. **Offer fixes** — ask if style-only issues should be auto-corrected

---

## Step 1: Parse Input & Get the Diff

**Pattern A — Hash range (issue number optional)** (e.g. `#45339 abc1234 def5678` or `abc1234 def5678`)

```bash
git log --oneline <hash1>..<hash2>
```

Show the commits and ask for confirmation before diffing. If `git log` returns nothing, warn that the hash order may be reversed (older hash must come first).

If confirmed:
```bash
git diff <hash1>..<hash2>
```

**Pattern B — Issue number only** (e.g. `#45339`)

```bash
git log --all --oneline --grep="#45339"
```

Show found commits and ask:

> 找到以下 N 個 commits，要審查哪個範圍？
> 1. **全部** (`<oldest>..<newest>`)
> 2. **指定範圍** — 請提供起始和結束 hash

Then diff the confirmed range.

**Pattern C — No arguments**

```bash
git status --short
git log --oneline origin/develop..HEAD 2>/dev/null || git log --oneline -10
```

Then ask:

> 要審查哪個範圍？
> 1. **未提交的變更** (`git diff HEAD`) — staged + unstaged
> 2. **整個 branch 相對於 develop** (`git diff origin/develop...HEAD`) — PR 送審前
> 3. **指定檔案或貼上 diff 文字**

**Pattern D — User pastes diff text directly**: use it as-is.

Do not guess — if the input is ambiguous, always ask first.

---

## Step 2: Detect Scope & Load Checklists

Inspect changed file paths to decide which checklists to load:

| Changed paths | Load this reference |
|---------------|---------------------|
| `/CRM/**/*.php`, `/api/v3/**` | `references/php-checklist.md` |
| `/templates/**/*.tpl`, `/js/**`, `/css/**` | `references/frontend-checklist.md` |
| `/xml/schema/**`, `/CRM/**/DAO/**`, `/neticrm/neticrm_update/**`, `*.mysql` | `references/database-checklist.md` |
| `/neticrm/**`, `/drupal/**` | `references/drupal-checklist.md` — also run `git branch --show-current` first |
| **Always** (every diff) | `references/security-checklist.md` |

If the user asks for `--php-only`, `--frontend-only`, `--security`, or `--db-only`, restrict to that layer plus security.

For detailed rules beyond the checklists:
- PHP → `neticrm-backend` skill: `references/php-coding-style.md`, `references/php-patterns.md`
- Frontend → `neticrm-frontend` skill: `references/css-standards.md`, `references/javascript-patterns.md`, `references/smarty-templates.md`

---

## Step 3: Review

Work through the diff file-by-file. Always start with Layer 1; escalate only when triggered.

### Layer 1 — Diff scan (always)

Inspect `+` lines against the loaded checklists. This layer is sufficient for:
- Code style (indentation, `array()`, constant casing, semicolons)
- Missing `{ts}` / translation wrappers
- Missing `{literal}` or `escape='js'` in Smarty
- Obvious SQL string concatenation (e.g. `"WHERE id = " . $id`)
- Database / migration idempotency patterns

### Layer 2 — Full function context (on trigger)

When a `+` line matches any of these patterns, read the complete surrounding function before deciding whether to flag an issue:

- Any DB query (`executeQuery`, `db_select`, `db_query`)
- User input access (`$_GET`, `$_POST`, `CRM_Utils_Request`)
- Data write operation (insert / update / delete)
- `CRM_Core_Permission::check()` appears absent

```bash
Read path/to/File.php
```

**Do not flag a security issue until you have confirmed the full function context.** The permission check or parameterization may exist earlier in the same function.

### Layer 3 — Class header context (on trigger)

When a `+` line suggests an architecture problem, read from the top of the file to the first method definition:

- Business logic or DB query inside a `/Form/` file
- Direct SQL in `/api/v3/`
- `extends` relationship looks wrong or class layer is unclear

### Layer 4 — Caller search (on trigger)

When a public function signature changes (parameters added / removed / reordered):

```bash
grep -r "functionName" /path/to/civicrm --include="*.php" -l
```

Flag affected callers outside the changed files as 🔴 Critical.

---

If the diff is large (>300 changed lines), complete Layers 1–2 first, then note in the report that Layer 3–4 checks were applied only to flagged items.

---

## Step 4: Output Report

When issue number or hash range is known from Step 1, include it in the header. Otherwise omit it.

```
## Code Review Report
**Issue**: #45339                          ← omit if not provided
**Range**: `abc1234..def5678` (N commits)  ← omit if not a hash range
  - abc1234 refs #45339, feat: ...
  - def5678 refs #45339, chore: ...

### 🔴 Critical（必須修正後才能 merge）
- **[Layer]** `path/to/File.php:42`
  Issue description.
  → Suggested fix

### 🟡 Warning（建議修正）
- **[Layer]** `path/to/file.tpl:18`
  Issue description.
  → Suggested fix

### 🔵 Suggestion（可選改善）
- **[Layer]** `path/to/file.js:55`
  Issue description.
  → Suggested fix

---
Summary: 🔴 Critical N  |  🟡 Warning N  |  🔵 Suggestion N
```

Layer labels: `[PHP]`, `[CSS]`, `[JS]`, `[Smarty]`, `[Database]`, `[Drupal]`, `[Security]`

If no issues are found: output `✅ No issues found in this diff.`

---

## Step 5: After the Report

After outputting the report, add this note:

> 以上為審查結果。如需修正，請明確告知要處理哪些項目，AI 才會著手修改。
