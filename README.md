# netiCRM `.claude` — AI Development Configuration

This directory contains project-level configuration for [Claude Code](https://claude.ai/code), including netiCRM/CiviCRM-specific **Agents**, **Skills**, and **permission settings** that allow the AI to assist development in line with the project's architecture, conventions, and quality standards.

---

## Directory Structure

```
.claude/
├── CLAUDE.md                    # Core development guide (auto-loaded every session)
├── README.md                    # This file
├── settings.local.json          # Local Bash command allowlist (not version-controlled)
├── agents/                      # Specialized AI agent definitions
│   ├── php-engineer.md
│   ├── frontend-engineer.md
│   ├── drupal-module-developer.md
│   ├── database-agent.md
│   ├── structure-planner.md
│   └── translation-extractor.md
└── skills/                      # Callable skill definitions
    ├── neticrm-backend/
    ├── neticrm-frontend/
    ├── neticrm-api/
    ├── playwright-testing/
    ├── extract-i18n/
    └── neticrm-review/
```

---

## CLAUDE.md — Core Development Guide

`CLAUDE.md` is the primary guide auto-loaded by Claude Code at the start of every conversation. It covers:

| Topic | Summary |
|-------|---------|
| **Code style** | 2-space indent, strict equality (`===`), PHP PascalCase, JS single quotes + semicolons |
| **Directory structure** | `/CRM/`, `/api/v3/`, `/templates/`, `/xml/schema/`, `/neticrm/`, `/drupal/` |
| **Route definitions** | `CRM/*/xml/Menu/*.xml`: `<path>`, `<page_callback>`, `<access_arguments>` |
| **Permission system** | `CRM_Core_Permission::check()`, defined in `basicPermissions()` and `Info.php` |
| **i18n translation** | PHP `ts()`, Smarty `{ts}`, Drupal `t()` — syntax and placeholder formats |
| **Branch strategy** | `develop` (new features) → `master` (stable release) → `hotfix` (urgent fixes) |

---

## Agents — Specialized AI Agents

Agents are independent AI execution units with specific skills and scoped tool access, suited for tasks that require deep focus in a particular domain. The main Claude Code agent decides whether to invoke them based on the task at hand.

### `php-engineer` · Model: Opus

**Use when**: implementing BAO business logic, modifying Form handlers, building API v3 endpoints, writing cron jobs

**Scope**:
- `/CRM/` — BAO, DAO, Form core classes
- `/api/v3/` — API endpoints
- `/external/` — external integration modules

**Skills loaded**: `neticrm-backend`

---

### `frontend-engineer` · Model: Sonnet

**Use when**: editing `.tpl`/`.css`/`.js` files, building UI features, fixing CSS layout issues, integrating frontend assets

**Scope**:
- `/templates/CRM/` — Smarty templates
- `/js/` — JavaScript
- `/css/` — stylesheets
- `/CRM/Core/Smarty/plugins/` — custom Smarty plugins

**Skills loaded**: `neticrm-frontend`

---

### `drupal-module-developer` · Model: Sonnet

**Use when**: implementing Drupal hooks, building Drupal forms, syncing Drupal users with CiviCRM contacts, working on `/neticrm/` submodule

**Scope**: `/neticrm/`, `/drupal/` (submodule directories)

**Important**: Always confirm the current branch first (`7.x-*` = Drupal 7; `10.x-*` = Drupal 10) to use the correct API.

**Skills loaded**: `neticrm-backend`

---

### `database-agent` · Model: Sonnet

**Use when**: any database schema change is needed — full workflow: XML schema definition → GenCode → migration script

**Scope**:
- `/xml/schema/` — schema XML definitions
- `/CRM/**/DAO/` — auto-generated DAOs (never edit manually)
- `/neticrm/neticrm_update/update/` — migration scripts
- `/sql/*.mysql` — SQL files

**Standard workflow**:
1. Edit XML definition in `/xml/schema/`
2. Run `cd xml && php GenCode.php` to regenerate DAOs
3. Create migration script at `/neticrm/neticrm_update/update/neticrm_xNNN.inc`
4. Commit XML, DAO, and migration script together

**Skills loaded**: `neticrm-backend`

---

### `structure-planner` · Model: Opus

**Use when**: any change touching multiple PHP files, complex business logic modifications, external API integrations, or when the impact on downstream components is unclear — plan before implementing

**Methodology**: Discovery → Analysis (technical debt) → Planning (step-by-step) → Validation (testing strategy)

**Skills loaded**: `neticrm-backend`, `neticrm-frontend`

---

### `translation-extractor` · Model: Haiku

**Use when**: after adding any user-facing text — automatically extract translation strings, update `civicrm.pot`, and push to Transifex

**Trigger**: `extract translations for #NNNNN` or `/extract-i18n NNNNN`

**Skills loaded**: `neticrm-backend`, `neticrm-frontend`, `extract-i18n`

---

## Skills — Callable Knowledge Modules

Skills are knowledge modules with detailed reference documentation, loaded by agents or the main agent when handling specific tasks.

### `neticrm-backend` — PHP Backend Standards

Complete PHP development standards for CiviCRM's DAO/BAO/Form/API layered architecture.

**Trigger**: writing PHP in `/CRM/`, implementing BAO logic, building API v3 endpoints, configuring route XML, checking permissions

| Reference | Contents |
|-----------|---------|
| `references/php-patterns.md` | BAO/Form class structure, routes, permissions, `ts()`, utilities, testing, security |
| `references/php-coding-style.md` | Full PSR rules, brace placement, constant casing, array syntax, php-cs-fixer |
| `references/hook-system.md` | Form hooks, data hooks (pre/post), `CRM_Utils_Hook` methods, real module examples |
| `references/database-schema.md` | XML schema structure, field types/attributes, naming rules, index/FK patterns, GenCode flow |
| `references/api-endpoints.md` | Endpoint file structure, function naming, CRUD helpers, spec functions, custom actions |

---

### `neticrm-frontend` — Frontend Standards

netiCRM-specific frontend standards for HTML, CSS, JavaScript, and Smarty templates.

**Trigger**: editing `.tpl`/`.css`/`.js` files, fixing CSS layout, writing jQuery code, implementing Smarty logic, checking browser compatibility

| Reference | Contents |
|-----------|---------|
| `references/css-standards.md` | Selector scoping (`.crm-container`), CSS variables, responsive design (`ncg-*`) |
| `references/javascript-patterns.md` | `cj()` vs `$` conflict, event delegation, `.crmAPI()` call patterns |
| `references/smarty-templates.md` | `{ts}` translation, `{literal}` blocks, `{crmURL}`, safe escaping |
| `references/html-conventions.md` | Semantic HTML structure, form elements, data tables, ZMDI icon font |
| `references/browser-support-policy.md` | Browser compatibility policy (required reading before using new CSS features) |

**Important**: Always consult `references/browser-support-policy.md` before using any new CSS feature.

---

### `neticrm-api` — API v3 Documentation Standards

Documentation standards and reference for netiCRM REST API v3.

**Trigger**: writing or updating API docs, looking up entity actions, implementing API endpoints

| Reference | Contents |
|-----------|---------|
| `references/authentication.md` | API key setup, header format, REST permissions |
| `references/request-response.md` | Pagination, sorting, filtering, nested queries, curl examples |
| `references/entities.md` | Supported actions and required fields per entity |
| `references/php-api.md` | Internal PHP calls (`civicrm_api3`), spec functions, return value format |

---

### `playwright-testing` — E2E Testing Standards

Complete standards for writing netiCRM frontend integration tests with Playwright.

**Trigger**: writing, modifying, or running tests under `tests/playwright/`

**Key rules**:
- Test data should be created via the **Admin UI first**; use JS API only when the UI cannot create it (explain to user and get consent)
- AI-generated tests go in `tests/playwright/tests/specific/` and are excluded from CI by default
- **Read `references/test-index.md` before writing any new test**

| Reference | Contents |
|-----------|---------|
| `references/test-index.md` | All existing test files and descriptions (**required reading before writing**) |
| `references/utilities.md` | `utils.js` shared functions, date picker, read-only field bypass |
| `references/civicrm-ui-patterns.md` | Accordion, selector, error checking, page title patterns |
| `references/test-data.md` | Creating test data via Admin UI, sort name, today's date |
| `references/validation-patterns.md` | Validation test patterns, common errors |
| `references/civicrm-js-api.md` | `crmAPI`, AJAX, CSRF handling |

---

### `extract-i18n` — i18n String Extraction Workflow

**Trigger**: `/extract-i18n NNNNN` (issue number)

Complete 8-step workflow:
1. Collect changed files from issue-related commits
2. AI scans for `ts()`/`{ts}` patterns to extract strings
3. Sync Transifex remote state (`pull-translation.sh`, `sync-pot.sh`)
4. Confirm no uncommitted changes in `l10n/`
5. AI translates to Traditional Chinese (Taiwan); user confirms
6. Verify no duplicate strings
7. Append to `civicrm.pot` and `l10n/zh_TW/civicrm.po`; regenerate `.mo`
8. Show summary; prompt user to verify then push to Transifex

---

### `neticrm-review` — Code Review Workflow

**Trigger**: `/neticrm-review` (with optional arguments)

netiCRM-specific code review skill supporting all development stages, with structured severity reporting. Covers both the parent repo and the `neticrm/` and `drupal/` submodules.

**When to use**:
- **Pre-commit self-review**: checking your own code before pushing
- **Pre-PR review**: quality gate before merging a feature branch
- **Post-merge retrospective**: reviewing already-merged code (junior review, security audit, time-range audit)

**Input modes**:

| Input format | Example | Behavior |
|-------------|---------|---------|
| `#issue hash1 hash2` | `#45339 abc1234 def5678` | Shows commits, diffs specified hash range after confirmation |
| `#issue` | `#45339` | Searches all related commits across all repos; select range then diff |
| (no args) | `/neticrm-review` | Asks review mode: uncommitted changes / vs develop / recently merged branch / specific range |
| (paste diff) | paste diff text directly | Reviews pasted diff as-is |

**Review layers**:

- **Layer 1 (always)**: scan all `+` lines against checklists for style and obvious issues
- **Layer 2 (triggered)**: DB query, user input, data write → read full function context
- **Layer 3 (triggered)**: architecture concerns (business logic in Form, direct SQL in API) → read class header
- **Layer 4 (triggered)**: public function signature changed → search all callers

**Report format**:

Every report always includes the following sections — **Change Overview is produced regardless of whether issues are found**:

```
### 📋 Change Overview        ← always present; analyzes change context and design decisions
### ✅ AC/TC Coverage         ← only when user provides AC/TC
### 🔴 Critical (must fix)
### 🟡 Warning (recommended fix)
### 🔵 Suggestion (optional improvement)
```

**Review Principles**:

- Only flag an issue when you can state concretely which rule it violates or what risk it creates
- Severity matches actual impact — never downgrade to soften tone, never upgrade to appear cautious
- No sycophantic commentary; no padding with low-value findings
- A clean diff means empty findings — not skipping the Change Overview
- Report always ends with: **AI review is for reference only; human review is still required**

**Important**: This skill outputs a report only — it **never auto-applies fixes**. To fix issues, explicitly instruct the AI which items to address.

| Reference | Layer | Contents |
|-----------|-------|---------|
| `references/php-checklist.md` | PHP | Style, architecture layers, common security mistakes |
| `references/frontend-checklist.md` | CSS / JS / Smarty | Selector scoping, `cj()` rules, `{ts}` translation |
| `references/database-checklist.md` | Database | Schema/DAO rules, migration idempotency guards |
| `references/drupal-checklist.md` | Drupal | D7/D10 API differences, CiviCRM initialization rules |
| `references/security-checklist.md` | **All layers (always loaded)** | SQL injection, XSS, permissions, dangerous GET operations |
| `references/tool-guidelines.md` | — | Efficient tool use: Grep before Read, offset/limit, parallel calls |

---

## settings.local.json — Local Permission Settings

This file configures the Bash command allowlist for Claude Code on your local machine — commands that don't require confirmation on every use. **It is added to `.gitignore` and not version-controlled**, since each developer's local environment paths differ.

Common authorized operation types:
- `grep`, `mysql`, `git`, `php` related commands
- Docker operations (`docker exec`, `docker compose`)
- Translation workflow scripts (`tx push`, `msgfmt`, `sync-pot.sh`)
- Specific WebFetch domains (Drupal, GitHub, CKEditor docs, etc.)

To add new permissions, use the `/update-config` skill or edit `settings.local.json` directly.

---

## How to Add or Modify Configuration

### Add an Agent

Create `<agent-name>.md` in `agents/` with frontmatter:

```markdown
---
name: my-agent
description: "Trigger conditions and use cases (used by Claude to decide when to invoke)"
tools: Read, Write, Edit, Bash, Grep, Glob
model: sonnet   # opus / sonnet / haiku
skills:
  - neticrm-backend
---

# Agent description
...
```

### Add a Skill

Create `SKILL.md` as the entry point in `skills/<skill-name>/`, then place detailed reference documents in `references/`.

### Add Local Permissions

```bash
/update-config
```

Or edit the `permissions.allow` array in `settings.local.json` directly.
