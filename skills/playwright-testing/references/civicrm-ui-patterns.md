# CiviCRM UI Interaction Patterns

Patterns specific to navigating and asserting CiviCRM pages within the netiCRM Drupal installation.

---

## Page Navigation

Always use **relative paths** — the base URL is set in `setup.env` and injected by Playwright config:

```javascript
await page.goto('civicrm/contribute/booster?reset=1');
await page.goto('civicrm/contact/add?reset=1&ct=Individual');
await page.goto('civicrm/contact/search/custom?force=1&reset=1&csid=20');
```

---

## Accordion Search Forms

CiviCRM custom search forms wrap criteria in a collapsible accordion. After a search runs, the accordion **auto-closes**. Reopen it before setting new criteria:

```javascript
const accordion = page.locator(
  '.crm-accordion-wrapper.crm-custom_search_form-accordion.crm-accordion-processed'
);
const count = await accordion.count();
if (count > 0) {
  const classes = await accordion.getAttribute('class');
  if (classes.includes('crm-accordion-closed')) {
    await utils.clickElement(page, page.locator('.crm-accordion-header'));
  }
}
```

Wrap this in a reusable `openSearchPage()` helper at the top of each spec that uses a custom search.

---

## Asserting No Errors

After **every** form submission, assert that no CiviCRM error elements are present:

```javascript
await expect(page.locator('.crm-error')).toHaveCount(0);
```

> Do **not** use `.crm-error` count to detect _validation_ errors — after a failed submission the count may be >1 (one element per invalid field). Use `page.locator('body').innerText()` + string matching for validation checks instead.

---

## Custom Search Form Selectors

| Element | Selector |
|---------|----------|
| Search submit (top button) | `#_qf_Custom_refresh-top` |
| Search submit (bottom button) | `#_qf_Custom_refresh-bottom` |
| Search results table | `table.selector` |
| Select-all checkbox (header) | `th [title="Select All Rows"]` |
| Result row by contact ID | `#rowid{contactId}` |

---

## Contribution Form Selectors

| Element | Selector |
|---------|----------|
| Contact autocomplete | `#contact_1` |
| Profiles / new contact dropdown | `#profiles_1` |
| Contribution type | `#contribution_type_id` |
| Total amount | `#total_amount` |
| Contribution status | `#contribution_status_id` |
| Receive date | `#receive_date` |
| Payment method | `#payment_instrument_id` |
| Transaction ID | `#trxn_id` |
| Save / submit | `#_qf_Contribution_upload-bottom` |

**Contribution status values**: 1 = Completed, 2 = Pending, 3 = Cancelled, 4 = Failed

---

## Inline Contact Creation (within Contribution Form)

When the contribution form is open, select "New Individual" from the profiles dropdown to create a contact inline:

```javascript
// '4' = New Individual option in the profiles dropdown
await utils.selectOption(page.locator('#profiles_1'), '4');

await utils.fillInput(page.locator('form#Edit #last_name'), lastName);
await utils.fillInput(page.locator('form#Edit #first_name'), firstName);
await page.locator('#_qf_Edit_next').click();

// Verify the contact was created and selected
await expect(page.locator('#contact_1')).toHaveValue(`${firstName} ${lastName}`);
```

---

## Reading Page Title (D10 vs D7 Compatibility)

The netiCRM test environment supports both Drupal 7 and Drupal 10. The page title selector differs between versions:

```javascript
const titleEl = page.locator('h1.page-title');
if (await titleEl.count() > 0) {
  // Drupal 10
  await expect(titleEl).toHaveText('Expected Title');
} else {
  // Drupal 7
  await expect(page.locator('#page-title')).toHaveText('Expected Title');
}
```

For convenience, see the `check_page_title()` helper in `contribution_booster.spec.js` — copy it into any spec that needs page title assertions.

---

## Validating Form Errors (body text approach)

When testing that a form rejects invalid input, read the full page body text rather than counting `.crm-error` elements:

```javascript
await page.locator('#_qf_Custom_refresh-top').click();
await utils.wait(2000);
const pageText = await page.locator('body').innerText();
// Match the actual error message text
expect(pageText).toMatch(/must be earlier|errors in the form|valid date/);
```
