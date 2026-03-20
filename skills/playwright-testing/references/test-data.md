---
name: test-data
description: Creating test data via the CiviCRM admin UI — contacts, contributions, and today's date patterns
type: reference
---

# Creating Test Data via the Admin UI

Do not rely on pre-existing database fixtures. Create test-specific records in a `TC-setup` test using the CiviCRM admin UI, then verify and clean up in subsequent tests.

---

## Creating a Contact + Contribution (inline flow)

```javascript
const firstName = 'TF' + utils.makeid(5);
const lastName  = 'TF' + utils.makeid(5);

await page.goto('civicrm/contribute/add?reset=1&action=add&context=standalone');
await utils.wait(2000);

// Select 'New Individual' from profiles dropdown ('4' = New Individual)
await utils.selectOption(page.locator('#profiles_1'), '4');

// Fill in the inline contact creation form
await utils.fillInput(page.locator('form#Edit #last_name'), lastName);
await utils.fillInput(page.locator('form#Edit #first_name'), firstName);
await page.locator('#_qf_Edit_next').click();
await utils.wait(2000);

// Confirm contact was created and selected
await expect(page.locator('#contact_1')).toHaveValue(`${firstName} ${lastName}`);

// Fill contribution fields
await utils.selectOption(page.locator('#contribution_type_id'), '1'); // 1 = General
await utils.fillInput(page.locator('#total_amount'), '100');

// Set status (1=Completed, 2=Pending, 3=Cancelled, 4=Failed)
await utils.selectOption(page.locator('#contribution_status_id'), '4'); // Failed

// Submit
await page.locator('#_qf_Contribution_upload-bottom').click();
await utils.wait(2000);
await expect(page.locator('.crm-error')).toHaveCount(0);
```

---

## Sort Name Convention

CiviCRM stores Individual sort names as `Last, First`. Use the unique `lastName` as a search token when verifying result rows:

```javascript
const sortName = `${lastName}, ${firstName}`;

// After searching, confirm the contact appears:
await expect(page.locator('table.selector')).toContainText(lastName);

// Confirm the contact is absent:
const pageText = await page.locator('body').innerText();
expect(pageText).not.toContain(lastName);
```

---

## Using Today's Date for `created_date`-Based Tests

`created_date` is auto-set on record creation. Compute today's date in JavaScript and use it as the "hit" range:

```javascript
const now = new Date();
const todayYear  = now.getFullYear();
const todayMonth = now.getMonth() + 1; // 1-indexed
const todayDay   = now.getDate();

// 'Hit' range: today to today (matches just-created record)
await utils.selectDate(page, page.locator('#failed_date_from'), todayYear, todayMonth, todayDay);
await utils.selectDate(page, page.locator('#failed_date_to'),   todayYear, todayMonth, todayDay);

// 'Miss' range: two years ago (will never contain today's record)
const pastYear = todayYear - 2;
await utils.selectDate(page, page.locator('#failed_date_from'), pastYear, 1,  1);
await utils.selectDate(page, page.locator('#failed_date_to'),   pastYear, 12, 31);
```

> Never hard-code a past date for the "hit" range — the test will break once the fixed date no longer matches newly-created data. Always derive from `new Date()`.
