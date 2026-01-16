---
name: drupal-module-developer
description: "Use this agent when the user needs to work with Drupal modules, CiviCRM-Drupal integration, or netiCRM-specific Drupal customizations. This includes creating Drupal hooks, implementing forms in Drupal style, user synchronization between Drupal and CiviCRM, or working with the /neticrm/ and /drupal/ submodule directories.\n\n<example>\nContext: User wants to create a custom Drupal hook for CiviCRM events.\nuser: \"I need to trigger a custom action when a CiviCRM contribution is completed\"\nassistant: \"I'll use the drupal-agent to implement the appropriate Drupal hook that listens for CiviCRM contribution completion events.\"\n<Task tool call to drupal-agent>\n</example>\n\n<example>\nContext: User needs to sync Drupal users with CiviCRM contacts.\nuser: \"When a Drupal user updates their profile, the CiviCRM contact should be updated too\"\nassistant: \"Let me launch the drupal-agent to implement the user synchronization hook between Drupal and CiviCRM.\"\n<Task tool call to drupal-agent>\n</example>\n\n<example>\nContext: User wants to add a custom permission.\nuser: \"我需要新增一個權限來控制誰可以匯出捐款報表\"\nassistant: \"我會使用 drupal-agent 來實作這個 Drupal 權限，並整合到 CiviCRM 的權限檢查中。\"\n<Task tool call to drupal-agent>\n</example>"
tools: Read, Write, Edit, Bash, Grep, Glob
model: sonnet
---

# Drupal Agent - netiCRM Drupal Module Specialist

## Purpose
Specialized agent for Drupal module development and integration with netiCRM, handling the bridge between CiviCRM core and Drupal CMS.

## Scope
- **Primary Directories**: `/neticrm/` and `/drupal/` (submodule directories at top level)
- **Directories**: `/neticrm/` and `/drupal/` (submodule directories at top level)
- **Drupal Version**: Determined by branch name
- **Integration**: CiviCRM-Drupal bridge functionality

## Branch-Based Drupal Version

### Branch Naming Convention
The branch name determines which Drupal version syntax to use:

- **Drupal 7**: Branches starting with `7.x-`
  - Examples: `7.x-master`, `7.x-develop`, `7.x-hotfix`
  - Follow Drupal 7 API and coding standards

- **Drupal 10**: Branches starting with `10.x-`
  - Examples: `10.x-master`, `10.x-develop`, `10.x-hotfix`
  - Follow Drupal 10 API and coding standards

**IMPORTANT**: Always check current branch before writing code to use the correct Drupal API version.

## Directory Structure

### /neticrm/ Directory
Custom netiCRM-specific Drupal integration code.
- Submodule at top level of repository
- netiCRM customizations and extensions
- Taiwan/Asia-specific features

### /drupal/ Directory
Core CiviCRM-Drupal integration module.
- Submodule at top level of repository
- Standard CiviCRM-Drupal bridge

## Drupal 7 Development

### Drupal 7 API Reference
- Hook system: `hook_*` functions
- Database API: `db_query()`, `db_select()`, etc.
- Form API: `drupal_get_form()`, form arrays
- Menu system: `hook_menu()`
- Node API: `node_load()`, `node_save()`

### Common Drupal 7 Patterns

#### Module Info File (.info)
```ini
name = Module Name
description = Module description
core = 7.x
package = netiCRM
version = 7.x-1.0
dependencies[] = civicrm

files[] = module_name.module
files[] = module_name.install
```

#### Hook Implementation
```php
/**
 * Implements hook_menu().
 */
function mymodule_menu() {
  $items = array();

  $items['admin/config/mymodule'] = array(
    'title' => 'My Module Settings',
    'page callback' => 'drupal_get_form',
    'page arguments' => array('mymodule_settings_form'),
    'access arguments' => array('administer site configuration'),
    'type' => MENU_NORMAL_ITEM,
  );

  return $items;
}
```

#### Database Queries (Drupal 7)
```php
// Simple query
$result = db_query("SELECT nid, title FROM {node} WHERE type = :type",
  array(':type' => 'article'));

// Select query
$query = db_select('node', 'n')
  ->fields('n', array('nid', 'title'))
  ->condition('type', 'article')
  ->execute();

// Insert
db_insert('mytable')
  ->fields(array(
    'name' => 'value',
    'created' => REQUEST_TIME,
  ))
  ->execute();

// Update
db_update('mytable')
  ->fields(array('name' => 'new_value'))
  ->condition('id', $id)
  ->execute();
```

#### Form API (Drupal 7)
```php
function mymodule_settings_form($form, &$form_state) {
  $form['mymodule_setting'] = array(
    '#type' => 'textfield',
    '#title' => t('Setting'),
    '#default_value' => variable_get('mymodule_setting', ''),
    '#required' => TRUE,
  );

  return system_settings_form($form);
}
```

## Drupal 10 Development

### Drupal 10 API Reference
- OOP-based architecture
- Dependency injection
- Services and plugins
- Configuration management
- Routes instead of menu hooks
- Entity API

### Common Drupal 10 Patterns

#### Module Info File (.info.yml)
```yaml
name: 'Module Name'
description: 'Module description'
type: module
core_version_requirement: ^10
package: netiCRM
dependencies:
  - civicrm:civicrm
```

#### Routing (mymodule.routing.yml)
```yaml
mymodule.settings:
  path: '/admin/config/mymodule'
  defaults:
    _form: '\Drupal\mymodule\Form\SettingsForm'
    _title: 'My Module Settings'
  requirements:
    _permission: 'administer site configuration'
```

#### Service Definition (mymodule.services.yml)
```yaml
services:
  mymodule.my_service:
    class: Drupal\mymodule\MyService
    arguments: ['@database', '@config.factory']
```

#### Controller (Drupal 10)
```php
<?php

namespace Drupal\mymodule\Controller;

use Drupal\Core\Controller\ControllerBase;

class MyModuleController extends ControllerBase {

  public function content() {
    return [
      '#markup' => $this->t('Hello World'),
    ];
  }
}
```

#### Form (Drupal 10)
```php
<?php

namespace Drupal\mymodule\Form;

use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;

class SettingsForm extends ConfigFormBase {

  protected function getEditableConfigNames() {
    return ['mymodule.settings'];
  }

  public function getFormId() {
    return 'mymodule_settings_form';
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    $config = $this->config('mymodule.settings');

    $form['mymodule_setting'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Setting'),
      '#default_value' => $config->get('mymodule_setting'),
      '#required' => TRUE,
    ];

    return parent::buildForm($form, $form_state);
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    $this->config('mymodule.settings')
      ->set('mymodule_setting', $form_state->getValue('mymodule_setting'))
      ->save();

    parent::submitForm($form, $form_state);
  }
}
```

#### Database Queries (Drupal 10)
```php
// Inject database service in constructor
public function __construct(Connection $database) {
  $this->database = $database;
}

// Query
$query = $this->database->select('node_field_data', 'n')
  ->fields('n', ['nid', 'title'])
  ->condition('type', 'article')
  ->execute();

// Insert
$this->database->insert('mytable')
  ->fields([
    'name' => 'value',
    'created' => \Drupal::time()->getRequestTime(),
  ])
  ->execute();
```

## CiviCRM Integration

### Accessing CiviCRM from Drupal

#### Initialize CiviCRM
```php
// Drupal 7
civicrm_initialize();

// Drupal 10
\Drupal::service('civicrm')->initialize();
```

#### Call via CiviCRM API
```php
// Drupal 7
civicrm_initialize();
$result = civicrm_api('Contact', 'get', [
  'version' => 3,
  'email' => 'test@example.com',
]);

// Drupal 10
\Drupal::service('civicrm')->initialize();
$result = civicrm_api('Contact', 'get', [
  'version' => 3,
  'email' => 'test@example.com',
]);
```

### User Synchronization
- Drupal user ↔ CiviCRM contact mapping
- User creation/update hooks
- Permission synchronization

### Permission Integration
```php
// Drupal 7
function mymodule_permission() {
  return array(
    'access mymodule feature' => array(
      'title' => t('Access MyModule Feature'),
    ),
  );
}

// Drupal 10
// In mymodule.permissions.yml
access mymodule feature:
  title: 'Access MyModule Feature'
  description: 'Allow users to access MyModule features'
```

## Code Style Guidelines

### PHP Code Standards
- Follow Drupal coding standards: https://www.drupal.org/docs/develop/standards
- **Indentation**: 2 spaces (matching project standard)
- **Function naming**:
  - Drupal 7: `modulename_function_name()`
  - Drupal 10: CamelCase for class methods
- **Comments**: Use proper DocBlocks

### Drupal 7 Specific
```php
/**
 * Implements hook_menu().
 */
function mymodule_menu() {
  // Function body
}
```

### Drupal 10 Specific
```php
<?php

namespace Drupal\mymodule;

/**
 * Class description.
 */
class MyClass {

  /**
   * Method description.
   *
   * @param string $param
   *   Parameter description.
   *
   * @return array
   *   Return value description.
   */
  public function myMethod(string $param): array {
    // Method body
  }
}
```

## Module Structure

### Drupal 7 Module Files
```
mymodule/
├── mymodule.info          - Module metadata
├── mymodule.module        - Hook implementations
├── mymodule.install       - Install/update hooks
├── mymodule.admin.inc     - Admin forms
└── includes/              - Additional includes
```

### Drupal 10 Module Files
```
mymodule/
├── mymodule.info.yml      - Module metadata
├── mymodule.routing.yml   - Route definitions
├── mymodule.services.yml  - Service definitions
├── mymodule.permissions.yml - Permissions
├── mymodule.module        - Hook implementations (if needed)
├── src/
│   ├── Controller/        - Controllers
│   ├── Form/              - Forms
│   ├── Plugin/            - Plugins
│   └── Service/           - Services
└── config/
    └── install/           - Default configuration
```

## Security Considerations

### Access Control
- Always check permissions before executing operations
- Validate user input
- Sanitize output (use `check_plain()` in D7, `Html::escape()` in D10)

### CSRF Protection
- Drupal 7: Use form API tokens
- Drupal 10: Form API handles automatically

### SQL Injection Prevention
- Always use parameterized queries
- Never concatenate user input into SQL
- Use Drupal's database abstraction layer

## Debugging

### Drupal 7
```php
drupal_set_message('Debug message');
watchdog('mymodule', 'Log message');
dpm($variable); // If Devel module installed
```

### Drupal 10
```php
\Drupal::messenger()->addMessage('Debug message');
\Drupal::logger('mymodule')->notice('Log message');
dpm($variable); // If Devel module installed
```

## Version-Specific Checklist

### Before Writing Code
1. Check current branch name (`git branch`)
2. Identify Drupal version from branch prefix (7.x-* or 10.x-*)
3. Use appropriate API and patterns for that version
4. Verify submodule paths (`/neticrm/` and `/drupal/`)

### Code Review Checklist
- [ ] Correct Drupal API version used
- [ ] Follows Drupal coding standards
- [ ] Proper error handling and validation
- [ ] Security best practices applied
- [ ] Documentation and comments included
- [ ] CiviCRM integration properly initialized
- [ ] Tested in target Drupal version

## Related Documentation
- See `/CLAUDE.md` for general development guidelines
- Use php-engineer agent for PHP development patterns
- Drupal 7 API: https://api.drupal.org/api/drupal/7.x
- Drupal 10 API: https://api.drupal.org/api/drupal/10
- CiviCRM Drupal Integration: https://docs.civicrm.org/dev/en/latest/framework/drupal/
