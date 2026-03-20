---
name: validation-patterns
description: Patterns for testing server-side form validation — invalid date format, date order errors, and common mistakes
type: reference
---

# Validation Testing Patterns

---

## Common Mistakes

### Using a fixed past date for "hit" tests
Tests fail when the fixed date is too far in the past and no data matches. Always derive the "hit" range from `new Date()` for time-sensitive searches (see `references/test-data.md`).

### Forgetting the accordion state
After a search returns results, the accordion closes. Reopen it before the next search by calling the `openSearchPage()` helper or checking `crm-accordion-closed` class.

### `selectDate` month indexing confusion
`utils.selectDate(page, locator, year, 3, 20)` selects **March** 20. The function internally subtracts 1 for the 0-based jQuery UI month widget. Pass human month numbers (1–12) — do **not** subtract 1 yourself.

### Using `page.fill()` on a readonly date input
Date inputs are `readonly="1"`. Use `page.evaluate()` to remove the attribute first, or use `utils.selectDate()` for valid dates.

### Relying on `.crm-error` count for validation assertions
After a validation error, `.crm-error` may appear inside table rows (one per field) so the count can be >1. Use `page.locator('body').innerText()` + string matching for reliable validation checks.

### Using `CRM_Utils_Rule::date()` for CiviCRM date format validation (PHP)
`CRM_Utils_Rule::date()` only accepts ISO `YYYY-MM-DD` format, but CiviCRM date pickers typically submit values in the configured display format (e.g., `mm/dd/yyyy`). Use `strtotime($value) === false` in `formRule()` instead.

### Assuming `CRM_Utils_Date::processDate()` returns falsy for invalid input (PHP)
`processDate('invalid-date-xyz')` returns `'19700101000000'` (Unix epoch) — not an empty string. Always check `strtotime($raw_value) === false` before calling `processDate()`.


## Invalid Date Format → Server-Side Error

Date picker inputs have `readonly="1"` set by jQuery UI to prevent manual typing. Use `page.evaluate()` to inject an invalid value for server-side validation testing:

```javascript
await page.evaluate(() => {
  document.getElementById('my_date_field').removeAttribute('readonly');
  document.getElementById('my_date_field').value = 'invalid-date-xyz';
});
await page.locator('#_qf_Custom_refresh-top').click();
await utils.wait(2000);
const pageText = await page.locator('body').innerText();
expect(pageText).toMatch(/valid date|errors in the form/);
```

> Do **not** use `page.fill()` on a date input — Playwright waits for the element to become editable and times out.

---

## Start Date Later Than End Date → Server-Side Error

Use `utils.selectDate()` to set reversed dates, then assert the error:

```javascript
await utils.selectDate(page, page.locator('#date_from'), 2025, 2, 28); // later date
await utils.selectDate(page, page.locator('#date_to'),   2025, 2, 1);  // earlier date
await page.locator('#_qf_Custom_refresh-top').click();
await utils.wait(2000);
const pageText = await page.locator('body').innerText();
expect(pageText).toMatch(/must be earlier|errors in the form/);
```

---

## Reading Validation Errors (Body Text Approach)

After a validation failure, `.crm-error` elements may appear once per invalid field, making count-based assertions unreliable. Read the full page body instead:

```javascript
const pageText = await page.locator('body').innerText();
const hasErrorText = pageText.includes('valid date') || pageText.includes('errors in the form');
expect(hasErrorText).toBeTruthy();
```

---
