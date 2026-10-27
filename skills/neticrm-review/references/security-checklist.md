# Security Review Checklist

Run on every diff regardless of layer. These are the highest-risk issues.

## Permissions

| Check | What to look for | Severity |
|-------|-----------------|---------|
| Route permission | Menu XML `<access_arguments>` is present and not empty | 🔴 Critical |
| Entry-point permission | Page/Form or custom handler reads or writes data its route does not already restrict, with no `CRM_Core_Permission::check()` in the handler | 🔴 Critical |
| API permission | New API entity/action not added to `CRM/Core/DAO/.permissions.php` — unmapped calls fall back to `access CiviCRM` only | 🔴 Critical |
| Drupal route | `.routing.yml` `requirements._permission` is set | 🔴 Critical |

Do not flag BAO methods for lacking `CRM_Core_Permission::check()`. BAOs are called by trusted code (cron, IPN, API with `check_permissions` off); permissions belong at the route, Form/Page, or API layer.

API permissions are enforced centrally in `api/api.php` via `_civicrm_api3_api_check_permission()`, only when `$params['check_permissions']` is set (REST always sets it). `_spec()` functions declare parameters and are not a permission guard.

## SQL Injection

| Check | What to look for | Severity |
|-------|-----------------|---------|
| String concat in SQL | `"SELECT ... WHERE id = " . $id` pattern | 🔴 Critical |
| Unparameterized query | `CRM_Core_DAO::executeQuery($sql)` with variables inside `$sql` | 🔴 Critical |
| Safe pattern | Correct: `CRM_Core_DAO::executeQuery("SELECT ... WHERE id = %1", [1 => [$id, 'Integer']])` | — |

## Output / XSS

| Check | What to look for | Severity |
|-------|-----------------|---------|
| Unescaped PHP output | `echo $userInput` or `print $var` without escaping | 🔴 Critical |
| Unescaped Smarty | `{$var}` for user-supplied data — must be `{$var\|escape}` | 🔴 Critical |
| innerHTML assignment | JS `element.innerHTML = data` — use `textContent` or `cj().text()` | 🔴 Critical |

## Sensitive Data

| Check | What to look for | Severity |
|-------|-----------------|---------|
| API key in frontend | Site key, API key, or secrets in `.tpl` / `.js` output | 🔴 Critical |
| Credentials in code | Hardcoded passwords or tokens in PHP | 🔴 Critical |
| PII in logs | CiviCRM watchdog/log calls that include email, payment data | 🟡 Warning |

## Dangerous Operations via GET

| Check | What to look for | Severity |
|-------|-----------------|---------|
| DELETE via GET | Route that deletes/resets data accessible via GET request | 🔴 Critical |
| Batch modify via GET | Mass-update operations reachable with a link click | 🔴 Critical |
