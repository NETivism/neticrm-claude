---
name: neticrm-review
description: "netiCRM project code review workflow covering PHP backend, frontend (JS/CSS/Smarty), database schema/migrations, Drupal integration, and security. Use when reviewing a git diff or PR before pushing, doing a self-check on your own changes, auditing a specific technical layer, or performing a security-focused review. Checks compliance with netiCRM conventions (CiviCRM class hierarchy, 2-space indent, Smarty translation rules, idempotent migrations, D7/D10 API differences). Output: 🔴 Critical / 🟡 Warning / 🔵 Suggestion layered report."
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
# Verify commits exist and show what will be reviewed
git log --oneline <hash1>..<hash2>
# Then diff
git diff <hash1>..<hash2>
```
Include the issue number and commit list as a header in the report.

**Pattern B — Hash range only** (e.g. `abc1234 def5678`)
```bash
git diff <hash1>..<hash2>
```

**Pattern C — Issue number only** (e.g. `#45339`)
```bash
# Find related commits
git log --all --oneline --grep="#45339"
```
Show the found commits and ask the user to confirm the range before diffing.

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

Work through the diff file-by-file:

- Only inspect `+` lines (new code being added)
- Match each line against the relevant checklist items
- Record: file path + approximate line number + issue description + suggested fix

If the diff is large (>300 changed lines), prioritize 🔴 Critical items and mention that a partial review was done.

---

## Step 4: Output Report

Use this exact structure:

```
## Code Review Report

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
