# Security Review Checklist

Run on every diff regardless of layer. These are the highest-risk issues.

## Permissions

| Check | What to look for | Severity |
|-------|-----------------|---------|
| Route permission | Menu XML `<access_arguments>` is present and not empty | 🔴 Critical |
| BAO permission | Data retrieval/modification in BAO without `CRM_Core_Permission::check()` | 🔴 Critical |
| API permission | API endpoint exposes data without `_spec()` / `$spec['check_permissions']` guard | 🔴 Critical |
| Drupal route | `.routing.yml` `requirements._permission` is set | 🔴 Critical |

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
