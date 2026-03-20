---
name: playwright-testing
description: "netiCRM Playwright E2E testing standards. Use when writing, modifying, or running frontend integration tests in tests/playwright/. Covers test structure, CiviCRM UI patterns (date pickers, accordions, custom search forms), test data creation via the admin UI, and result verification."
---

# netiCRM Playwright E2E Testing

## Overview

End-to-end frontend testing for netiCRM using Playwright. Tests interact with the full browser UI (CiviCRM + Drupal) as a logged-in admin user.

**Key principle**: Tests must work without hardcoded environment details (base URL, Docker container names). All environment specifics are resolved via `setup.env` and the pre-authenticated `storageState.json`.

---

## When Unsure — Read Existing Tests First

Before writing a new test, browse `tests/playwright/tests/` and read the top section of relevant spec files (variable declarations, helper functions, and the setup test). Each file documents:
- Which CiviCRM pages it visits
- How it creates test data via the admin UI
- Which form selectors it relies on

Use existing files as templates. The patterns for inline contact creation, accordion handling, and date filtering are already proven there.

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
- After writing, register the new test in **both** `.github/workflows/ci.yml` and `.drone.yml` at the end of each Playwright block (see [Registering a New AI Test in CI](#registering-a-new-ai-test-in-ci) below)

---

## Running Tests

From **within** the test environment (the server running netiCRM):

```bash
cd tests/playwright
npx playwright test tests/<your-file>.spec.js
```

To run all tests:

```bash
npx playwright test
```

> How to access the server environment (Docker, SSH, local) depends on the developer's machine setup and is intentionally not specified here.

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

After placing a new spec file under `tests/specific/`, add it to **both** CI config files at the end of every Playwright block.

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

## Reference Docs

| Topic | File |
|-------|------|
| Utility functions (`utils.js`), date picker, readonly bypass | `references/utilities.md` |
| CiviCRM UI patterns (accordion, selectors, error checks, page title) | `references/civicrm-ui-patterns.md` |
| Creating test data via admin UI, sort name, today's date | `references/test-data.md` |
| Validation testing patterns, common mistakes | `references/validation-patterns.md` |
