---
name: neticrm-review
description: "netiCRM code review workflow covering PHP, frontend (JS/CSS/Smarty), database migrations, Drupal integration, and security. Use at any stage — before or after merge — for self-check, pre-PR review, retrospective audit, or security review of merged code. Trigger with issue number, hash range, or no args. Outputs Change Overview + 🔴 Critical / 🟡 Warning / 🔵 Suggestion findings report."
---

# netiCRM Code Review

Review flow:

1. **Parse input** — determine diff range from arguments or ask
2. **Gather context** — synthesize change purpose; ask for AC/TC if not provided
3. **Load checklists** — read only the relevant reference files
4. **Review** — diff scan first, escalate to function/class context only on trigger
5. **Report** — change overview, AC/TC coverage, then findings grouped by severity
6. **Finalize** — output note that fixes require explicit instruction

---

## Review Principles

### Accuracy over accommodation

Report what is actually there — not what sounds reassuring.

- Flag an issue only when you can state concretely which checklist rule it violates or what risk it creates
- Severity must match actual impact:
  - 🔴 Critical = data loss / security hole / runtime failure
  - 🟡 Warning = real correctness or convention risk
  - 🔵 Suggestion = genuinely optional improvement with a clear benefit
- Do not add findings to make the report look thorough
- Do not soften a Critical to avoid seeming harsh; do not escalate a Suggestion to a Warning to appear cautious
- Do not add sycophantic commentary (e.g. "Overall this is a solid implementation")

### Change Overview is mandatory

A clean diff means no findings — it does not mean no analysis.

- Change Overview must always be produced with full depth, regardless of whether any issues are found
- Reviewers rely on it to understand the code without reading everything, cross-check conclusions, and learn from design decisions
- `✅ No issues found in this diff.` appears only inside the findings section — it never replaces or skips the Change Overview

### Good code deserves recognition

Silence on positive choices is a missed teaching opportunity.

- While reviewing, actively look for 1–2 well-executed patterns worth highlighting: good architectural decisions, defensive edge-case handling, clean refactors, or design trade-offs handled correctly
- These appear in the **✨ Notable Design Patterns** section of the report — not as praise, but as concrete examples of "what good looks like" in this codebase
- Each entry must explain *why* the pattern is good and *when* to apply it elsewhere — otherwise skip it
- Omit the entire section if the diff contains nothing architecturally notable

---

## Tool Use Guidelines

See `references/tool-guidelines.md` for detailed patterns and examples. Core rules:

- **Grep before Read** — locate line numbers with `grep -n` first; read with `offset/limit`, never the whole file
- **Layer 4 search** — `grep -rl` to list files first, then `grep -n` on matched files only
- **Parallel calls** — issue independent Bash commands in the same response turn
- **git diff scoping** — add path filter (`-- neticrm/ CRM/Contribute/`) when review is module-specific

---

## Step 1: Parse Input & Get the Diff

This project has two submodules that must be included in every review: `neticrm/` and `drupal/`. The `.claude/` submodule is excluded. Always treat all three repos (parent + two submodules) as a single review unit.

**Pattern A — Hash range (issue number optional)** (e.g. `#45339 abc1234 def5678` or `abc1234 def5678`)

```bash
git log --oneline <hash1>..<hash2>
```

Show the commits and ask for confirmation before diffing. If `git log` returns nothing, warn that the hash order may be reversed (older hash must come first).

If confirmed, get the parent diff and then expand submodule pointers (see **Submodule Expansion** below):
```bash
git diff <hash1>..<hash2>
```

**Pattern B — Issue number only** (e.g. `#45339`)

Search all three repos in parallel:

```bash
git log --all --oneline --grep="#45339"
cd neticrm && git log --all --oneline --grep="#45339"
cd drupal && git log --all --oneline --grep="#45339"
```

⛔ **STOP — do not run any diff commands yet.**

Output the results grouped by repo, listing every commit found (including submodule commits — they are first-class commits, not background noise):

```
Found N commits across repos:

Parent repo:
- abc1234  refs #45339, ...
- def5678  refs #45339, ...

neticrm submodule:
- 255cd80  refs #45339, ...

drupal submodule: (none)

Which range(s) to review?
1. All — use oldest..newest per repo
2. Specific range — provide start and end hash (per repo)
```

**Do not run any diff commands until the user replies and confirms the scope.**

Then diff each confirmed range and combine (apply **Submodule Expansion** to parent diff).

**Pattern C — No arguments**

```bash
git status --short
git log --oneline -10
cd neticrm && git log --oneline -10
cd drupal && git log --oneline -10
```

Then ask:

> Which range to review?
> 1. **Uncommitted changes** (`git diff HEAD` in each repo) — staged + unstaged
> 2. **Current branch vs develop** (`git diff origin/develop...HEAD`) — feature branch not yet merged
> 3. **Recently merged into this branch** — show merge commits to pick from
> 4. **Specific range or paste diff text**

For option 3, run:
```bash
git log --oneline --merges -10
```
Show merge commits and ask which one to review. Then diff using:
```bash
git diff <merge-commit>^1..<merge-commit>
```
Then apply **Submodule Expansion** to extract submodule diffs.

**Pattern D — User pastes diff text directly**: use it as-is.

Do not guess — if the input is ambiguous, always ask first.

---

### Submodule Expansion

After obtaining any parent repo diff, scan it for `Subproject commit` lines. Each occurrence means a submodule's code changed. Extract the before/after hashes and diff inside the submodule directory:

```
# In parent diff:
-Subproject commit <old_hash>
+Subproject commit <new_hash>
```

```bash
# For neticrm submodule
cd neticrm && git diff <old_hash>..<new_hash>

# For drupal submodule
cd drupal && git diff <old_hash>..<new_hash>
```

Add the resulting diffs to the review scope. If a submodule pointer changed but the submodule diff is empty (e.g. pointer-only bump with no real changes), skip it silently.

---

## Step 2: Gather Context

### Ask for AC/TC

If the user's input contains no Acceptance Criteria (AC) or Test Cases (TC), ask before proceeding:

> Do you have Acceptance Criteria (AC) or Test Cases (TC) for this change?
> They help evaluate whether the implementation is complete and correctly tested.
> (Reply "skip" to proceed without them.)

Record any AC/TC provided. They will be used in the Change Overview and report.

### Synthesize Change Overview

Read commit messages from Step 1 and the diff. For any BAO, core logic, or migration file, proactively read the surrounding function (follow Tool Use Guidelines for offset/limit) to understand design intent — not just to check for issues.

Produce a **Change Overview** with these five sections. Depth scales with complexity; omit a section only if genuinely not applicable:

- **Background** — why the change was needed; cite AC if provided
- **What Changed** — concrete changes grouped by module/file area, with technical purpose for each item
- **Affected Features / User Flows** — user-facing features, admin pages, or API behaviors impacted
- **Key Implementation Decisions** — layer choice (BAO vs Form vs API), edge case handling, migration strategy, trade-offs
- **Expected Outcome** — what behaves differently after the change; map to AC items if provided

---

## Step 3: Detect Scope & Load Checklists

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

## Step 4: Review

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

Use `grep -n` to locate the function, then `Read` with `offset/limit` (see Tool Use Guidelines).

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

## Step 5: Output Report

**Language**: Write the entire report in Traditional Chinese using Taiwan conventions (台灣用語繁體中文) by default — not Simplified Chinese, not Hong Kong usage. Use the user's specified language only if they explicitly request one. Code identifiers, file paths, and inline code remain in their original form regardless of language.

When issue number or hash range is known from Step 1, include it in the header. Otherwise omit it.

```
## Code Review Report
**Issue**: #45339                          ← omit if not provided
**Range**: `abc1234..def5678` (N commits)  ← omit if not a hash range
  - abc1234 refs #45339, feat: ...
  - def5678 refs #45339, chore: ...

---

### 📋 Change Overview

**Background**
[Why this change was needed — problem, bug, or requirement]

**What Changed**
- [Module / file area] [Concrete change and its purpose]
- [Module / file area] [Concrete change and its purpose]

**Affected Features / User Flows**
- [User-facing feature or flow impacted]

**Key Implementation Decisions**
- [Notable technical choice and reasoning]
- [Migration / idempotency strategy if applicable]

**Expected Outcome**
- [What behaves differently after this change]
- AC1: [description] ← include only if AC/TC was provided

---

### ✅ AC/TC Coverage          ← omit entire section if no AC/TC was provided
| # | AC / TC | Status |
|---|---------|--------|
| 1 | [description] | ✅ Covered / ⚠️ Partial / ❌ Not covered |

---

### ✨ Notable Design Patterns          ← omit entire section if nothing architecturally notable
- **`path/to/File.php` — Pattern name**: Why this design is good, what problem it solves, and in which similar scenarios it can be reused.

---

### 🔴 Critical (must fix)
- **[Layer — subcategory]** `path/to/File.php:42`
  Issue description.
  **Impact**: Who is affected, under what conditions this breaks, or why violating this rule is dangerous.

  ```php
  // Before
  problematic code snippet (extract from diff + lines or file read)
  ```
  ```php
  // After
  corrected code snippet
  ```

### 🟡 Warning (recommended fix)
- **[Layer — subcategory]** `path/to/file.tpl:18`
  Issue description.
  **Impact**: Who is affected, under what conditions this breaks, or why violating this rule is dangerous.

  ```html
  // Before
  problematic code snippet
  ```
  ```html
  // After
  corrected code snippet
  ```

### 🔵 Suggestion (optional improvement)
- **[Layer — subcategory]** `path/to/file.js:55`
  Issue description.
  **Impact**: The concrete maintainability, readability, or consistency benefit this improvement brings.
  → Suggested approach   ← use text-only when no single code fix applies
```

---
Summary: 🔴 Critical N  |  🟡 Warning N  |  🔵 Suggestion N

### 📚 Key Takeaways          ← omit if findings ≤ 1 or all findings are trivial formatting issues
1. **Principle name** (from 🟡 Warning N): One-sentence generalizable rule applicable to all instances of this problem type — not just this PR.
2. **Principle name** (from 🔵 Suggestion N): Same format.
```

Layer labels: `[PHP]`, `[CSS]`, `[JS]`, `[Smarty]`, `[Database]`, `[Drupal]`, `[Security]`

**Layer subcategory** (best-effort, append with ` — `):
- PHP: `SQL safety`, `architecture`, `readability`, `i18n`
- Smarty: `i18n`, `XSS`, `JS context`
- JS: `formatting`, `security`, `event binding`

**Before/After rules:**
- Include Before/After code blocks for every finding where the fix is a specific code change
- Extract **Before** from the diff `+` lines (Layer 1) or from the file read (Layer 2/3) — only the relevant lines, not the whole function
- Write **After** as the corrected version of those same lines
- Use `→ Suggested approach` text only when no concrete code fix applies (e.g., missing file, architectural redesign needed)

**Impact rules:**
- Every finding must include an `**Impact**` line between the description and Before/After
- State the practical consequence: who is affected, under what conditions, and why the rule exists
- For low-risk style findings (🔵), state the maintainability benefit rather than a risk scenario
- One to two sentences maximum — do not pad

**✨ Notable Design Patterns rules:**
- Each entry: `**\`path/file.php\` — Pattern name**`: why it's good, what problem it solves, where to reuse
- Maximum 3 entries per report — quality over quantity
- Not praise — explain the *mechanism* that makes it correct

**📚 Key Takeaways rules:**
- Distill generalizable principles from the findings — not a finding summary
- Each entry must cite which finding(s) it derives from
- Maximum 4 entries; prefer principles applicable across future PRs
- Omit entirely if findings count ≤ 1 or all findings are trivial formatting issues

If no issues are found in the findings section: output `✅ No issues found in this diff.`

---

## Step 6: After the Report

After outputting the report, add this note:

> Review complete. To apply fixes, explicitly specify which items to address.
>
> ⚠️ **This review is AI-generated and for reference only.** Human review remains required. The AI may miss: business logic correctness, performance under real load, conflicts with parallel in-flight changes, and whether the implementation truly meets the product intent.

### Knowledge gap prompt

If a suspected finding was ruled out after reading the implementation, or an undocumented project pattern was discovered, append one prompt after the disclaimer:

> 💡 **Reference update opportunity**: [one sentence — what was found, which `references/` file it belongs in]. Would you like me to add it?

Skip if no gaps were found. One prompt per session — consolidate multiple gaps into one.
