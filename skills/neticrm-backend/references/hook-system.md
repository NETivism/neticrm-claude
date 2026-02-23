# Hook System — netiCRM/CiviCRM

## Ground Truth

This file documents conventions and patterns. If anything feels off, read the source directly:

| Topic | Source file |
|-------|-------------|
| Available hook methods | `CRM/Utils/Hook.php` |
| Form hook firing order | `CRM/Core/Form.php` |
| pre/post in BAO | `CRM/Contribute/BAO/Contribution.php` |
| Module implementation examples | `neticrm/civicrm_webhook/civicrm_webhook.module` |

> Verified against codebase: 2026-02.
> Module examples (Section 3) reflect `neticrm/` code — update this file when module hook logic changes significantly.

---

## Table of Contents
1. [Overview](#1-overview)
2. [Where to Implement Hooks](#2-where-to-implement-hooks)
3. [Form Hooks](#3-form-hooks)
4. [Data Hooks (pre / post)](#4-data-hooks-pre--post)
5. [CRM_Utils_Hook — Available Methods](#5-crm_utils_hook--available-methods)

---

## 1. Overview

CiviCRM hooks are triggered via `CRM_Utils_Hook` static methods inside CiviCRM core (BAO, Form). Drupal modules receive them by implementing `{modulename}_civicrm_{hookname}()` functions.

**Function naming rule:**
```
{module_name}_civicrm_{hook_name}($arg1, ...)
```

Example: module `civicrm_webhook` implementing `hook_civicrm_post`:
```php
function civicrm_webhook_civicrm_post($op, $entityType, $id, &$object) { ... }
```

---

## 2. Where to Implement Hooks

Hooks live in Drupal `.module` files under `/neticrm/`:

```
neticrm/
├── civicrm_webhook/civicrm_webhook.module
├── civicrm_participant_serial/civicrm_participant_serial.module
├── civicrm_twaddress/civicrm_twaddress.module
└── civicrm_spgateway/civicrm_spgateway.module
```

Each `.module` file contains one or more `{module}_civicrm_{hook}()` functions.

---

## 3. Form Hooks

### hook_civicrm_buildForm
Fires after `buildQuickForm()` completes. Use to add fields, modify elements, inject JS, or assign template variables.

```php
// civicrm_participant_serial.module
function civicrm_participant_serial_civicrm_buildForm($form_name, &$form) {
  switch ($form_name) {
    case 'CRM_Event_Form_Registration_Register':
    case 'CRM_Event_Form_Registration_AdditionalParticipant':
      $cid = variable_get('civicrm_participant_serial', '');
      $c_field = 'custom_' . $cid;
      drupal_add_js('$(document).ready(function(){ $(".' . $c_field . '-section").hide(); });', 'inline');
      break;
  }
}

// civicrm_twaddress.module — modify form elements
function civicrm_twaddress_civicrm_buildForm($formName, &$form) {
  foreach ($form->_elements as $k => $e) {
    $name = $e->_attributes['name'];
    if (strstr($name, 'state_province') || !empty($e->_attributes['state-province'])) {
      $element = $form->getElement($name);
      // Reorder province options...
    }
  }
}

// civicrm_webhook.module — read POST params, store in form session
function civicrm_webhook_civicrm_buildForm($formName, &$form) {
  switch ($formName) {
    case 'CRM_Contribute_Form_Contribution_Main':
      $url = CRM_Utils_Request::retrieve('_wh_redirect', 'Link', CRM_Core_DAO::$_nullObject, FALSE, NULL, 'POST');
      if (CRM_Utils_Rule::url($url, $config->webhookDomain)) {
        $form->set('Webhook_Redirect_URL', $url);
      }
      break;
  }
}
```

### hook_civicrm_preSave
Fires before `postProcess()` saves data. Use to compute or set values before DB write.

```php
// civicrm_participant_serial.module
function civicrm_participant_serial_civicrm_preSave($form_name, &$form) {
  switch ($form_name) {
    case 'CRM_Event_Form_Registration_Register':
    case 'CRM_Event_Form_Registration_AdditionalParticipant':
      $event_id = $form->getVar('_eventId');
      // Generate and set serial number before save...
      break;
  }
}
```

### hook_civicrm_postProcess
Fires after `postProcess()` completes. Use to trigger side effects after data is saved.

```php
// civicrm_webhook.module
function civicrm_webhook_civicrm_postProcess($formName, &$form) {
  if ($formName == 'CRM_Contribute_Form_Contribution_Confirm') {
    $redirect = $form->get('Webhook_Redirect_URL');
    // Save webhook URL to custom field...
  }
}
```

### hook_civicrm_validate
Fires during form validation. Return `TRUE` to pass, or an array of `['field' => 'error message']` to block submission.

```php
// civicrm_spgateway.module
function civicrm_spgateway_civicrm_validate($form_name, &$form) {
  $errors = [];
  if ($form_name == 'CRM_Contribute_Form_Contribution_Main') {
    if (!empty($form['installments']) && $form['installments'] > 99) {
      $errors['installments'] = t('Installments must be lower than 99.');
    }
  }
  return empty($errors) ? TRUE : $errors;
}
```

### Form hook firing order

Triggered by `CRM/Core/Form.php`:

```
buildForm()
  → preProcess()              (Form method)
  → CRM_Utils_Hook::preProcess()
  → buildQuickForm()          (Form method)
  → CRM_Utils_Hook::buildForm()   ← hook_civicrm_buildForm

validate()
  → parent::validate()
  → CRM_Utils_Hook::validate()    ← hook_civicrm_validate

submit()
  → CRM_Utils_Hook::preSave()     ← hook_civicrm_preSave
  → postProcess()             (Form method)
  → CRM_Utils_Hook::postProcess() ← hook_civicrm_postProcess
```

---

## 4. Data Hooks (pre / post)

### hook_civicrm_post
Fires after a CiviCRM object is created, edited, or deleted.

```php
// civicrm_webhook.module — send webhook after contribution edit
function civicrm_webhook_civicrm_post($op, $entityType, $id, &$object) {
  if ($entityType == 'Contribution' && $op == 'edit') {
    $notify = civicrm_webhook_notify_params($id);
    if (!empty($notify['Webhook_Notify_URL'])) {
      civicrm_webhook_notify_send($notify['Webhook_Notify_URL'], $notify);
    }
  }
}

// webform_civicrm.module — clean up on Activity delete
function webform_civicrm_civicrm_post($op, $type, $id, $obj) {
  if ($type === 'Activity' && $op === 'delete') {
    db_update('webform_civicrm_submissions')
      ->fields(['activity_id' => 0])
      ->condition('activity_id', $id)
      ->execute();
  }
}
```

**Parameters:**
- `$op` — `'create'` | `'edit'` | `'delete'`
- `$entityType` / `$type` — object name (see table below)
- `$id` — object ID
- `$object` / `$obj` — reference to BAO/DAO object

### hook_civicrm_pre
Fires before a CiviCRM object is created, edited, or deleted. Allows modifying `$params` before DB write.

**Parameters:**
- `$op` — `'create'` | `'edit'` | `'delete'`
- `$objectName` — object name
- `$id` — object ID (`NULL` for new records)
- `&$params` — data being saved (modifiable)

### How BAO fires these hooks

From `CRM/Contribute/BAO/Contribution.php`:

```php
// Before save
if (!empty($ids['contribution'])) {
  CRM_Utils_Hook::pre('edit', 'Contribution', $ids['contribution'], $params);
}
else {
  CRM_Utils_Hook::pre('create', 'Contribution', NULL, $params);
}

// ... DB operation ...

// After save
if (!empty($ids['contribution'])) {
  CRM_Utils_Hook::post('edit', 'Contribution', $contribution->id, $contribution);
}
else {
  CRM_Utils_Hook::post('create', 'Contribution', $contribution->id, $contribution);
}

// On delete
CRM_Utils_Hook::pre('delete', 'Contribution', $id, CRM_Core_DAO::$_nullArray);
// ... delete ...
CRM_Utils_Hook::post('delete', 'Contribution', $dao->id, $dao);
```

From `CRM/Contact/BAO/Contact.php` — uses contact type as `$objectName`:
```php
CRM_Utils_Hook::pre('edit', $params['contact_type'], $params['contact_id'], $params);
// $params['contact_type'] is 'Individual', 'Organization', or 'Household'
```

### Common `$objectName` values

| objectName | Triggered by |
|------------|-------------|
| `Contribution` | Contribution create/edit/delete |
| `Individual` / `Organization` / `Household` | Contact create/edit/delete |
| `Membership` | Membership create/edit/delete |
| `Participant` | Event participant create/edit/delete |
| `Relationship` | Relationship create/edit/delete |
| `ContributionRecur` | Recurring contribution |
| `MembershipPayment` | Membership payment |
| `GroupContact` | Group membership change |
| `Mailing` | Mailing create/edit/delete |
| `Activity` | Activity create/edit/delete |
| `Profile` | Profile form save |

---

## 5. CRM_Utils_Hook — Available Methods

Defined in `CRM/Utils/Hook.php`. Called inside CiviCRM core to fire hooks.

| Method | Drupal hook | When fired |
|--------|------------|-----------|
| `pre($op, $objectName, $id, &$params)` | `hook_civicrm_pre` | Before BAO create/edit/delete |
| `post($op, $objectName, $objectId, &$objectRef)` | `hook_civicrm_post` | After BAO create/edit/delete |
| `buildForm($formName, &$form)` | `hook_civicrm_buildForm` | After `buildQuickForm()` |
| `preProcess($formName, &$form)` | `hook_civicrm_preProcess` | At start of form build |
| `postProcess($formName, &$form)` | `hook_civicrm_postProcess` | After `postProcess()` |
| `validate($formName, &$fields, &$files, &$form)` | `hook_civicrm_validate` | During form validation |
| `preSave($formName, &$form)` | `hook_civicrm_preSave` | Before `postProcess()` saves |
| `custom($op, $groupID, $entityID, &$params)` | `hook_civicrm_custom` | Custom field operations |
| `tokens(&$tokens)` | `hook_civicrm_tokens` | Define email tokens |
| `tokenValues(&$details, &$contactIDs, ...)` | `hook_civicrm_tokenValues` | Fill email token values |
| `alterMailParams(&$params)` | `hook_civicrm_alterMailParams` | Modify outgoing email params |
| `alterPaymentProcessorParams(...)` | `hook_civicrm_alterPaymentProcessorParams` | Modify payment params |
