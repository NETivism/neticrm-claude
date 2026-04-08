# Entity API Summary

## Available Entities

| Entity (URL param) | Description | CRUD support |
|-------------------|-------------|--------------|
| `Contact` | Contacts (Individual / Household / Organization) | get / getcount / create / update / delete / checksum |
| `Contribution` | Donation records | get / getcount / create / update / delete |
| `Membership` | Membership records | get / getcount / create / update / delete |
| `Participant` | Event participants | get / getcount / create / update / delete |
| `Activity` | Activity / interaction records | get / create / update / delete |
| `Group` | Groups | get / create / update / delete |
| `Email` | Email addresses (nested or standalone) | get / create / update / delete |
| `Phone` | Phone numbers (nested or standalone) | get / create / update / delete |
| `Event` | Event pages | get |
| `ContributionPage` | Contribution (donation) pages | get |
| `contribution_recur` | Recurring contributions | get |
| `CustomGroup` | Custom field groups | get |
| `CustomField` | Custom field definitions | get |
| `CustomValue` | Custom field values (nested queries) | get |

---

## Contact

### Actions
| Action | Method | Required fields |
|--------|--------|-----------------|
| `get` | GET | — |
| `get` (search) | POST | — |
| `getcount` | POST | — |
| `create` (insert) | POST | `contact_type` |
| `create` (update) | POST | `id` |
| `delete` | POST | `id` |
| `checksum` | POST | `contact_id`, `live` |

Create supports inline creation of `email` / `phone` / `address` by passing arrays in the body.

Date-range search params: `contact_modified_date_low`, `contact_modified_date_high`

### Key fields
| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Required on update |
| `contact_type` | enum | `Individual`, `Household`, `Organization` — required on create |
| `first_name` / `last_name` | varchar | Individual name |
| `organization_name` | varchar | Organization name |
| `household_name` | varchar | Household name |
| `display_name` / `sort_name` | varchar | Read-only formatted names |
| `birth_date` | date | `yyyy-mm-dd` |
| `gender_id` | int | FK to option value |
| `do_not_email` / `do_not_phone` | boolean | `0` or `1` |
| `is_opt_out` | boolean | Bulk email opt-out |
| `is_deleted` | boolean | Soft-deleted flag |
| `external_identifier` | varchar | External system ID |
| `source` | varchar | Import origin |

---

## Contribution

### Actions
| Action | Method | Required fields |
|--------|--------|-----------------|
| `get` | GET | — |
| `get` (search) | POST | — |
| `getcount` | POST | — |
| `create` (insert) | POST | `contact_id`, `total_amount` |
| `create` (update) | POST | `id` |
| `delete` | POST | `id` |

Date-range search params: `contribution_date_low`, `contribution_date_low_time`, `contribution_date_high`, `contribution_date_high_time`

### Key fields
| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Required on update |
| `contact_id` | int | Required |
| `total_amount` | decimal | Required |
| `contribution_type_id` | int | FK to contribution type |
| `contribution_status_id` | int | 1=Completed, 2=Pending, 3=Cancelled, 4=Failed |
| `receive_date` | datetime | `yyyy-mm-dd hh:ii:ss` |
| `payment_instrument_id` | int | Payment method |
| `trxn_id` / `invoice_id` | varchar | Transaction / invoice identifier |
| `is_test` | boolean | Test record flag |
| `contribution_recur_id` | int | FK to recurring order |
| `source` | varchar | Origin label |

---

## Membership

### Actions
| Action | Method | Required fields |
|--------|--------|-----------------|
| `get` | GET/POST | — |
| `getcount` | POST | — |
| `create` (insert) | POST | `contact_id`, `membership_type_id`, `status_id` |
| `create` (update) | POST | `id` |
| `delete` | POST | `id` |

### Key fields
| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Required on update |
| `contact_id` | int | Required |
| `membership_type_id` | int | Required |
| `status_id` | int | Required |
| `join_date` | date | Initial membership start `yyyy-mm-dd` |
| `start_date` | date | Current period start |
| `end_date` | date | Current period expiry |
| `is_override` | boolean | Manual status override |
| `is_test` | boolean | Test record flag |

---

## Participant

### Actions
| Action | Method | Required fields |
|--------|--------|-----------------|
| `get` | GET | — |
| `getcount` | POST | — |
| `create` (insert) | POST | `contact_id`, `event_id`, `status_id` |
| `create` (update) | POST | `id` |
| `delete` | POST | `id` |

### Key fields
| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Required on update |
| `contact_id` | int | Required |
| `event_id` | int | Required |
| `status_id` | int | Required; 1=Registered |
| `role_id` | varchar | Participant role |
| `register_date` | datetime | Registration timestamp |
| `fee_amount` | decimal | Fee paid |
| `is_test` | boolean | Test record flag |

---

## Activity

### Actions
| Action | Method | Required fields |
|--------|--------|-----------------|
| `get` | GET | — |
| `create` (insert) | POST | `activity_type_id`, `target_entity_table`, `target_entity_id` |
| `create` (update) | POST | `id` |
| `delete` | POST | `id` |

### Key fields
| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Required on update |
| `activity_type_id` | int | Required; FK to option value |
| `target_entity_table` | varchar | Required; e.g. `civicrm_contact` |
| `target_entity_id` | int | Required; FK to target record |
| `source_contact_id` | int | Initiating contact |
| `subject` | varchar | Short description |
| `activity_date_time` | datetime | Scheduled datetime |
| `status_id` | int | Activity status |
| `details` | text | Notes / agenda |

---

## Email

### Actions
| Action | Method | Required fields |
|--------|--------|-----------------|
| `get` | GET | — |
| `create` (insert) | POST | `contact_id`, `email` |
| `create` (update) | POST | `id` |
| `delete` | POST | `id` |

### Key fields
| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Required on update |
| `contact_id` | int | |
| `email` | varchar | Email address |
| `location_type_id` | int | Address type |
| `is_primary` | boolean | Primary email flag |
| `on_hold` | boolean | Bounce hold status |

---

## Phone

### Actions
| Action | Method | Required fields |
|--------|--------|-----------------|
| `get` | GET | — |
| `create` (insert) | POST | `contact_id`, `phone` |
| `create` (update) | POST | `id` |
| `delete` | POST | `id` |

### Key fields
| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Required on update |
| `contact_id` | int | |
| `phone` | varchar | Full phone number |
| `phone_type_id` | int | Phone / Mobile / Fax / Pager |
| `location_type_id` | int | Address type |
| `is_primary` | boolean | Primary phone flag |

---

## Group

### Actions
| Action | Method | Required fields |
|--------|--------|-----------------|
| `get` | GET | — |
| `create` (insert) | POST | `title` |
| `create` (update) | POST | `id` |
| `delete` | POST | `id` |

### Key fields
| Field | Type | Notes |
|-------|------|-------|
| `id` | int | Required on update |
| `title` | varchar | Display name |
| `name` | varchar | Internal name |
| `description` | text | Optional description |
| `is_active` | boolean | Active flag |

---

## Event (read-only)

### Actions
| Action | Method | Notes |
|--------|--------|-------|
| `get` | GET | Fetch event page data |

Key response fields: `id`, `title`, `event_type_id`, `start_date`, `end_date`, `is_online_registration`, `registration_start_date`, `registration_end_date`, `is_public`

---

## ContributionPage (read-only)

### Actions
| Action | Method | Notes |
|--------|--------|-------|
| `get` | GET | Fetch donation page data |

---

## contribution_recur (read-only)

### Actions
| Action | Method | Notes |
|--------|--------|-------|
| `get` | GET | Fetch recurring contribution records |

### Key fields
| Field | Type | Notes |
|-------|------|-------|
| `id` | int | |
| `contact_id` | int | Required |
| `amount` | decimal | Per-cycle amount |
| `frequency_unit` | enum | `day`, `week`, `month`, `year` |
| `frequency_interval` | int | Number of units per cycle |
| `cycle_day` | int | Day within period |
| `start_date` | datetime | First charge date |
| `contribution_status_id` | int | 1=completed, 2=pending, 3=cancel, 4=failed, 5=in progress, 6=overdue, 7=suspend |
| `next_sched_contribution` | datetime | Next scheduled payment |

---

## Custom Fields

### Get custom group / field definitions
```
GET <entrypoint>?entity=CustomGroup&action=get
GET <entrypoint>?entity=CustomField&action=get
```

### Get custom field values (nested query)
```json
{
  "id": 1234,
  "api.CustomValue.get": {
    "entity_table": "civicrm_contact",
    "entity_id": "$value.id"
  }
}
```

Response shape per value: `{ "entity_id": "1234", "id": "2", "latest": "value", "0": "value" }`

---

## Field Type Reference

| XML type | Format |
|----------|--------|
| `int unsigned` | integer `>= 0` |
| `varchar` | string |
| `text` | long string |
| `boolean` | `0` or `1` |
| `date` | `yyyy-mm-dd` |
| `datetime` | `yyyy-mm-dd hh:ii:ss` |
| `decimal` | `00.00` |
| `enum` | one of listed values |

## Field Creation Rules

| Rule | Meaning |
|------|---------|
| required | Must be provided on create |
| required on update | Must be provided when `id` is present |
| default: X | Default value when not provided |

---

## Common GetOptions Fields

Request: `POST <entrypoint>?entity=<Entity>&action=getoptions` with body `{ "field": "<field_name>" }`

Response shape — `values` is an **array** of `{ value, label }` objects (not a keyed map):
```json
{
  "is_error": 0,
  "version": 3,
  "count": 3,
  "values": [
    { "value": 1, "label": "信用卡" },
    { "value": 2, "label": "簽帳卡" },
    { "value": 3, "label": "現金" }
  ]
}
```

To build a value→label lookup map:
```js
const map = {};
(result.values || []).forEach(function(opt) {
  map[String(opt.value)] = opt.label;
});
```

For `entity=Contact`:
- `contact_type` — Individual / Household / Organization
- `prefix_id`, `suffix_id` — name prefix/suffix
- `gender_id` — gender
- `location_type_id` — Home / Work / Main / Other / Billing
- `phone_type_id` — Mobile / Phone / Fax / Pager
- `country_id`, `state_province_id` — location

For `entity=Contribution`:
- `contribution_type_id` — contribution types
- `contribution_status_id` — statuses
- `payment_instrument_id` — payment methods (credit card, ATM, etc.)
- `currency` — currencies
