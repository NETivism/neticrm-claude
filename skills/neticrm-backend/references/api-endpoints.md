# Implementing API Endpoints (api/v3/)

## File structure and naming

```
api/v3/
├── Email.php           # Simple CRUD (good reference)
├── Contact.php         # Entity with custom actions (checksum, etc.)
├── Contribution.php    # Entity with custom actions (sendconfirmation, etc.)
└── Generic/            # Shared actions (Getactions, Setvalue, Update...)
```

Function naming (snake_case, all lowercase):
```
civicrm_api3_{entity}_{action}($params)        # main action handler
_civicrm_api3_{entity}_{action}_spec(&$params) # spec function (optional; declares params)
```

Examples:
```
civicrm_api3_email_create()          → Email / create
civicrm_api3_contact_checksum()      → Contact / checksum (custom)
_civicrm_api3_email_create_spec()    → spec for email create
```

## Standard CRUD (using helpers)

```php
// Email.php — minimal CRUD

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

Available helpers (defined in `api/v3/utils.php`):

| Helper | Purpose |
|--------|---------|
| `_civicrm_api3_basic_get($bao, $params)` | SELECT with filters and pagination |
| `_civicrm_api3_basic_create($bao, $params)` | INSERT or UPDATE (include `id` to update) |
| `_civicrm_api3_basic_delete($bao, $params)` | DELETE by `id` |
| `_civicrm_api3_get_BAO(__FUNCTION__)` | Resolve BAO class from function name |

## Spec functions

Declare parameter metadata — required fields, defaults, types. Optional but recommended for any non-trivial action:

```php
function _civicrm_api3_email_create_spec(&$params) {
  $params['email']['api.required'] = 1;
  $params['contact_id']['api.required'] = 1;
  $params['is_primary']['api.default'] = 0;
}
```

Common spec attributes:

```php
$params['field']['api.required'] = 1;          // required field
$params['field']['api.default']  = 'value';    // default value
$params['field']['api.aliases']  = ['alias1']; // alternative param names

// Full field definition (for non-DAO fields)
$params['note'] = [
  'name'        => 'note',
  'title'       => 'Note',
  'type'        => CRM_Utils_Type::T_TEXT,
  'description' => 'Associated note in the notes table',
];

// Foreign key field
$params['soft_credit_to'] = [
  'name'        => 'soft_credit_to',
  'title'       => 'Soft Credit contact ID',
  'type'        => CRM_Utils_Type::T_INT,
  'FKClassName' => 'CRM_Contact_DAO_Contact',
];
```

Type constants (`CRM_Utils_Type`):

| Constant | Meaning |
|----------|---------|
| `T_INT` | Integer |
| `T_STRING` | String |
| `T_BOOLEAN` | Boolean |
| `T_DATE` | Date |
| `T_MONEY` | Decimal / money |
| `T_TEXT` | Long text |

## Custom actions

```php
// Contact.php — checksum action

function _civicrm_api3_contact_checksum_spec(&$params) {
  $params['contact_id']['api.required'] = 1;
  $params['live']['api.required'] = 1;
}

function civicrm_api3_contact_checksum($params) {
  if (!CRM_Utils_Rule::positiveInteger($params['live']) || $params['live'] > 360) {
    return civicrm_api3_create_error('Parameter live should be integer indicate hours. Cannot over 360 hours.');
  }

  $contactId = CRM_Core_DAO::getFieldValue('CRM_Contact_DAO_Contact', $params['contact_id'], 'id');
  if (empty($contactId)) {
    return civicrm_api3_create_error('Parameter contact_id should be integer and exists on current database.');
  }

  $checksum = CRM_Contact_BAO_Contact_Utils::generateChecksum($params['contact_id'], $params['ts'], $params['live']);
  return civicrm_api3_create_success([[$params['contact_id'] => $checksum]], $params, 'contact', 'checksum');
}
```

Custom action with exception handling:

```php
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

Validation helpers:

```php
// Throw exception if any listed param is missing
civicrm_api3_verify_mandatory($params, NULL, ['contact_id', 'total_amount']);

// Throw exception if NONE of the listed params are present (at least one required)
civicrm_api3_verify_one_mandatory($params, NULL, ['id', 'external_identifier']);
```

## Return values

```php
// Success (with data)
return civicrm_api3_create_success($valuesArray, $params, 'Contribution', 'create');
// → ['is_error'=>0, 'version'=>3, 'count'=>N, 'id'=>123, 'values'=>[...]]

// Success (no data)
return civicrm_api3_create_success();

// Error
return civicrm_api3_create_error('Could not delete contribution');
// → ['is_error'=>1, 'error_message'=>'...', 'version'=>3]

// Error with extra data
return civicrm_api3_create_error('Invalid parameter', ['field' => 'total_amount']);

// Throw exception (caught by API framework; same effect)
throw new Exception('Contribution does not exist');
throw new API_Exception('Invalid status', 'invalid_status');
```
