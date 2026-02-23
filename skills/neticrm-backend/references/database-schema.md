# Database Schema — netiCRM/CiviCRM

## Ground Truth

This file documents XML schema conventions and migration patterns verified against actual code.

| Topic | Source |
|-------|--------|
| Schema XML examples | `/xml/schema/Contribute/ContributionProduct.xml`, `Contribution.xml` |
| Membership with uniqueName | `/xml/schema/Member/Membership.xml` |
| Email with simple FK | `/xml/schema/Core/Email.xml` |
| Recent update scripts | `/neticrm/neticrm_update/update/neticrm_x326.inc`, `neticrm_x329.inc` |

> Verified against codebase: 2026-02.

---

## Table of Contents
1. [Path Lookup](#1-path-lookup)
2. [XML Schema Structure](#2-xml-schema-structure)
3. [Field Types & Attributes](#3-field-types--attributes)
4. [Common Field Patterns](#4-common-field-patterns)
5. [Indexes](#5-indexes)
6. [Foreign Keys](#6-foreign-keys)
7. [Naming Conventions](#7-naming-conventions)
8. [Table-level Attributes](#8-table-level-attributes)

---

## 1. Path Lookup

| To find | Method |
|---------|--------|
| XML schema | Table `civicrm_contribution_product` → `/xml/schema/Contribute/ContributionProduct.xml` (CamelCase, drop `civicrm_` prefix) |
| DAO class | Table `civicrm_contribution_product` → `/CRM/Contribute/DAO/ContributionProduct.php` |
| SQL seed files | Use `*.mysql` extension: `/sql/civicrm.mysql`, `/sql/civicrm_data.mysql` |
| Update scripts | `/neticrm/neticrm_update/update/neticrm_xNNN.inc` (newer) or `/update/NNNN.inc` (older) |

**Class-to-file mapping:**
```
CRM_Contribute_DAO_ContributionProduct → /CRM/Contribute/DAO/ContributionProduct.php
CRM_Member_DAO_Membership              → /CRM/Member/DAO/Membership.php
```

---

## 2. XML Schema Structure

Minimal complete example:

```xml
<?xml version="1.0" encoding="iso-8859-1" ?>

<table>
  <base>CRM/Contribute</base>
  <class>ContributionProduct</class>
  <name>civicrm_contribution_product</name>
  <comment>Links contributions to products (premiums).</comment>
  <add>1.4</add>
  <log>true</log>

  <!-- Primary key — always id, always auto-increment -->
  <field>
    <name>id</name>
    <type>int unsigned</type>
    <required>true</required>
    <add>1.4</add>
  </field>
  <primaryKey>
    <name>id</name>
    <autoincrement>true</autoincrement>
  </primaryKey>

  <!-- Foreign key field + declaration -->
  <field>
    <name>contribution_id</name>
    <type>int unsigned</type>
    <required>true</required>
    <comment>FK to civicrm_contribution</comment>
    <add>1.4</add>
  </field>
  <foreignKey>
    <name>contribution_id</name>
    <table>civicrm_contribution</table>
    <key>id</key>
    <onDelete>CASCADE</onDelete>
    <add>1.4</add>
  </foreignKey>

  <!-- Regular string field -->
  <field>
    <name>product_option</name>
    <title>Product Option</title>
    <type>varchar</type>
    <length>255</length>
    <export>true</export>
    <comment>Option value selected, e.g. color or size.</comment>
    <add>1.4</add>
  </field>

  <!-- Boolean field -->
  <field>
    <name>restock</name>
    <type>boolean</type>
    <default>0</default>
    <export>true</export>
    <comment>Indicates if contribution product has been restocked.</comment>
    <add>1.4</add>
  </field>

  <!-- Index -->
  <index>
    <name>idx_contribution_id</name>
    <fieldName>contribution_id</fieldName>
    <add>1.4</add>
  </index>
</table>
```

**Required top-level elements:**

| Element | Purpose | Example |
|---------|---------|---------|
| `<base>` | Namespace path for generated class | `CRM/Contribute` |
| `<class>` | Class name (CamelCase, no prefix) | `ContributionProduct` |
| `<name>` | Actual table name | `civicrm_contribution_product` |
| `<add>` | CiviCRM version when added | `1.4` |

---

## 3. Field Types & Attributes

### Supported types

| XML type | MySQL column | Notes |
|----------|-------------|-------|
| `int unsigned` | `int unsigned` | Use for IDs and counts |
| `int` | `int` | Use for signed integers |
| `varchar` | `varchar(N)` | Requires `<length>` |
| `text` | `text` | Long strings, no length needed |
| `datetime` | `datetime` | `YYYY-MM-DD HH:MM:SS` |
| `date` | `date` | `YYYY-MM-DD` only |
| `timestamp` | `timestamp` | Auto `CURRENT_TIMESTAMP` patterns |
| `boolean` | `tinyint(4)` | Always set `<default>0</default>` |
| `decimal` | `decimal(20,2)` | Currency/money amounts |

### Field attributes

| Attribute | Purpose |
|-----------|---------|
| `<name>` | Column name (snake_case) |
| `<type>` | Data type (see table above) |
| `<length>` | Required for `varchar` |
| `<required>` | `true` → NOT NULL |
| `<default>` | Default value |
| `<comment>` | Column comment in DB |
| `<title>` | Human-readable label (used in UI) |
| `<uniqueName>` | Disambiguated name for import/API when same field name exists on multiple tables |
| `<add>` | Version field was added |
| `<drop>` | Version field was removed (marks deprecated field) |
| `<change>` | Version field was altered |
| `<export>` | `true` → included in CSV export |
| `<import>` | `true` → available for CSV import |
| `<usage>System</usage>` | Marks internal system fields |
| `<headerPattern>` | Regex for matching CSV header during import |
| `<dataPattern>` | Regex for validating import data |

### uniqueName — when to use

Used when the same logical field exists on multiple tables and would collide in API or import contexts:

```xml
<!-- civicrm_membership: id field has uniqueName to distinguish from other table IDs -->
<field>
  <name>id</name>
  <uniqueName>membership_id</uniqueName>
  <type>int unsigned</type>
  ...
</field>

<!-- start_date is common — uniqueName prevents collision with contribution_start_date -->
<field>
  <name>start_date</name>
  <uniqueName>membership_start_date</uniqueName>
  <type>date</type>
  ...
</field>
```

---

## 4. Common Field Patterns

### Timestamp fields
```xml
<!-- Created date: set once on INSERT -->
<field>
  <name>created_date</name>
  <type>datetime</type>
  <comment>When this record was created.</comment>
  <add>1.0</add>
</field>

<!-- Modified date: auto-update on every change -->
<field>
  <name>modified_date</name>
  <type>timestamp</type>
  <default>CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP</default>
  <comment>When this record was last modified.</comment>
  <add>1.0</add>
</field>
```

In update scripts (raw SQL), the same pattern:
```sql
`created_date`  datetime  NOT NULL DEFAULT CURRENT_TIMESTAMP,
`modified_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

### Boolean flag fields
```xml
<field>
  <name>is_active</name>
  <type>boolean</type>
  <default>1</default>
  <comment>Is this record active?</comment>
  <add>1.0</add>
</field>
```

Boolean fields always have a `<default>` (0 or 1). Naming convention: `is_*` prefix.

### Decimal / money fields
```xml
<field>
  <name>total_amount</name>
  <type>decimal</type>
  <required>true</required>
  <comment>Total amount of this contribution.</comment>
  <add>1.3</add>
</field>
```

GenCode generates `decimal(20,2)` for `<type>decimal</type>`.

### Self-referencing FK (same table)
```xml
<!-- civicrm_membership: optional parent membership -->
<field>
  <name>owner_membership_id</name>
  <type>int unsigned</type>
  <comment>Optional FK to parent membership record.</comment>
  <add>1.7</add>
</field>
<foreignKey>
  <name>owner_membership_id</name>
  <table>civicrm_membership</table>
  <key>id</key>
  <onDelete>SET NULL</onDelete>
  <add>1.7</add>
</foreignKey>
```

---

## 5. Indexes

### Regular index
```xml
<index>
  <name>index_contact_type</name>
  <fieldName>contact_type</fieldName>
  <add>2.1</add>
</index>
```

### Unique index
```xml
<!-- UI_ prefix = Unique Index convention -->
<index>
  <name>UI_contrib_trxn_id</name>
  <fieldName>trxn_id</fieldName>
  <unique>true</unique>
  <add>2.1</add>
</index>
```

### Multi-column index
```xml
<!-- ML_ prefix = Multi-column index seen in practice -->
<index>
  <name>ML_contribution</name>
  <fieldName>contact_id</fieldName>
  <fieldName>contribution_status_id</fieldName>
  <fieldName>receive_date</fieldName>
  <add>4.0</add>
</index>
```

### Index naming summary

| Prefix | Meaning | Example |
|--------|---------|---------|
| `index_` | Regular index | `index_contact_type` |
| `idx_` | Regular index (alternative) | `idx_contribution_id` |
| `UI_` | Unique index | `UI_contrib_trxn_id` |
| `ML_` | Multi-column index | `ML_contribution` |

---

## 6. Foreign Keys

### XML declaration
```xml
<foreignKey>
  <name>contact_id</name>           <!-- must match the field <name> -->
  <table>civicrm_contact</table>    <!-- referenced table -->
  <key>id</key>                     <!-- referenced column (always id) -->
  <onDelete>CASCADE</onDelete>
  <add>1.3</add>
</foreignKey>
```

### onDelete options

| Value | Behavior | When to use |
|-------|----------|-------------|
| `CASCADE` | Delete child rows when parent is deleted | Child has no meaning without parent |
| `SET NULL` | Set FK to NULL when parent is deleted | Child can exist independently |
| `RESTRICT` | Prevent parent deletion if children exist | Rarely used explicitly; DB default |

**Guideline:** Required FK (contact, contribution) → `CASCADE`. Optional FK → `SET NULL`.

### FK constraint naming in raw SQL (update scripts)
```sql
CONSTRAINT `FK_civicrm_premiums_combination_premiums_id`
  FOREIGN KEY (`premiums_id`) REFERENCES `civicrm_premiums` (`id`) ON DELETE CASCADE
```
Pattern: `FK_civicrm_{child_table_without_prefix}_{field_name}`

---

## 7. Naming Conventions

| Element | Pattern | Example |
|---------|---------|---------|
| Table | `civicrm_{module}_{entity}` | `civicrm_contribution_product` |
| Primary key | always `id` | — |
| Foreign key field | `{referenced_entity}_id` | `contribution_id`, `contact_id` |
| Boolean field | `is_{state}` | `is_active`, `is_test`, `is_pay_later` |
| Regular index | `index_{field}` or `idx_{field}` | `index_contact_type` |
| Unique index | `UI_{field}` | `UI_contrib_trxn_id` |
| Multi-column index | `ML_{table_short}` | `ML_contribution` |
| FK constraint (SQL) | `FK_civicrm_{table}_{field}` | `FK_civicrm_premiums_combination_premiums_id` |
| Schema XML file | CamelCase class name | `ContributionProduct.xml` |

---

## 8. Table-level Attributes

### `<log>true</log>`

Enables CiviCRM's built-in activity logging for this table. When set, changes are tracked in the log database automatically. Most core tables have this enabled.

```xml
<table>
  <base>CRM/Contribute</base>
  <class>Contribution</class>
  <name>civicrm_contribution</name>
  <add>1.3</add>
  <log>true</log>   <!-- enables change logging -->
  ...
</table>
```

Enable for: tables that store important business records (contributions, memberships, contacts).
Skip for: pure lookup/config tables where change history is not needed.

### Technical requirements

- **Engine**: `InnoDB` (required for foreign key constraints)
- **Character set**: `utf8mb4` with `utf8mb4_unicode_ci` collation
- **ROW_FORMAT**: `DYNAMIC` (required in update scripts for large varchar/text fields)

```sql
-- Standard CREATE TABLE footer in update scripts
ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC
```
