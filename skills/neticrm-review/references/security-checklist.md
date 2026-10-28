# Security Review Checklist

Run on every diff regardless of layer. These are the highest-risk issues.

## Permissions

| Check | What to look for | Severity |
|-------|-----------------|---------|
| Route permission | Menu XML `<access_arguments>` is present and not empty | 🔴 Critical |
| Entry-point permission | Page/Form/AJAX handler (or a BAO method used directly as `<page_callback>`) reads or writes data its route does not already restrict, with no `CRM_Core_Permission::check()` in the handler | 🔴 Critical |
| Per-record access | Handler loads a record by an ID from the request (`cid`, `id`, …) and shows or modifies it without a per-record check (`CRM_Contact_BAO_Contact_Permission::allow()`, `CRM_Contact_BAO_Contact_Utils::validChecksum()`, or an ownership check), on a route open to users without `view/edit all contacts` | 🔴 Critical |
| Permission flag disabled | Diff changes an existing permission/ACL argument so checks are skipped (e.g. passing `FALSE` to a `$checkPermission` parameter) on a user-reachable path | 🔴 Critical |
| API permission | New API entity/action exposing data that needs more than `access CiviCRM`, but not mapped in `CRM/Core/DAO/.permissions.php` or via `hook_civicrm_alterAPIPermissions` — unmapped calls fall back to `access CiviCRM` only | 🔴 Critical |
| Drupal route | `.routing.yml` `requirements._permission` is set | 🔴 Critical |

Do not flag BAO methods for lacking `CRM_Core_Permission::check()`: permissions belong at the route, Form/Page, or API layer, which runs before the BAO is called. Exceptions are the two rows above that mention BAO usage (`<page_callback>` BAO methods, disabled permission arguments).

API permissions are enforced centrally in `api/api.php` via `_civicrm_api3_api_check_permission()`, only when `$params['check_permissions']` is set (REST always sets it). `_spec()` functions declare parameters and are not a permission guard. Map keys in `.permissions.php` are lowercase with underscores (`group_contact`).

## SQL Injection

| Check | What to look for | Severity |
|-------|-----------------|---------|
| String concat in SQL | Request- or user-controlled value concatenated into SQL without `(int)` cast, fixed whitelist, or `CRM_Utils_Type::escape()` | 🔴 Critical |
| Unparameterized query | `CRM_Core_DAO::executeQuery($sql)` where `$sql` contains such a value | 🔴 Critical |
| Safe pattern | Correct: `CRM_Core_DAO::executeQuery("SELECT ... WHERE id = %1", [1 => [$id, 'Integer']])` | — |

Concatenating constants, `(int)`-cast values, or values checked against a fixed whitelist is not SQL injection. Switching such code to `%1` params is at most a 🔵 Suggestion.

## Output / XSS

| Check | What to look for | Severity |
|-------|-----------------|---------|
| Unescaped PHP output | `echo $userInput` or `print $var` without escaping | 🔴 Critical |
| Unescaped Smarty | `{$var}` for user-supplied data — must be `{$var\|escape}` | 🔴 Critical |
| HTML injection in JS | `element.innerHTML = data` or `cj(el).html(data)` where `data` contains user input — use `textContent` or `cj().text()`. Static markup is fine | 🔴 Critical |

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
