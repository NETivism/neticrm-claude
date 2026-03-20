# Utility Functions Reference (`utils.js`)

All helpers are exported from `tests/playwright/tests/utils.js`. Always `require('./utils.js')` and prefer these over raw Playwright calls — they include built-in assertions and logging.

## Function Summary

| Function | Signature | Purpose |
|----------|-----------|---------|
| `findElement` | `(page, selector)` | Waits for element to exist in DOM; logs the selector |
| `fillInput` | `(locator, text)` | Clicks, fills, then asserts the value matches |
| `selectOption` | `(locator, option)` | Selects a `<select>` option by value string, `{index}`, or `{value}` |
| `clickElement` | `(page, locator, expectEl?)` | Clicks element; optionally asserts `{exist}`, `{notExist}`, or `{visible}` |
| `checkInput` | `(page, locator, expectEl?)` | Clicks a checkbox; optionally asserts a selector becomes visible |
| `selectDate` | `(page, locator, year, month, day)` | Drives jQuery UI Datepicker (see below) |
| `makeid` | `(length)` | Returns a random alphanumeric string — use for unique test data names |
| `wait` | `(ms)` | `setTimeout` wrapper — use sparingly; prefer Playwright `waitFor` |
| `reLogin` | `(page, user?, password?)` | Re-authenticates admin and overwrites `storageState.json` |
| `logoutUser` | `(page)` | Logs out the current user (handles D10 confirm dialog) |

## `selectOption` Details

Accepts three forms for the `option` argument:

```javascript
// By value (most common)
await utils.selectOption(page.locator('#status'), '4');

// By zero-based index (last item: -1)
await utils.selectOption(page.locator('#status'), { index: -1 });

// By explicit value object
await utils.selectOption(page.locator('#status'), { value: '4' });
```

## `clickElement` with Post-Click Assertions

```javascript
// Assert an element appears after click
await utils.clickElement(page, page.locator('#save'), { visible: '#success-message' });

// Assert an element disappears after click
await utils.clickElement(page, page.locator('#submit'), { notExist: '.crm-error' });

// Assert an element exists (non-zero count) after click
await utils.clickElement(page, page.locator('#open'), { exist: '#modal' });
```

---

## Date Picker (`selectDate`)

CiviCRM uses **jQuery UI Datepicker**. The `selectDate` function:

1. Clicks the input to open the calendar widget
2. Selects the year via `select.ui-datepicker-year`
3. Selects the month via `select.ui-datepicker-month` (the jQuery UI widget is **0-indexed**; `selectDate` subtracts 1 internally)
4. Clicks the day cell `a.ui-state-default[data-date='${day}']`
5. Asserts the visible input value matches the field's `format` attribute

**Month parameter is 1-indexed** (pass human month numbers 1–12):

```javascript
// March 20, 2026 → pass month=3
await utils.selectDate(page, page.locator('#failed_date_from'), 2026, 3, 20);

// January 1, 2024 → pass month=1
await utils.selectDate(page, page.locator('#date_from'), 2024, 1, 1);
```

### Common mistake: month off by one
`utils.selectDate(page, locator, 2026, 3, 20)` selects **March** 20 — not February. The function handles the 0-based jQuery UI offset internally. Do **not** subtract 1 yourself.

---

## Bypassing Readonly Date Inputs

Date picker inputs have `readonly="1"` set by the jQuery UI widget to prevent manual typing. To inject an arbitrary value (e.g., to test server-side format validation), use `page.evaluate()` to remove the attribute first:

```javascript
await page.evaluate(() => {
  document.getElementById('my_date_field').removeAttribute('readonly');
  document.getElementById('my_date_field').value = 'invalid-date-xyz';
});
// Submit the form, then assert the error appears
await page.locator('#_qf_Custom_refresh-top').click();
await utils.wait(2000);
const pageText = await page.locator('body').innerText();
expect(pageText).toMatch(/valid date|errors in the form/);
```

This pattern is only needed when testing **invalid** input. For valid dates, always use `utils.selectDate()`.
