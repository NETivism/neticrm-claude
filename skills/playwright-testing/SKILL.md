---
name: playwright-testing
description: "netiCRM Playwright E2E testing standards. Use when writing, modifying, or running frontend integration tests in tests/playwright/. Covers test structure, CiviCRM UI patterns (date pickers, accordions, custom search forms), test data creation via the admin UI, and result verification."
---

# netiCRM Playwright E2E Testing

## Overview

End-to-end frontend testing for netiCRM using Playwright. Tests interact with the full browser UI (CiviCRM + Drupal) as a logged-in admin user.

**Key principles**:
- Tests must work without hardcoded environment details (base URL, Docker container names). All environment specifics are resolved via `setup.env` and the pre-authenticated `storageState.json`.
- **Prioritize using frontend UI** to create data and set up test scenarios. The JS API (`crmAPI`) should only be used as a last resort if UI-based creation is impossible. You MUST explain such cases to the user and obtain their approval before using the JS API.

---

## REQUIRED: Read Existing Tests Before Writing

**Before writing any new test, you MUST follow these steps — no exceptions:**

1. **Read `references/test-index.md`** to find the most relevant existing test(s) for the feature being tested.
   - *Example*: If you need to create a contribution page, follow the patterns in `add_contribution_page.spec.js` (listed in the index).
2. **Read the full content of the matched spec file(s)** — not just the first few lines. Pay attention to:
   - Variable declarations and shared state
   - How test data is created via the admin UI
   - Which selectors and helper functions are used
   - The `beforeAll` / `afterAll` structure
3. **Use the existing file as a template** — copy its structure, adapt its patterns. Do not invent new patterns if a proven one already exists.
4. **Consult the user** if:
   - You believe the JS API is necessary for setup.
   - The patterns in existing tests (like `add_contribution_page.spec.js`) are insufficient for your specific test case.

This step is mandatory. Skipping it produces tests that diverge from project conventions and are harder to maintain.

---

## Project Layout

```
tests/playwright/
├── playwright.config.js      # Playwright configuration (reads from setup.env)
├── global-setup.js           # Runs once to authenticate and save storageState.json
├── setup.env                 # Local environment config (gitignored) — NOT checked in
├── setup.example.env         # Template for setup.env
├── storageState.json         # Saved browser auth session — DO NOT commit
└── tests/
    ├── utils.js              # Shared utility functions (selectDate, fillInput, etc.)
    ├── *.spec.js             # Hand-written test files
    └── specific/             # AI-generated test files (see below)
        └── *.spec.js
```

All spec files go in `tests/playwright/tests/`. The `testDir` in `playwright.config.js` points to `./tests`.

### AI-generated tests → `tests/specific/`

Tests written by AI (Claude) must be placed in `tests/playwright/tests/specific/`. This makes it easy to distinguish AI-authored tests from hand-written ones and review them separately.

Rules for files in `specific/`:
- Same structure and conventions as regular spec files (see [Test File Structure](#test-file-structure) below)
- Import `utils.js` one level up: `require('../utils.js')`
- **Do NOT register AI tests in CI by default** — only add them to `.github/workflows/ci.yml` and `.drone.yml` if the user explicitly requests it (see [Registering a New AI Test in CI](#registering-a-new-ai-test-in-ci) below)

---

## Running Tests

First, determine whether netiCRM is running directly on the host or inside a Docker container.

**Detecting the environment:**
- If the developer's OS is **macOS or Windows**, netiCRM almost certainly runs inside a Docker container (Linux containers can't run natively on these OSes).
- On **Linux**, it may be either native or Docker — check with `docker ps` to see if a netiCRM container is running.
- You can also check for a `docker-compose.yml` or `.env` file at the project root for container names.

**If running inside Docker**, prefix commands with `docker exec <container-name> bash -c "..."`:

```bash
# Find the container name first
docker ps

# Then run the test inside the container
docker exec <container-name> bash -c "cd /path/to/civicrm/tests/playwright && npx playwright test tests/<your-file>.spec.js"
```

**If running natively on the host**:

```bash
cd tests/playwright
npx playwright test tests/<your-file>.spec.js
```

To run all tests:

```bash
npx playwright test
```

---

## Test File Structure

```javascript
const { test, expect, chromium } = require('@playwright/test');
const utils = require('./utils.js');

let page;

test.beforeAll(async () => {
  const browser = await chromium.launch();
  page = await browser.newPage();
});

test.afterAll(async () => {
  await page.close();
});

test.describe.serial('Feature Name', () => {
  test.use({ storageState: 'storageState.json' });

  test('TC-01: Description', async () => {
    await test.step('Step description', async () => {
      // ...
    });
  });
});
```

Rules:
- Use `test.describe.serial` — tests run in order and share state via outer variables
- Always use `storageState: 'storageState.json'` to reuse the admin session
- Use `test.step()` for sub-steps within a test (improves trace readability)
- `beforeAll`/`afterAll` are **outside** the describe block

---

## Registering a New AI Test in CI

> **Default: do NOT add AI-generated tests to CI.** Only register a test in CI config files when the user explicitly asks for it.

When the user requests CI registration, add the spec file to **both** CI config files at the end of every Playwright block.

### `.github/workflows/ci.yml`

Three jobs exist: `test7`, `test8`, `test8-d10`. Each job has a Playwright block that ends just before the `upload-artifact` step. Append to all three.

For `test7` and `test8` (Drupal 7, path `$DRUPAL_ROOT/sites/all/modules/civicrm`):
```yaml
      - name: Frontend - <Description> - Playwright
        run: docker exec neticrm-ci bash -c "cd \$DRUPAL_ROOT/sites/all/modules/civicrm/tests/playwright/ && npx playwright test tests/specific/<your-file>.spec.js"
```

For `test8-d10` (Drupal 10, path `$DRUPAL_ROOT/modules/civicrm`):
```yaml
      - name: Frontend - <Description> - Playwright
        run: docker exec neticrm-ci bash -c "cd \$DRUPAL_ROOT/modules/civicrm/tests/playwright/ && npx playwright test tests/specific/<your-file>.spec.js"
```

### `.drone.yml`

Three pipelines: `php7`, `php8`, `php83-d10`. Each pipeline's commands list ends before the `notify` step. Append to all three.

For `php7` and `php8` (Drupal 7, path `$DRUPAL_ROOT/sites/all/modules/civicrm`):
```yaml
    - cd $DRUPAL_ROOT/sites/all/modules/civicrm/tests/playwright/ && npx playwright test tests/specific/<your-file>.spec.js
```

For `php83-d10` (Drupal 10, path `$DRUPAL_ROOT/modules/civicrm`):
```yaml
    - cd $DRUPAL_ROOT/modules/civicrm/tests/playwright/ && npx playwright test tests/specific/<your-file>.spec.js
```

---

## Keeping test-index.md Up to Date

`references/test-index.md` only lists tests that are **committed and actually running in CI**. AI-generated tests in `tests/specific/` are excluded until they are explicitly registered in CI.

Update the index whenever:
- A spec file already listed in the index has its first-line comment (`// ...`) updated — sync the description in the index to match
- A test in `tests/specific/` is officially registered in both CI config files (`.github/workflows/ci.yml` and `.drone.yml`) and committed — add it to the appropriate category in the index

---

## Reference Docs

| Topic | File |
|-------|------|
| **All existing test files with descriptions (read this first)** | `references/test-index.md` |
| **CiviCRM/netiCRM Javascript API (crmAPI, AJAX, CSRF)** | `references/civicrm-js-api.md` |
| Utility functions (`utils.js`), date picker, readonly bypass | `references/utilities.md` |
| CiviCRM UI patterns (accordion, selectors, error checks, page title) | `references/civicrm-ui-patterns.md` |
| Creating test data via admin UI, sort name, today's date | `references/test-data.md` |
| Validation testing patterns, common mistakes | `references/validation-patterns.md` |
