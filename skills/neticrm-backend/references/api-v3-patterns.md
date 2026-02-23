# API v3 Patterns — netiCRM/CiviCRM

## Ground Truth

This file documents conventions and patterns. If anything feels off, read the source directly:

| Topic | Source file |
|-------|-------------|
| Simple CRUD | `api/v3/Email.php` |
| Custom action | `api/v3/Contact.php` (checksum) |
| Complex action with BAO | `api/v3/Contribution.php` (sendconfirmation) |
| Helper functions | `api/v3/utils.php` |

> Verified against codebase: 2026-02.

---

## Table of Contents
1. [File Structure & Naming](#1-file-structure--naming)
2. [Basic CRUD with Helper Functions](#2-basic-crud-with-helper-functions)
3. [Spec Functions](#3-spec-functions)
4. [Custom Actions](#4-custom-actions)
5. [Return Values](#5-return-values)
6. [Calling API Internally (PHP)](#6-calling-api-internally-php)

---

## 1. File Structure & Naming

```
api/v3/
├── Email.php           # Simple CRUD entity (good reference)
├── Contact.php         # Complex entity with custom actions
├── Contribution.php    # Entity with custom actions (sendconfirmation, etc.)
└── Generic/            # Shared actions (Getactions, Setvalue, Update...)
```

**Function naming** (snake_case, all lowercase):
```
civicrm_api3_{entity}_{action}($params)       # main action
_civicrm_api3_{entity}_{action}_spec(&$params) # spec (optional, defines params)
```

Examples:
```
civicrm_api3_email_create()          → Email / create
civicrm_api3_contact_checksum()      → Contact / checksum (custom)
_civicrm_api3_email_create_spec()    → spec for email create
```

**Class-to-BAO resolution**: `_civicrm_api3_get_BAO(__FUNCTION__)` derives the BAO class from the function name automatically.

---

## 2. Basic CRUD with Helper Functions

For standard CRUD, delegate to `_civicrm_api3_basic_*` helpers. This is the preferred pattern.

```php
// Email.php — minimal CRUD example

function civicrm_api3_email_get($params) {
  return _civicrm_api3_basic_get(_civicrm_api3_get_BAO(__FUNCTION__), $params);
}

function civicrm_api3_email_create($params) {
  return _civicrm_api3_basic_create(_civicrm_api3_get_BAO(__FUNCTION__), $params);
}

function civicrm_api3_email_delete($params) {
  return _civicrm_api3_basic_delete(_civicrm_api3_get_BAO(__FUNCTION__), $params);
}
```

**Available helpers** (defined in `api/v3/utils.php`):

| Helper | Purpose |
|--------|---------|
| `_civicrm_api3_basic_get($bao, $params)` | Standard SELECT with filters/pagination |
| `_civicrm_api3_basic_create($bao, $params)` | INSERT or UPDATE (pass `id` to update) |
| `_civicrm_api3_basic_delete($bao, $params)` | DELETE by `id` |
| `_civicrm_api3_get_BAO(__FUNCTION__)` | Resolve BAO class from function name |

---

## 3. Spec Functions

Spec functions define parameter metadata — required fields, defaults, types, aliases. They are optional but recommended for any non-trivial action.

```php
// Naming: _civicrm_api3_{entity}_{action}_spec(&$params)
function _civicrm_api3_email_create_spec(&$params) {
  $params['email']['api.required'] = 1;
  $params['contact_id']['api.required'] = 1;
  $params['is_primary']['api.default'] = 0;
}
```

**Common spec attributes:**

```php
$params['field']['api.required'] = 1;          // required field
$params['field']['api.default']  = 'value';    // default value
$params['field']['api.aliases']  = ['alias1']; // alternative param names

// Full field definition (used for custom/non-DAO fields)
$params['note'] = [
  'name'        => 'note',
  'title'       => 'Note',
  'type'        => CRM_Utils_Type::T_TEXT,
  'description' => 'Associated note in the notes table',
];

// Foreign key reference
$params['soft_credit_to'] = [
  'name'        => 'soft_credit_to',
  'title'       => 'Soft Credit contact ID',
  'type'        => CRM_Utils_Type::T_INT,
  'FKClassName' => 'CRM_Contact_DAO_Contact',
];
```

**Type constants** (`CRM_Utils_Type`):

| Constant | Meaning |
|----------|---------|
| `T_INT` | Integer |
| `T_STRING` | String |
| `T_BOOLEAN` | Boolean |
| `T_DATE` | Date |
| `T_MONEY` | Decimal/money |
| `T_TEXT` | Long text |

---

## 4. Custom Actions

For actions beyond basic CRUD, implement the full function manually.

### Simple custom action

```php
// Contact.php — checksum action

function _civicrm_api3_contact_checksum_spec(&$params) {
  $params['contact_id']['api.required'] = 1;
  $params['live']['api.required'] = 1;
}

function civicrm_api3_contact_checksum($params) {
  // Validate business rules
  if (!CRM_Utils_Rule::positiveInteger($params['live']) || $params['live'] > 360) {
    return civicrm_api3_create_error('Parameter live should be integer indicate hours. Cannot over 360 hours.');
  }

  // Check record exists
  $contactId = CRM_Core_DAO::getFieldValue('CRM_Contact_DAO_Contact', $params['contact_id'], 'id');
  if (empty($contactId)) {
    return civicrm_api3_create_error('Parameter contact_id should be integer and exists on current database.');
  }

  // Business logic via BAO
  $checksum = CRM_Contact_BAO_Contact_Utils::generateChecksum($params['contact_id'], $params['ts'], $params['live']);

  return civicrm_api3_create_success([[$params['contact_id'] => $checksum]], $params, 'contact', 'checksum');
}
```

### Custom action with exception handling

```php
// Extension.php — install action

function civicrm_api3_extension_install($params) {
  $keys = _civicrm_api3_getKeys($params);
  if (count($keys) == 0) {
    return civicrm_api3_create_success();
  }

  try {
    CRM_Extension_System::singleton()->getManager()->install($keys);
  }
  catch (CRM_Extension_Exception $e) {
    return civicrm_api3_create_error($e->getMessage());
  }

  return civicrm_api3_create_success();
}
```

### Custom action using BAO directly

```php
// Contribution.php — sendconfirmation action

function _civicrm_api3_contribution_sendconfirmation_spec(&$params) {
  $params['id'] = [
    'api.required' => 1,
    'title'        => 'Contribution ID',
  ];
}

function civicrm_api3_contribution_sendconfirmation($params) {
  $contribution = new CRM_Contribute_BAO_Contribution();
  $contribution->id = $params['id'];
  if (!$contribution->find(TRUE)) {
    throw new Exception('Contribution does not exist');
  }
  $input = $ids = $cvalues = [];
  $contribution->loadRelatedObjects($input, $ids, FALSE, TRUE);
  $contribution->composeMessageArray($input, $ids, $cvalues, FALSE, FALSE);
}
```

**Mandatory validation helpers:**

```php
// Throw exception if any listed param is missing
civicrm_api3_verify_mandatory($params, NULL, ['contact_id', 'total_amount']);

// Throw exception if NONE of the listed params are present
civicrm_api3_verify_one_mandatory($params, NULL, ['id', 'external_identifier']);
```

---

## 5. Return Values

### Success

```php
// Full signature
civicrm_api3_create_success($values, $params, $entity, $action)

// With data
return civicrm_api3_create_success($valuesArray, $params, 'Contribution', 'create');

// Empty success (no data to return)
return civicrm_api3_create_success();

// Response structure (auto-generated)
[
  'is_error' => 0,
  'version'  => 3,
  'count'    => 1,
  'id'       => 123,
  'values'   => [ /* entity data */ ],
]
```

### Error

```php
// Simple error
return civicrm_api3_create_error('Could not delete contribution');

// Error with extra data
return civicrm_api3_create_error('Invalid parameter', ['field' => 'total_amount']);

// Throw exception (caught by API framework, same effect)
throw new Exception('Contribution does not exist');
throw new API_Exception('Invalid status', 'invalid_status');

// Response structure
[
  'is_error'      => 1,
  'error_message' => 'Could not delete contribution',
  'version'       => 3,
]
```

---

## 6. Calling API Internally (PHP)

```php
// Standard call — throws CiviCRM_API3_Exception on error
$result = civicrm_api3('Contribution', 'get', [
  'contact_id' => $contactId,
  'options'    => ['limit' => 0, 'sort' => 'receive_date DESC'],
  'return'     => ['id', 'total_amount', 'receive_date'],
]);
// $result['values'] = keyed array of records
// $result['count']  = number of results

// Single record — throws exception if 0 or more than 1 result
$contribution = civicrm_api3('Contribution', 'getsingle', ['id' => $id]);

// Count only
$count = civicrm_api3('Contribution', 'getcount', ['contact_id' => $contactId]);

// Create (omit 'id') or update (include 'id')
$result = civicrm_api3('Contribution', 'create', [
  'contact_id'        => $contactId,
  'total_amount'      => 100,
  'financial_type_id' => 1,
  'receive_date'      => date('YmdHis'),
]);

// Delete
civicrm_api3('Contribution', 'delete', ['id' => $id]);

// Wrap in try/catch when calling from non-API code
try {
  $result = civicrm_api3('Contribution', 'getsingle', ['id' => $id]);
}
catch (CiviCRM_API3_Exception $e) {
  CRM_Core_Error::debug_var('API error', $e->getMessage());
}
```
