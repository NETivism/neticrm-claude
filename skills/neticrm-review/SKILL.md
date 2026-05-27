---
name: neticrm-review
description: "netiCRM project code review workflow covering PHP backend, frontend (JS/CSS/Smarty), database schema/migrations, Drupal integration, and security. Use when reviewing a git diff or PR before pushing, doing a self-check on your own changes, auditing a specific technical layer, performing a security-focused review, or when given a specific issue number with commit hash range (e.g. '#45339 abc1234 def5678'). Checks compliance with netiCRM conventions (CiviCRM class hierarchy, 2-space indent, Smarty translation rules, idempotent migrations, D7/D10 API differences). Output: 🔴 Critical / 🟡 Warning / 🔵 Suggestion layered report."
---

# netiCRM Code Review

Review flow:

1. **Detect scope** — analyze the diff to identify which layers are affected
2. **Load checklists** — read only the relevant reference files
3. **Review each layer** — check only `+` lines (additions); ignore `-` lines
4. **Report findings** — grouped by severity with file path, line, and fix suggestion
5. **Offer fixes** — after the report, ask if style-only issues should be auto-corrected

---

## Step 1: Parse Input & Get the Diff

### Input patterns (parse in order)

**Pattern A — Issue + hash range** (e.g. `#45339 abc1234 def5678`)

```bash
git log --oneline <hash1>..<hash2>
```

Display the found commits and ask for confirmation:

> 確認審查以下 N 個 commits（`<hash1>..<hash2>`）？
> abc1234 refs #45339, feat: ...
> def5678 refs #45339, chore: ...

If confirmed:
```bash
git diff <hash1>..<hash2>
```

If `git log` returns no commits, warn: "這個範圍沒有找到 commits，請確認 hash 順序是否正確（舊的在前、新的在後）。"

**Pattern B — Hash range only** (e.g. `abc1234 def5678`)

Same flow as Pattern A but without an issue number.

```bash
git log --oneline <hash1>..<hash2>
# Show commits → confirm → git diff <hash1>..<hash2>
```

**Pattern C — Issue number only** (e.g. `#45339`)

```bash
git log --all --oneline --grep="#45339"
```

Show found commits and ask:

> 找到以下 N 個 commits，要審查哪個範圍？
> 1. **全部** (`<oldest_hash>..<newest_hash>`)
> 2. **指定範圍** — 請提供起始和結束 hash

Then diff the confirmed range.

**Pattern D — No arguments**

Run these two commands first:
```bash
git status --short
git log --oneline origin/develop..HEAD 2>/dev/null || git log --oneline -10
```

Then ask:
> 要審查哪個範圍？
> 1. **未提交的變更** (`git diff HEAD`) — staged + unstaged
> 2. **整個 branch 相對於 develop** (`git diff origin/develop...HEAD`) — PR 送審前
> 3. **指定檔案或貼上 diff 文字**

**Pattern E — User pastes diff text directly**
Use it as-is.

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

For detailed rules beyond the checklists, reference:
- PHP details → `neticrm-backend` skill: `references/php-coding-style.md`, `references/php-patterns.md`
- Frontend details → `neticrm-frontend` skill: `references/css-standards.md`, `references/javascript-patterns.md`, `references/smarty-templates.md`

---

## Step 3: Review

Work through the diff file-by-file using three levels of context depth. Always start with Layer 1; escalate to deeper layers only when triggered.

### Layer 1 — Diff scan (always)

Inspect `+` lines against the loaded checklists. Sufficient for:
- Code style (indentation, `array()`, constant casing, semicolons)
- Missing `{ts}` / translation wrappers
- Missing `{literal}` or `escape='js'` in Smarty
- Obvious SQL string concatenation (e.g. `"WHERE id = " . $id`)
- Database / migration idempotency patterns

### Layer 2 — Full function context (on trigger)

When a `+` line matches any of these patterns, **read the complete surrounding function** (from its definition line to its closing `}`) before deciding whether to flag an issue:

| Trigger pattern | Why context is needed |
|----------------|-----------------------|
| Any DB query (`executeQuery`, `db_select`, `db_query`) | Permission check or parameterization may exist earlier in the same function |
| User input access (`$_GET`, `$_POST`, `CRM_Utils_Request`) | Input may already be validated/sanitized above |
| Data write operation (insert / update / delete) | Permission check may be in `preProcess()` or a guard clause above |
| `CRM_Core_Permission::check()` appears absent | May be enforced by parent class or route `<access_arguments>` |

```bash
# Read the full file, then locate the function boundaries
Read path/to/File.php
```

Do not flag a security issue until you have confirmed the full function context.

### Layer 3 — Class header context (on trigger)

When a `+` line suggests an architecture problem, **read from the top of the file to the first method definition**:

| Trigger pattern | Why context is needed |
|----------------|-----------------------|
| Business logic or DB query inside a `/Form/` file | May actually be a BAO helper method included in the Form |
| Direct SQL in `/api/v3/` | Need to confirm the class/function role |
| Suspicious `extends` or no clear layer identity | Determine DAO / BAO / Form / API responsibility before flagging |

### Layer 4 — Caller search (on trigger)

When a `+` or `-` line **changes a public function signature** (adds/removes/reorders parameters):

```bash
grep -r "functionName" /path/to/civicrm --include="*.php" -l
```

List the affected callers in the report as a 🔴 Critical if any exist outside the changed files.

---

If the diff is large (>300 changed lines), complete Layers 1–2 first, then note in the report that Layer 3–4 checks were done only on flagged items.

---

## Step 4: Output Report

Use this exact structure. The header section is conditional — include only the fields that are known from Step 1.

```
## Code Review Report
<!-- Include if issue number was provided: -->
**Issue**: #45339
<!-- Include if hash range was used: -->
**Range**: `abc1234..def5678` (N commits)
  - abc1234 refs #45339, feat: consolidate CKEditor dimensions
  - def5678 refs #45339, chore: disable TinyMCE option

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

## Step 5: Offer Fixes

After the report, ask:

> **自動修正？** 以上 🟡 Warning 中屬於 code style 的問題（縮排、`array()` → `[]`、常數大小寫等）可以自動套用修正。是否要執行？

Only offer auto-fix for mechanical style issues (indentation, array syntax, constant casing). Never auto-fix architecture, security, or logic issues — those require human judgement.
