# CiviCRM/netiCRM Javascript API Reference for Playwright Testing

This reference explains how to correctly interact with the CiviCRM/netiCRM AJAX API within a Playwright testing environment.

## Table of Contents
1. [Core Mechanism](#core-mechanism)
2. [Security Requirements](#security-requirements)
3. [Recommended Usage in Playwright](#recommended-usage-in-playwright)
4. [Common Pitfalls](#common-pitfalls)

---

## Core Mechanism

The CiviCRM/netiCRM frontend API is primarily accessed through a jQuery-based wrapper: `cj().crmAPI()`.

- **Endpoint**: `civicrm/ajax/rest`
- **Definition File**: `js/rest.js`
- **Backend Handler**: `CRM_Utils_REST::ajax()` in `CRM/Utils/REST.php`

The API supports both APIv3 and netiCRM-specific extensions. It handles JSON stringification and parameter preparation automatically.

---

## Security Requirements

The backend implementation of the AJAX API has strict CSRF protections:

1.  **X-Requested-With Header**: The request **MUST** include the header `X-Requested-With: XMLHttpRequest`. 
2.  **Session Cookie**: The request must be made within an authenticated session (handled automatically by the browser/Playwright if logged in).

**Anti-pattern**: Using `page.goto('civicrm/ajax/rest?...')` will fail because it is treated as a standard page navigation, which does not send the `X-Requested-With` header, triggering a security alert:
`"SECURITY ALERT: Ajax requests can only be issued by javascript clients..."`

---

## Recommended Usage in Playwright

To interact with the API during a test, use `page.evaluate` to execute the API call within the browser context. This ensures that the `cj().crmAPI` function is available and the security headers are correctly applied by jQuery.

### API Wrapper Template

Use this pattern to wrap the callback-based `crmAPI` into a modern `Promise` for use with `await`.

```javascript
/**
 * Helper to call CiviCRM API v3 within Playwright evaluate block.
 */
async function callCiviApi(page, entity, action, params) {
  return await page.evaluate(async ({ entity, action, params }) => {
    return new Promise((resolve, reject) => {
      if (typeof cj === 'undefined' || typeof cj().crmAPI !== 'function') {
        reject(new Error('CiviCRM JS API (cj().crmAPI) is not loaded on this page.'));
        return;
      }
      cj().crmAPI(entity, action, params, {
        success: (data) => resolve(data),
        error: (err) => reject(err)
      });
    });
  }, { entity, action, params });
}
```

### Example: Updating a Mailing

```javascript
async function updateMailing(page, mailingName, subject) {
  // 1. Get Mailing ID
  const getResult = await callCiviApi(page, 'Mailing', 'get', { 
    sequential: 1, 
    name: mailingName 
  });
  
  if (getResult.is_error || getResult.count === 0) {
    throw new Error(`Mailing not found: ${mailingName}`);
  }
  const mailingId = getResult.values[0].id;

  // 2. Update the Mailing
  return await callCiviApi(page, 'Mailing', 'create', {
    id: mailingId,
    subject: subject,
    sequential: 1
  });
}
```

---

## Common Pitfalls

- **Page Context**: `cj().crmAPI` is only available on pages that include the CiviCRM core resources. Ensure the test is on a CiviCRM-rendered page (e.g., `civicrm/dashboard`, `civicrm/mailing/browse`) before calling.
- **Sequential Parameter**: Always include `sequential: 1` if you expect the results in the `values` array to be indexed numerically starting from 0.
- **Error Handling**: Always check `result.is_error` even if the Promise resolves, as some API errors might still be returned as "success" status codes with an error payload.
