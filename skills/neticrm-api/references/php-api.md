# PHP API — netiCRM/CiviCRM

The PHP API and the REST API are the same mechanism. REST sends params via HTTP and receives JSON; PHP passes an array and receives an array. Entity, action, and field names are identical.

---

## Internal PHP Calls (civicrm_api3)

### Basic get / create / delete

```php
// GET — fetch multiple records; returns $result['values'] (keyed by id)
$result = civicrm_api3('Contribution', 'get', [
  'contact_id' => $contactId,
  'options'    => ['limit' => 0, 'sort' => 'receive_date DESC'],
  'return'     => ['id', 'total_amount', 'receive_date'],
]);
// $result['values'] = [ id => [...], ... ]
// $result['count']  = number of records

// GET single record — throws exception if 0 or more than 1 result
$contribution = civicrm_api3('Contribution', 'getsingle', ['id' => $id]);

// GET count only
$count = civicrm_api3('Contribution', 'getcount', ['contact_id' => $contactId]);

// CREATE (no id = insert; with id = update)
$result = civicrm_api3('Contribution', 'create', [
  'contact_id'              => $contactId,
  'total_amount'            => 100,
  'contribution_type_id'    => 1,
  'receive_date'            => date('YmdHis'),
]);
// $result['id'] = id of the created/updated record

// DELETE
civicrm_api3('Contribution', 'delete', ['id' => $id]);
```

### Error handling

`civicrm_api3()` throws `CiviCRM_API3_Exception` by default when `is_error=1`.

```php
try {
  $result = civicrm_api3('Contribution', 'getsingle', ['id' => $id]);
}
catch (CiviCRM_API3_Exception $e) {
  CRM_Core_Error::debug_var('API error', $e->getMessage());
}
```

### options parameter

Identical to REST; pass as an array:

```php
civicrm_api3('Contact', 'get', [
  'options' => [
    'limit'  => 100,
    'offset' => 0,
    'sort'   => 'created_date asc',
  ],
]);
```

### Nested queries

```php
civicrm_api3('Contact', 'get', [
  'id' => 1234,
  'api.Email.get' => ['contact_id' => '$value.id'],
  'api.CustomValue.get' => [
    'entity_table' => 'civicrm_contact',
    'entity_id'    => '$value.id',
  ],
]);
```
