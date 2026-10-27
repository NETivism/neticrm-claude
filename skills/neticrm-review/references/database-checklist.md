# Database Review Checklist

Applies to changes in `/xml/schema/`, `/CRM/**/DAO/`, `/neticrm/neticrm_update/update/`, `/sql/*.mysql`.

## Schema & DAO

| Check | What to look for | Severity |
|-------|-----------------|---------|
| DAO not hand-edited | Manual edits inside `/CRM/**/DAO/` files | 🔴 Critical |
| GenCode run | XML schema changed but no corresponding DAO update | 🔴 Critical |
| Commit together | XML + DAO + migration committed in separate commits | 🟡 Warning |
| XML location | Schema file in `/xml/schema/{Module}/{TableName}.xml` (CamelCase) | 🟡 Warning |

## Migration Scripts

| Check | What to look for | Severity |
|-------|-----------------|---------|
| Idempotent guard | `ALTER TABLE` without prior `SHOW COLUMNS ... LIKE '...'` check | 🔴 Critical |
| Create table guard | `CREATE TABLE` without prior `SHOW TABLES LIKE '...'` check | 🔴 Critical |
| Sequential number | `neticrm_xNNN.inc` — confirm NNN is next after highest existing file | 🟡 Warning |
| Function name | `_neticrm_update_update_xNNN()` matches filename number | 🟡 Warning |

Do not flag a missing `civicrm_initialize()` in update functions: `neticrm_update_load_include()` in `neticrm_update.install` already calls it before loading each update file.

## Table Definitions

| Check | What to look for | Severity |
|-------|-----------------|---------|
| Engine & charset | `ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC` | 🟡 Warning |
| Auto-increment PK | Primary key named `id`, type `int unsigned NOT NULL AUTO_INCREMENT` | 🟡 Warning |
| Column comments | Each column has a `COMMENT '...'` describing its purpose | 🔵 Suggestion |
