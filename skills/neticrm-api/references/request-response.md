# Request & Response Patterns

## Search (POST, recommended)

POST with `Content-Type: application/json` is the standard way to query data.
The request body accepts the same filter parameters as the backend search UI.

```bash
curl -g \
  --header 'x-civicrm-api-key: <secret-key>' \
  --header 'x-civicrm-site-key: <site-key>' \
  --header 'content-type: application/json' \
  --request POST \
  --data '{"contact_modified_date_low":"2025-01-01","last_name":"王"}' \
  '<entrypoint>?entity=Contact&action=get'
```

Fetch all records (no filter):
```bash
curl -g \
  --header 'x-civicrm-api-key: <secret-key>' \
  --header 'x-civicrm-site-key: <site-key>' \
  --header 'content-type: application/json' \
  --request POST \
  --data '{}' \
  '<entrypoint>?entity=Contact&action=get'
```

## GET queries (simple lookups)

GET is suitable for single-record lookups by ID. Use POST for anything more complex.

```bash
# Fetch contact by ID
curl -g \
  --header 'x-civicrm-api-key: <secret-key>' \
  --header 'x-civicrm-site-key: <site-key>' \
  --header 'content-type: application/json' \
  --request POST \
  --data '{"id":"1234"}' \
  '<entrypoint>?entity=Contact&action=get'
```

## Pagination

Maximum 100 records per request; default is 25. Pass `options` in the POST body:

```bash
# Records 1-100
curl -g \
  --header 'x-civicrm-api-key: <secret-key>' \
  --header 'x-civicrm-site-key: <site-key>' \
  --header 'content-type: application/json' \
  --request POST \
  --data '{"options":{"limit":100,"offset":0}}' \
  '<entrypoint>?entity=Contact&action=get'

# Records 101-200
curl -g \
  --header 'x-civicrm-api-key: <secret-key>' \
  --header 'x-civicrm-site-key: <site-key>' \
  --header 'content-type: application/json' \
  --request POST \
  --data '{"options":{"limit":100,"offset":100}}' \
  '<entrypoint>?entity=Contact&action=get'
```

When all data has been returned, `values` will be an empty array.

## Sorting

Pass `options.sort` in the POST body with `asc` or `desc`:

```bash
# Contributions ranked 101-200 by amount, status=completed
curl -g \
  --header 'x-civicrm-api-key: <secret-key>' \
  --header 'x-civicrm-site-key: <site-key>' \
  --header 'content-type: application/json' \
  --request POST \
  --data '{"contribution_status_id":1,"options":{"sort":"total_amount desc","limit":100,"offset":100}}' \
  '<entrypoint>?entity=Contribution&action=get'
```

Common sort fields: `created_date`, `receive_date`, `total_amount`

## Nested Queries

Fetch related entity data in a single request using `api.<RelatedEntity>.get`.
Use POST so the JSON body doesn't need to be URL-encoded:

```bash
curl -g \
  --header 'x-civicrm-api-key: <secret-key>' \
  --header 'x-civicrm-site-key: <site-key>' \
  --header 'content-type: application/json' \
  --request POST \
  --data '{
    "id": 1234,
    "api.Email.get": {"contact_id": "$value.id"},
    "api.Phone.get": {"contact_id": "$value.id"},
    "api.CustomValue.get": {"entity_table": "civicrm_contact", "entity_id": "$value.id"}
  }' \
  '<entrypoint>?entity=Contact&action=get'
```

`$value.id` references the `id` from the parent query result.

## GetCount API

Returns the total number of matching records. Accepts the same params as the search POST body:

```bash
curl -g \
  --header 'x-civicrm-api-key: <secret-key>' \
  --header 'x-civicrm-site-key: <site-key>' \
  --header 'content-type: application/json' \
  --request POST \
  --data '{"contribution_date_low":"2024-01-01","contribution_date_high":"2024-12-31"}' \
  '<entrypoint>?entity=Contribution&action=getcount'
```

Response:
```json
{
    "is_error": 0,
    "result": 50
}
```

## Get Options API

Fetch the option list for a field (useful for `_id` suffix fields):

```bash
curl -g \
  --header 'x-civicrm-api-key: <secret-key>' \
  --header 'x-civicrm-site-key: <site-key>' \
  --header 'content-type: application/json' \
  --request POST \
  --data '{"field":"contribution_status_id"}' \
  '<entrypoint>?entity=Contribution&action=getoptions'
```

Response:
```json
{
    "is_error": 0,
    "version": 3,
    "count": 4,
    "values": [
        {"value": 1, "label": "已完成"},
        {"value": 2, "label": "待處理"}
    ]
}
```

## Pretty-printed response

Add `pretty=1` to the URL to get formatted JSON output (useful during development):
```
<entrypoint>?entity=Contact&action=get&pretty=1
```

## Contact Checksum API

Generates a CS (Contact Checksum) so users can click a link and have their contact data pre-filled:

```bash
curl -g \
  --header 'x-civicrm-api-key: <secret-key>' \
  --header 'x-civicrm-site-key: <site-key>' \
  --header 'content-type: application/json' \
  --request POST \
  --data '{"contact_id":1234,"live":3}' \
  '<entrypoint>?entity=Contact&action=checksum'
```

- `contact_id`: the contact's ID
- `live`: validity period in hours (max 360)

Use the returned checksum with `cid` on a contribution or event registration page:
```
https://<site-domain>/civicrm/contribute/transact?reset=1&id=<page_id>&cs=<checksum>&cid=<contact_id>
```
