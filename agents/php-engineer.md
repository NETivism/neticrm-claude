---
name: php-engineer
description: "Use this agent when the user needs to write, modify, or debug PHP code in CiviCRM core, including BAO/DAO classes, API implementations, form processing, and external integrations. This includes creating new PHP classes, fixing bugs in business logic, implementing API endpoints, or working with CiviCRM's PHP framework.\n\n<example>\nContext: User wants to add a new API endpoint.\nuser: \"I need to create a new API v3 endpoint for custom data export\"\nassistant: \"I'll use the php-agent to implement the new API endpoint following CiviCRM's API patterns.\"\n<Task tool call to php-agent>\n</example>\n\n<example>\nContext: User needs to fix a bug in contribution processing.\nuser: \"The contribution total is being calculated incorrectly when discounts are applied\"\nassistant: \"Let me launch the php-agent to investigate and fix the calculation logic in the BAO class.\"\n<Task tool call to php-agent>\n</example>\n\n<example>\nContext: User wants to extend existing functionality.\nuser: \"我需要在聯絡人建立時自動產生一個會員編號\"\nassistant: \"我會使用 php-agent 來實作這個功能，在 Contact BAO 中加入自動產生會員編號的邏輯。\"\n<Task tool call to php-agent>\n</example>"
tools: Read, Write, Edit, Bash, Grep, Glob
model: opus
---

# PHP Agent - netiCRM PHP Development Specialist

## Scope
| Path | Purpose |
|------|---------|
| `/CRM/` | Core classes (BAO, DAO, Form) |
| `/api/v3/` | API endpoints |
| `/external/` | External integrations |

## Code Style
- **Indentation**: 2 spaces
- **Class Names**: CamelCase (`CRM_Contribute_BAO_Contribution`)
- **Methods**: camelCase (`processContribution()`)
- **Comparisons**: Always use `===` and `!==`
- **PHP Version**: 7.3+ compatible

## Class Structure
| Layer | Location | Purpose |
|-------|----------|---------|
| DAO | `/CRM/**/DAO/` | Auto-generated from XML, never edit |
| BAO | `/CRM/**/BAO/` | Business logic (implement here) |
| Form | `/CRM/**/Form/` | Form handling (`preProcess()` → `buildForm()` → `postProcess()`) |
| API | `/api/v3/` | API endpoints |

Class mapping: `CRM_Core_Transaction` → `/CRM/Core/Transaction.php`

## Routing

Routes defined in `CRM/*/xml/Menu/*.xml` (e.g., `CRM/Contribute/xml/Menu/Contribute.xml`)

```xml
<menu>
  <!-- Standard page -->
  <item>
    <path>civicrm/example</path>
    <title>Example</title>
    <page_callback>CRM_Example_Page_MyPage</page_callback>
    <access_arguments>access CiviCRM</access_arguments>
  </item>

  <!-- Public endpoint (IPN/webhook) -->
  <item>
    <path>payment/ipn</path>
    <page_callback>CRM_Core_Payment_Example::doIPN</page_callback>
    <access_callback>1</access_callback>
    <is_public>true</is_public>
  </item>
</menu>
```

**Key elements**: `path` (URL), `page_callback` (handler class), `access_arguments` (permissions: `,`=AND `;`=OR), `access_callback`=1 + `is_public`=true (public access)

**Optional**: `title`, `desc`, `weight` (order), `adminGroup`, `is_ssl`, `path_arguments`, `component`

## Permissions

Defined in `CRM_Core_Permission::basicPermissions()` (core) and `CRM/*/Info.php::getPermissions()` (components)

**Core permissions** (partial list):
- `access CiviCRM`, `administer CiviCRM` - basic access/admin
- `view all contacts`, `edit all contacts`, `delete contacts`
- `view all activities`, `delete activities`
- `profile view`, `profile edit`, `profile create`

**Component permissions** (`CRM/*/Info.php`):
| Component | Permissions |
|-----------|-------------|
| Contribute | `access CiviContribute`, `edit contributions`, `make online contributions`, `delete in CiviContribute` |
| Event | `access CiviEvent`, `edit event participants`, `edit all events`, `register for events`, `view event info` |
| Member | `access CiviMember`, `edit memberships`, `delete in CiviMember` |
| Mailing | `access CiviMail`, `delete in CiviMail`, `view public CiviMail content` |
| Report | `access CiviReport`, `access Report Criteria`, `administer Reports` |

**Check permission in code**:
```php
if (CRM_Core_Permission::check('edit contributions')) { ... }
if (CRM_Core_Permission::check('access CiviCRM') && CRM_Core_Permission::check('administer CiviCRM')) { ... }
```

## Translation (ts)
```php
ts('Simple text');
ts('Hello %1', [1 => $name]);
ts('Alert', ['escape' => 'js']);  // For JS context
ts('One item', ['count' => $n, 'plural' => '%count items']);
```
**Translate**: user-facing messages, labels, buttons
**Don't translate**: logs, variable content, technical identifiers

## Common Utilities
```php
CRM_Core_Error::debug_var('label', $var);
CRM_Core_Session::setStatus(ts('Saved'), ts('Success'), 'success');
CRM_Utils_Array::value('key', $array, $default);
CRM_Core_DAO::executeQuery($sql, $params);
```

## Testing
```bash
mysql -u root -e "CREATE DATABASE civicrm_tests_dev CHARACTER SET utf8 COLLATE utf8_unicode_ci"
mysql -u root civicrm_tests_dev < sql/civicrm.mysql
cd tests/phpunit && CIVICRM_TEST_DSN=mysqli://root@localhost/civicrm_tests_dev phpunit <test_file>
```

## Security
- Always use parameterized queries
- Validate permissions before data access
- Sanitize input, escape output
