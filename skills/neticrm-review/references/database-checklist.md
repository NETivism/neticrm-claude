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
| Existence guard | `ADD COLUMN`, `ADD INDEX`/`ADD CONSTRAINT`, `DROP ...`, `RENAME`, `CHANGE COLUMN` that renames, or `CREATE TABLE` without an existence check — re-running the update fails | 🔴 Critical |
| Schema filter | `INFORMATION_SCHEMA` query without `table_schema = DATABASE()` — may match the same table in another database on the server | 🟡 Warning |
| Static call | `CRM_Core_DAO::checkTableExists()` / `checkConstraintExists()` called statically — they are non-static and fatal on PHP 8 | 🔴 Critical |
| Sequential number | `neticrm_xNNN.inc` — confirm NNN is next after highest existing file | 🟡 Warning |
| Function name | `_neticrm_update_update_xNNN()` matches filename number | 🟡 Warning |

Accepted existence checks: `SHOW COLUMNS/TABLES/INDEX ... LIKE`, an `INFORMATION_SCHEMA` query, `CRM_Core_DAO::checkFieldExists()` (static), `CREATE TABLE IF NOT EXISTS`, `DROP ... IF EXISTS`.

Do not flag `MODIFY COLUMN`, or `CHANGE COLUMN` keeping the same name, that restates the full column definition: re-running it gives the same result.

Do not flag a missing `civicrm_initialize()` in update functions: `neticrm_update_load_include()` in `neticrm_update.install` already calls it before loading each update file.

## Table Definitions

| Check | What to look for | Severity |
|-------|-----------------|---------|
| Engine & charset | `ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC` | 🟡 Warning |
| Auto-increment PK | Primary key named `id`, type `int unsigned NOT NULL AUTO_INCREMENT` | 🟡 Warning |
| Column comments | Each column has a `COMMENT '...'` describing its purpose | 🔵 Suggestion |
