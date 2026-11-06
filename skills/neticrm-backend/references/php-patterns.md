# PHP Patterns — netiCRM/CiviCRM

## Table of Contents
1. [BAO Class Patterns](#1-bao-class-patterns)
2. [Form Class Patterns](#2-form-class-patterns)
3. [Routing](#3-routing)
4. [Permissions](#4-permissions)
5. [Translation (ts)](#5-translation-ts)
6. [Common Utilities](#6-common-utilities)
7. [Testing](#7-testing)
8. [Security](#8-security)
9. [Custom AJAX Endpoints](#9-custom-ajax-endpoints)

---

## 1. BAO Class Patterns

BAO (Business Access Object) contains all business logic. Extends DAO.

```php
class CRM_Contribute_BAO_Contribution extends CRM_Contribute_DAO_Contribution {

  /**
   * Create or update a contribution record.
   */
  public static function create(&$params) {
    $contribution = new CRM_Contribute_BAO_Contribution();
    $contribution->copyValues($params);

    $transaction = new CRM_Core_Transaction();
    try {
      $contribution->save();
      $transaction->commit();
      return $contribution;
    }
    catch (Exception $e) {
      $transaction->rollback();
      throw $e;
    }
  }

  /**
   * Retrieve a contribution by ID.
   */
  public static function retrieve($id) {
    return CRM_Core_DAO::findById('CRM_Contribute_BAO_Contribution', $id);
  }

  /**
   * Delete a contribution.
   */
  public static function deleteContribution($id) {
    CRM_Utils_Hook::pre('delete', 'Contribution', $id, CRM_Core_DAO::$_nullArray);
    $dao = new CRM_Contribute_DAO_Contribution();
    $dao->id = $id;
    $dao->delete();
    CRM_Utils_Hook::post('delete', 'Contribution', $id, $dao);
  }
}
```

**Key conventions:**
- Static methods for CRUD operations (`create`, `retrieve`, `delete`)
- Wrap multi-step writes in `CRM_Core_Transaction`
- Fire `CRM_Utils_Hook::pre()` and `CRM_Utils_Hook::post()` for deletions and major operations

---

## 2. Form Class Patterns

Form classes handle user-facing forms. Three lifecycle methods must be implemented in order.

```php
class CRM_Contribute_Form_Contribution extends CRM_Core_Form {

  // Properties: underscore prefix for instance state
  protected $_contributionId;
  protected $_contactId;

  /**
   * Phase 1: Validate access, set up instance state.
   */
  public function preProcess() {
    $this->_contributionId = CRM_Utils_Request::retrieve('id', 'Positive', $this);
    if (!CRM_Core_Permission::check('edit contributions')) {
      CRM_Utils_System::permissionDenied();
    }
    parent::preProcess();
  }

  /**
   * Phase 2: Build form elements.
   */
  public function buildQuickForm() {
    $this->add('text', 'total_amount', ts('Amount'), ['size' => 8], TRUE);
    $this->add('select', 'financial_type_id', ts('Financial Type'), $this->getFinancialTypes(), TRUE);
    $this->addButtons([['type' => 'submit', 'name' => ts('Save')]]);
    parent::buildQuickForm();
  }

  /**
   * Phase 3: Process submitted data.
   */
  public function postProcess() {
    $values = $this->exportValues();
    CRM_Contribute_BAO_Contribution::create($values);
    CRM_Core_Session::setStatus(ts('Contribution saved.'), ts('Saved'), 'success');
  }
}
```

**Key conventions:**
- `preProcess()` → permission and request validation
- `buildQuickForm()` → form field definitions
- `postProcess()` → call BAO to persist data, then set session status
- Use `CRM_Utils_Request::retrieve()` for URL parameters (never `$_GET` directly)

---

## 3. Routing

Routes are defined in `CRM/*/xml/Menu/*.xml`.

```xml
<menu>
  <!-- Standard authenticated page -->
  <item>
    <path>civicrm/contribute/add</path>
    <title>Add Contribution</title>
    <page_callback>CRM_Contribute_Form_Contribution</page_callback>
    <access_arguments>edit contributions</access_arguments>
  </item>

  <!-- Multiple permissions: comma = AND, semicolon = OR -->
  <item>
    <path>civicrm/admin/contribute</path>
    <title>Contribution Settings</title>
    <page_callback>CRM_Contribute_Page_ContributionPage</page_callback>
    <access_arguments>access CiviContribute,administer CiviCRM</access_arguments>
  </item>

  <!-- Public endpoint (IPN/webhook) -->
  <item>
    <path>civicrm/payment/ipn/1</path>
    <page_callback>CRM_Core_Payment_PayflowPro::handlePaymentNotification</page_callback>
    <access_callback>1</access_callback>
    <is_public>true</is_public>
  </item>
</menu>
```

**Key elements:**
- `path` — URL
- `page_callback` — handler class
- `access_arguments` — permission string(s): `,` = AND, `;` = OR
- `access_callback>1` + `is_public>true` — bypass permission check (public routes only)

---

## 4. Permissions

### Where permissions are defined
- **Core**: `CRM_Core_Permission::basicPermissions()`
- **Components**: `CRM/*/Info.php::getPermissions()`

### Core permissions (common)
```
access CiviCRM          administer CiviCRM
view all contacts       edit all contacts       delete contacts
view all activities     delete activities
profile view            profile edit            profile create
```

### Component permissions
| Component | Key permissions |
|-----------|----------------|
| Contribute | `access CiviContribute`, `edit contributions`, `make online contributions` |
| Event | `access CiviEvent`, `edit event participants`, `register for events` |
| Member | `access CiviMember`, `edit memberships` |
| Mailing | `access CiviMail`, `view public CiviMail content` |
| Report | `access CiviReport`, `administer Reports` |

### Permission checks in code
```php
// Single permission
if (!CRM_Core_Permission::check('edit contributions')) {
  CRM_Utils_System::permissionDenied();
}

// AND logic
if (CRM_Core_Permission::check('access CiviCRM') && CRM_Core_Permission::check('administer CiviCRM')) {
  // both required
}

// Using checkAnyPerm (OR logic)
$perms = ['edit contributions', 'administer CiviCRM'];
if (!CRM_Core_Permission::checkAnyPerm($perms)) {
  CRM_Utils_System::permissionDenied();
}
```

---

## 5. Translation (ts)

All user-facing strings must be wrapped in `ts()`.

```php
// Simple
ts('Hello world')

// With placeholder
ts('Hello %1', [1 => $name])

// Multiple placeholders
ts('%1 contributions for %2', [1 => $count, 2 => $contactName])

// JavaScript context
ts('Are you sure?', ['escape' => 'js'])

// Plural forms
ts('One item', ['count' => $n, 'plural' => '%count items'])
```

**Translate**: labels, buttons, messages, error text, status notifications
**Do not translate**: log messages, internal keys, variable content, database field names

---

## 6. Common Utilities

```php
// Debug output (development only)
CRM_Core_Error::debug_var('label', $variable);

// Session status message (shown to user)
CRM_Core_Session::setStatus(ts('Record saved.'), ts('Success'), 'success');
CRM_Core_Session::setStatus(ts('An error occurred.'), ts('Error'), 'error');

// Safe array access with default
$value = CRM_Utils_Array::value('key', $array, $default);

// Direct SQL (use parameterized form)
CRM_Core_DAO::executeQuery(
  "SELECT * FROM civicrm_contact WHERE id = %1",
  [1 => [$contactId, 'Integer']]
);

// Find single record by ID
$dao = CRM_Core_DAO::findById('CRM_Contribute_BAO_Contribution', $id);

// Retrieve URL parameter safely
$id = CRM_Utils_Request::retrieve('id', 'Positive', $this, FALSE);
// Types: 'Positive', 'Integer', 'String', 'Boolean', 'Date'
```

---

## 7. Testing

### Directory structure
```
CRM/Utils/RequestLimiter.php  →  tests/phpunit/CRM/Utils/RequestLimiterTest.php
CRM/Contribute/BAO/Contribution.php  →  tests/phpunit/CRM/Contribute/BAO/ContributionTest.php
```

### Test class structure
```php
// Reference: tests/phpunit/CiviTest/CiviUnitTestCase.php
// Example: tests/phpunit/CRM/Utils/TypeTest.php

class CRM_Contribute_BAO_ContributionTest extends CiviUnitTestCase {

  public function setUp() {
    parent::setUp();
    // Set up fixtures
  }

  public function tearDown() {
    // Clean up
    parent::tearDown();
  }

  public function testCreateContribution() {
    $params = [
      'contact_id' => $this->individualCreate(),
      'total_amount' => 100,
      'financial_type_id' => 1,
      'receive_date' => date('YmdHis'),
    ];
    $contribution = CRM_Contribute_BAO_Contribution::create($params);
    $this->assertNotNull($contribution->id);
    $this->assertEquals(100, $contribution->total_amount);
  }
}
```

---

## 8. Security

### Parameterized queries — always required
```php
// CORRECT: parameterized
CRM_Core_DAO::executeQuery(
  "SELECT * FROM civicrm_contact WHERE email = %1 AND is_deleted = 0",
  [1 => [$email, 'String']]
);

// WRONG: string concatenation — SQL injection risk
CRM_Core_DAO::executeQuery("SELECT * FROM civicrm_contact WHERE email = '$email'");
```

### Parameter type tokens
| Token | Type |
|-------|------|
| `'Integer'` | Integer |
| `'Positive'` | Positive integer |
| `'String'` | String (escaped) |
| `'Boolean'` | Boolean |
| `'Date'` | Date |
| `'Memo'` | Long text |

### Output escaping
```php
// Plain text printed from PHP
htmlspecialchars($value, ENT_QUOTES, 'UTF-8')

// HTML that is meant to be rendered (rich text): strip unsafe tags/attributes
CRM_Utils_String::htmlPurifier($html)
```

There is no `CRM_Utils_String::escapeHtml()`. Values passed to Smarty are escaped in the template (`{$var|escape}`) — Smarty 2 does not do it automatically; see the neticrm-frontend skill.

### Checklist before submitting PHP code
- [ ] Permission checked before accessing/modifying data
- [ ] Every record id taken from the request is checked against the current user (see [Custom AJAX Endpoints](#9-custom-ajax-endpoints))
- [ ] All SQL uses parameterized queries
- [ ] All user-facing strings use `ts()`
- [ ] No sensitive data logged or exposed; responses only carry the fields the client needs
- [ ] `CRM_Utils_Request::retrieve()` used for URL parameters (not `$_GET`)

---

## 9. Custom AJAX Endpoints

Handlers in `CRM/<Component>/Page/AJAX.php` that read a JSON body from `php://input` and answer with `json_encode()` + `CRM_Utils_System::civiExit()` (e.g. `CRM_AI_Page_AJAX`). Routes live in `CRM/Core/xml/Menu/*.xml`. These are the endpoints the security issues of #46672 were found in.

### What the route does not protect
- `<access_arguments>access CiviCRM</access_arguments>` only means "a logged-in staff user". It says nothing about **which records** that user may read or change.
- A JSON body bypasses `CRM_Utils_Request` type checks and PHPIDS (`CRM_Core_IDS` only inspects `$_REQUEST`). Validate type and format yourself and treat every value as raw text.
- Keep the exact `Content-Type: application/json` check on POST handlers: a cross-site page cannot send that content type without a CORS preflight, and CORS is not enabled by default.

### Check every record id from the request
```php
$session = CRM_Core_Session::singleton();
if (!CRM_AI_BAO_AICompletion::isRecordOwner($id, $session->get('userID'))) {
  // Same answer for "does not exist" and "not yours", so ids cannot be probed
  self::responseError(['status' => 0, 'message' => 'The record was not found.'], self::HTTP_FORBIDDEN);
}
```

```php
// Ownership helper: empty ids fail, compare as integers
public static function isRecordOwner($id, $contactId) {
  if (empty($id) || empty($contactId)) {
    return FALSE;
  }
  $ownerId = CRM_Core_DAO::getFieldValue('CRM_AI_DAO_AICompletion', $id, 'contact_id');
  return !empty($ownerId) && (int) $ownerId === (int) $contactId;
}
```

- **Records shared on purpose** (templates, published items): put the sharing condition into the lookup itself, e.g. `['id' => $id, 'is_template' => 1]` passed to `commonRetrieve()`. Looking the row up by id alone returns private rows too.
- **Where the check lives**: in the AJAX handler when the BAO method is also called by admin forms that legitimately edit other people's records (moving it into the BAO breaks them); in the BAO only when every caller needs it.
- Ids are sequential integers — assume they will be guessed.

### Tokens and keys
```php
// CRM_Core_Key::validate() returns NULL on failure, and NULL == '' is TRUE,
// so a loose comparison lets an empty token through
$isValid = !empty($token) && CRM_Core_Key::validate($token, $name) === $token;
```

### Return only what the client uses
- Build the response from an explicit list of columns. Do not `SELECT *` or `json_encode()` a full `commonRetrieve()` row, especially for data other users can read.
- Log-like columns are the usual leak: in #46672 a template's `post_data` (the raw request sent to OpenAI) carried the earlier, private turns of the conversation to every user who opened the template list, although the UI only showed role, tone and content.

### Saved values are printed elsewhere
Free text saved through an endpoint (names, titles, notes, AI output) is later shown on other pages — admin lists and view pages included. Each of those templates must escape it; see the neticrm-frontend skill, Security Rules.
