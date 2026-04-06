# netiCRM API Authentication

## Key Types

| Key | Header name | Source |
|-----|-------------|--------|
| API Secret Key | `x-civicrm-api-key` | Set by netiCRM support; stored on the contact record |
| Site Key | `x-civicrm-site-key` | Find at: Settings > Global Settings > CiviCRM Private Key |


## Header Format

```
x-civicrm-api-key: <secret-key>
x-civicrm-site-key: <site-key>
```

## curl Example

```bash
curl -g \
  --header 'x-civicrm-api-key: <secret-key>' \
  --header 'x-civicrm-site-key: <site-key>' \
  --header 'content-type: application/json' \
  --request POST \
  --data '{}' \
  '<entrypoint>?entity=Contact&action=get'
```

## Permissions

- API permissions match the site user role linked to the contact
- Permissions admin page: `https://<site-domain>/admin/people/permissions`
- Accessing the API Explorer requires the `administer CiviCRM` permission

## API Limits

| Limit | Details |
|-------|---------|
| Rate limit | At least 0.5s between requests; excessive calls will auto-block the IP |
| Records per request | Default 25; maximum 100 (via `options.limit`) |
