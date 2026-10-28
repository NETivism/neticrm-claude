# Drupal Review Checklist

Applies to changes in `/neticrm/`, `/drupal/`, and `$NETICRMP`. Detect the Drupal version first.

## Drupal Version Detection

The parent repo branch (`hotfix`, `develop`, …) does not encode the Drupal version; the `drupal` submodule branch does.

```bash
git -C $DRUPAL branch --show-current
# 7.x-*  → Drupal 7 rules apply
# 10.x-* → Drupal 10 rules apply
# empty (detached HEAD) → $DRUPAL/civicrm.info.yml exists = D10, $DRUPAL/civicrm.info exists = D7
```

If a reviewed submodule or `$NETICRMP` commit is not in the current checkout (`git -C <repo> merge-base --is-ancestor <hash> HEAD` fails), the commit may belong to the other Drupal version — ask the user which version applies instead of guessing.

Parent repo code (`CRM/`, `api/`, `templates/`) is shared by both versions: do not apply the Drupal API rules below to it.

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
| Initialization | CiviCRM API or `CRM_*` classes used without prior initialization (not required in `neticrm_update/update/*.inc` — see `database-checklist.md`) | 🔴 Critical |

Both `civicrm_initialize()` and `\Drupal::service('civicrm')->initialize()` are valid on D10 — the former is a wrapper defined in `drupal/civicrm.module`. D7 only has `civicrm_initialize()`.

## Module Structure

| Check | Drupal 7 | Drupal 10 | Severity |
|-------|----------|-----------|---------|
| Module info format | `.info` (INI) | `.info.yml` (YAML) | 🔴 Critical |
| Route definition | `hook_menu()` | `.routing.yml` | 🔴 Critical |
| Form class | Procedural `_form()` functions | `ConfigFormBase` / `FormBase` | 🟡 Warning |
