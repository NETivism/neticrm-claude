# Test File Index

Spec files that are **committed and running in CI**. AI-generated tests in `tests/specific/` are not listed here until officially registered in CI.

Read the relevant file(s) as templates before writing a new test.

## Contact

| File | What it tests |
|------|---------------|
| `add_contact.spec.js` | Adding a new individual contact with basic fields in the backend |
| `edit_contact.spec.js` | Searching and editing a contact's basic info (name, phone, email) in the backend |
| `batch_action.spec.js` | Batch actions on contacts: merge duplicates, delete, and add to group |
| `import.spec.js` | Batch CSV import for contacts and contributions |

## Event

| File | What it tests |
|------|---------------|
| `add_event.spec.js` | Creating a new event in the backend including info, fees, and online registration settings |
| `event_register.spec.js` | Registration pages for all event types (unlimited, limited, waitlist, approval) are accessible |
| `event_normal_register.spec.js` | Standard event registration with no participant limit; verifies thank-you page redirect |
| `event_limit_approval_register.spec.js` | Event registration with participant limit and approval required; verifies full-capacity message |
| `event_limit_nowait_register.spec.js` | Event registration with participant limit and no waitlist; verifies rejection when full |
| `event_limit_wait_register.spec.js` | Event registration with participant limit and waitlist enabled |
| `event_unlimit_approval_register.spec.js` | Event registration with no participant limit but approval required |
| `event_coupon.spec.js` | Applying a discount coupon during event registration and verifying the correct fee |
| `event_participant.spec.js` | Creating a contact and editing their event participant record in the backend |

## Contribution

| File | What it tests |
|------|---------------|
| `add_contribution_page.spec.js` | Creating a new contribution page through the multi-step admin wizard (title, amounts, thank-you page) |
| `new_contribution.spec.js` | Manually adding a contribution record in the backend and verifying saved field values |
| `contribution_allpay.spec.js` | Donation payment flow via ECPay (AllPay) credit card method |
| `contribution_allpay_atm.spec.js` | Donation payment flow via ECPay (AllPay) ATM virtual account transfer |
| `contribution_allpay_barcode.spec.js` | Donation payment flow via ECPay (AllPay) convenience store barcode method |
| `contribution_spgateway.spec.js` | Donation payment flow via NewebPay (SPGateway) payment gateway |
| `contribution_booster.spec.js` | Contribution Booster dashboard links and search filter functionality |
| `donation_tax_deduction.spec.js` | Full donation tax deduction electronic filing process (Taiwan MOF format) |
| `check_membership.spec.js` | Full membership flow: create membership type and contribution page, then join via frontend |

## Mailing

| File | What it tests |
|------|---------------|
| `add_group.spec.js` | Creating a group and setting up a mailing for that group |
| `edit_mailing.spec.js` | Creating a mailing and editing its content blocks (title, paragraph, image, button) |

## Profile & Custom Data

| File | What it tests |
|------|---------------|
| `add_profile.spec.js` | Creating a CiviCRM profile with various field types and verifying frontend display |
| `custom_data.spec.js` | Creating a custom data group with various field types (text, radio, checkbox, etc.) |

## Search & Report

| File | What it tests |
|------|---------------|
| `advanced_search.spec.js` | Advanced search by contact, contribution, and membership criteria; verifies results |
| `report_check.spec.js` | Batch-visit all report pages and verify each loads without errors |

## Utility / Smoke

| File | What it tests |
|------|---------------|
| `page.spec.js` | Batch-check all admin and CiviCRM backend pages for successful loading |
| `version_check.spec.js` | Batch-check a list of sites to verify pages are reachable and responding correctly |
| `sample.spec.js` | Sample test: verify the site front page loads with the correct title |

