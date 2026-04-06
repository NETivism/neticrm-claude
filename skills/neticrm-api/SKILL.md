---
name: neticrm-api
description: "netiCRM API v3 documentation standards. Use when writing, updating, or reviewing API documentation for netiCRM entities in content/3/. Covers entity actions (get/search/getcount/create/update/delete), request/response format, authentication, pagination, nested queries, and curl examples."
---

# netiCRM API v3

## Overview

netiCRM API v3 is a unified data access interface that supports two calling methods:

| Method | Entry point | Input | Output |
|--------|-------------|-------|--------|
| **REST** | HTTP `<entrypoint>?entity=...&action=...` | URL params / JSON body | JSON |
| **PHP** | `civicrm_api3($entity, $action, $params)` | PHP array | PHP array |

Entity, action, and field names are **identical** — only the transport differs.

### Section template
```markdown
## {Entity} {Action} API

{Description}

### Request Example

#### HTTP Method
\```
POST
\```

#### Request Content Type
\```
application/json
\```

#### Request URL
\```
<entrypoint>?entity={Entity}&action={action}
\```

#### Request Body
\```json
{ ... }
\```

#### curl Example
\```bash
curl -g \
  --header 'x-civicrm-api-key: <secret-key>' \
  --header 'x-civicrm-site-key: <site-key>' \
  --header 'content-type: application/json' \
  --request POST \
  --data '{...}' \
  '<entrypoint>?entity={Entity}&action={action}'
\```

### Response Example
\```json
{ ... }
\```
```

## Core API Patterns

### Action to HTTP Method mapping
| Action | HTTP Method | Notes |
|--------|-------------|-------|
| `get` | GET | Fetch one or many; pass `json` as URL param |
| `get` (search) | POST | Body is JSON matching backend search params |
| `getcount` | POST | Same params as search; returns `{"is_error":0,"result":N}` |
| `create` (insert) | POST | Body is JSON, **no** `id` field |
| `create` (update) | POST | Body includes `"id"` field |
| `delete` | POST | Body only needs `{"id": N}` |
| `getoptions` | GET | Fetch option list for a field |
| `checksum` | POST | Contact only; generates CS link |

### URL format
```
<entrypoint>?entity=<EntityName>&action=<action>
```
- GET with filter: `&json={"field":"value"}`
- GET all: `&json={}` or omit json entirely

### Required auth headers
```
x-civicrm-api-key: <secret-key>
x-civicrm-site-key: <site-key>
```

## Response Format

### Success (get / create / update)
```json
{
    "is_error": 0,
    "version": 3,
    "count": 1,
    "id": 123,
    "values": [ { ... } ]
}
```

### Success (getcount)
```json
{
    "is_error": 0,
    "result": 50
}
```

### Success (delete)
```json
{
    "is_error": 0,
    "version": 3,
    "count": 1,
    "values": 1
}
```

## References

- **Authentication**: See [authentication.md](references/authentication.md) — key setup flow, header format, permissions (REST)
- **Request & Response**: See [request-response.md](references/request-response.md) — pagination, sorting, filtering, nested queries, curl notes (REST)
- **Entities**: See [entities.md](references/entities.md) — supported actions and required fields per entity
- **PHP API**: See [php-api.md](references/php-api.md) — internal PHP calls (civicrm_api3), implementing API endpoints, spec functions, return value format
