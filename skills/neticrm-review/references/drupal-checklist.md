# Drupal Review Checklist

Applies to changes in `/neticrm/` and `/drupal/`. Always check current branch first.

## Branch Detection

```bash
git branch --show-current
# 7.x-* → Drupal 7 rules apply
# 10.x-* → Drupal 10 rules apply
```

## API Version Differences

| Feature | Drupal 7 ✅ | Drupal 10 ✅ | Common Mistake |
|---------|------------|------------|----------------|
| Translation | `t('text', ['!var' => $v])` | `$this->t('text', ['@var' => $v])` | Using `t()` in D10 class |
| Messages | `drupal_set_message()` | `\Drupal::messenger()->addStatus()` | D7 function in D10 |
| DB queries | `db_select()`, `db_query()` | Inject `$database` service | `db_select()` in D10 |
| Logging | `watchdog()` | `\Drupal::logger('module')->notice()` | D7 function in D10 |
| Escaping | `check_plain()` | `Html::escape()` | D7 function in D10 |
| Routes | `hook_menu()` in `.module` | `.routing.yml` file | Hook in D10 |
| Permissions | `hook_permission()` | `.permissions.yml` | Hook in D10 |
| Module info | `.info` (INI format) | `.info.yml` (YAML format) | Wrong format |

## CiviCRM Integration

| Check | What to look for | Severity |
|-------|-----------------|---------|
| Initialization | CiviCRM API called without prior initialization | 🔴 Critical |
| D7 pattern | `civicrm_initialize()` before `civicrm_api()` calls | 🔴 Critical |
| D10 pattern | `\Drupal::service('civicrm')->initialize()` before API calls | 🔴 Critical |

## Module Structure

| Check | Drupal 7 | Drupal 10 | Severity |
|-------|----------|-----------|---------|
| Module info format | `.info` (INI) | `.info.yml` (YAML) | 🔴 Critical |
| Route definition | `hook_menu()` | `.routing.yml` | 🔴 Critical |
| Form class | Procedural `_form()` functions | `ConfigFormBase` / `FormBase` | 🟡 Warning |
