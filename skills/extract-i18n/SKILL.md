---
name: extract-i18n
description: "CiviCRM i18n extraction and translation workflow. Reads git diff to extract new translatable strings via AI, shows them for user confirmation, syncs remote state, AI-translates into zh_TW, verifies against existing PO/POT, then appends new entries. Use when the user says 'extract translations for #NNNNN' or '/extract-i18n NNNNN'."
---

# i18n String Extraction and Translation Workflow

## Overview

Read `git diff` from commits referencing a specific issue, extract new translatable strings by AI pattern recognition, show them for user confirmation, sync remote translations, AI-translate into Traditional Chinese (Taiwan), verify against existing `civicrm.po` / `civicrm.pot`, then append new entries to both files.

**Required input**: issue number (e.g. `45479`, without `#`). Ask the user if not provided.

**Default extraction method**: AI reads git diff directly — no external tools required. `civistrings` may be used as an alternative for large file sets if available.

---

## Step 1: Collect Changed Files from Issue Commits

```bash
ISSUE="45479"   # from user input
CIVICRMPATH=$(git -C /mnt/neticrm-10/civicrm rev-parse --show-toplevel)

# Find all commits referencing this issue across all branches
COMMITS=$(git -C "$CIVICRMPATH" log --all --oneline --grep="#${ISSUE}" | awk '{print $1}')

if [ -z "$COMMITS" ]; then
  echo "No commits found for #${ISSUE}. Check the issue number."
  exit 1
fi

echo "Commits found:"
echo "$COMMITS"

# Collect all changed translatable files (deduplicated, excluding l10n/)
FILES=$(echo "$COMMITS" | xargs -I{} git -C "$CIVICRMPATH" show --name-only --format="" {} \
  | grep -E '\.(php|tpl|module|inc|js)$' \
  | grep -v '^l10n/' \
  | sort -u)

if [ -z "$FILES" ]; then
  echo "No translatable files changed in these commits. Nothing to do."
  exit 0
fi

echo ""
echo "Changed translatable files:"
echo "$FILES"
```

---

## Step 2: AI-Based String Extraction from git diff

Read the full diff of the identified commits, extract every translatable string by recognising the patterns below, and record each string's source file and line number.

```bash
# Get the combined diff for all found commits
echo "$COMMITS" | xargs -I{} git -C "$CIVICRMPATH" show {} -- $FILES
```

### Patterns to extract

**PHP — `ts()` calls**
```php
ts('Simple string')
ts("With double quotes")
ts('With placeholder %1', [1 => $var])
ts('Multi %1 placeholders %2', [1 => $a, 2 => $b])
```

**Smarty — `{ts}` blocks**
```smarty
{ts}Simple string{/ts}
{ts 1=$var}Hello %1{/ts}
{ts escape='js'}String in JS context{/ts}
```

**JS — `ts()` / `CRM.ts()` calls**
```js
ts('Simple string')
CRM.ts('Simple string')
```

For each string found in the diff (`+` lines only — ignore removed `-` lines):
1. Record the source file path (relative to `CIVICRMPATH`) and line number for the `#:` comment.
2. Normalise multi-line strings to a single-line `msgid`.
3. Skip strings that are already present verbatim in `$CIVICRMPATH/l10n/pot/civicrm.pot`.

### Display extracted strings in POT format for user confirmation

Show each candidate entry in standard gettext format, **before any translation**:

```
#: templates/CRM/Event/Form/Registration/Register.tpl:125
msgid "Registration is currently unavailable. Please contact the website administrator for assistance."
msgstr ""

#: CRM/Contribute/Form/Contribution.php:342
msgid "Thank you for your contribution of %1."
msgstr ""
```

Ask the user: **"Are these the strings to translate? (yes / edit / skip)"**
- **yes** — continue to Step 3.
- **edit** — let the user add, remove, or correct entries, then re-confirm.
- **skip** — abort cleanly.

---

## Step 3: Sync Remote State

Pull the latest remote translations and sync the PO file.

```bash
SCRIPTS="$CIVICRMPATH/tools/scripts"

echo "=== Pulling latest translations from Transifex ==="
"$SCRIPTS/pull-translation.sh"

echo ""
echo "=== Syncing PO file ==="
"$SCRIPTS/sync-po.sh"
```

If either script exits with an error, stop and show the output to the user.

---

## Step 4: Check for Dirty / Uncommitted Work in l10n

After syncing, verify that `l10n/` has no uncommitted changes before we write new entries.

```bash
DIRTY=$(git -C "$CIVICRMPATH" status --porcelain -- l10n/)
if [ -n "$DIRTY" ]; then
  echo "Uncommitted changes detected under l10n/:"
  git -C "$CIVICRMPATH" status --short -- l10n/
fi
```

If dirty: **stop here** and tell the user:

> "There are uncommitted changes under l10n/. Please commit or stash them before continuing, then re-run the skill."

Do **not** stash or commit on the user's behalf.

---

## Step 5: AI Translation

Translate each confirmed string into **Traditional Chinese (Taiwan style)** and format as PO entries with `#:` source references.

Show a draft translation block for the user to review before writing:

```
#: templates/CRM/Event/Form/Registration/Register.tpl:125
msgid "Registration is currently unavailable. Please contact the website administrator for assistance."
msgstr "報名功能目前無法使用，請聯繫網站管理員以取得協助。"

#: CRM/Contribute/Form/Contribution.php:342
msgid "Thank you for your contribution of %1."
msgstr "感謝您捐款 %1。"
```

### Translation Rules (zh_TW)

| Rule | Detail |
|------|--------|
| Taiwan vocabulary | 「儲存」not 「保存」; 「取消」not 「撤銷」; 「設定」not 「設置」 |
| Placeholders | Keep `%1`, `%2` exactly; reorder for natural Chinese word order |
| HTML tags | Keep `<a>`, `<strong>` etc. verbatim; translate text only |
| Proper nouns | CiviCRM, Drupal, Transifex — do not translate |
| Tone | Concise UI language; error messages phrased for end-users |
| Uncertain strings | Leave `msgstr ""` and flag for manual review |

**Common glossary**:

| English | zh_TW |
|---------|-------|
| Save / Update | 儲存 |
| Cancel | 取消 |
| Delete | 刪除 |
| Edit | 編輯 |
| Submit | 送出 |
| Search | 搜尋 |
| Filter | 篩選 |
| Export | 匯出 |
| Import | 匯入 |
| Error | 錯誤 |
| Warning | 警告 |
| Success | 成功 |
| Required | 必填 |
| Optional | 選填 |
| Contact | 聯絡人 |
| Contribution | 捐款 |
| Event | 活動 |
| Member | 會員 |
| Email | 電子郵件 |
| Phone | 電話 |
| Address | 地址 |
| Date | 日期 |
| Amount | 金額 |
| Status | 狀態 |
| Configuration | 設定 |
| Dashboard | 儀表板 |
| Pending | 待處理 |
| Completed | 已完成 |
| Failed | 失敗 |
| Report | 報表 |
| Profile | 個人資料 |
| Permission | 權限 |
| Click here | 點擊此處 |
| Please select | 請選擇 |
| No results found | 找不到結果 |

Ask the user to verify the translations. Let them correct any entry before proceeding.

---

## Step 6: Verify — No Duplicates in Existing PO / POT

Before writing, confirm each string is genuinely new and not already translated.

```bash
POT_FILE="$CIVICRMPATH/l10n/pot/civicrm.pot"
PO_FILE="$CIVICRMPATH/l10n/zh_TW/civicrm.po"

# Build a temporary PO that contains ONLY the new entries (with translations from Step 5)
TEMP_NEW=$(mktemp --suffix=.po)
# ... write the new entries to $TEMP_NEW ...

# Merge into the existing POT to detect collisions
TEMP_MERGED=$(mktemp --suffix=.po)
msgmerge --no-fuzzy-matching --quiet "$TEMP_NEW" "$POT_FILE" -o "$TEMP_MERGED" 2>/dev/null

# Strings that msgmerge marks obsolete were already in POT — skip them
ALREADY_IN_POT=$(msgattrib --only-obsolete "$TEMP_MERGED" \
  | grep '^#~ msgid "' | grep -v '^#~ msgid ""$' \
  | sed 's/^#~ msgid "//; s/"$//')

# Strings already translated in PO
ALREADY_IN_PO=$(grep -F 'msgid "' "$PO_FILE" \
  | grep -v '^msgid ""$' \
  | sed 's/^msgid "//; s/"$//')

rm -f "$TEMP_MERGED" "$TEMP_NEW"
```

If any string is already present in the POT or has a non-empty `msgstr` in the PO, **skip it** and report it to the user:

> "The following strings are already covered and will be skipped: ..."

Only truly new, untranslated strings proceed to Step 7.

---

## Step 7: Append New Entries to civicrm.pot and civicrm.po

Write the verified entries to both files — POT first (source-of-truth), then PO (with translations).

```bash
POT_FILE="$CIVICRMPATH/l10n/pot/civicrm.pot"
PO_FILE="$CIVICRMPATH/l10n/zh_TW/civicrm.po"

# Append to POT (msgstr always empty in POT)
for entry in "${NEW_ENTRIES[@]}"; do
  printf '\n%s\nmsgid "%s"\nmsgstr ""\n' "$sources" "$escaped_msgid" >> "$POT_FILE"
done

# Append to PO (with translated msgstr)
for entry in "${NEW_ENTRIES[@]}"; do
  printf '\n%s\nmsgid "%s"\nmsgstr "%s"\n' "$sources" "$escaped_msgid" "$escaped_msgstr" >> "$PO_FILE"
done

# Regenerate MO binary
echo "Regenerating MO file ..."
msgfmt "$PO_FILE" -o "$CIVICRMPATH/l10n/zh_TW/LC_MESSAGES/civicrm.mo"
echo "Done."

# Stage both files
git -C "$CIVICRMPATH" add "$POT_FILE" "$PO_FILE"
git -C "$CIVICRMPATH" status
```

Do **not** push to Transifex — strings will be reviewed by a human before pushing.

---

## Step 8: Summary — Ask User to Verify

Show a compact summary:

```
=== i18n Extraction Summary ===
Issue:           #45479
Commits:         3
Files scanned:   5
Strings found:   8
Already in POT:  3  (skipped)
New strings:     5

Added to civicrm.pot:
  - "Registration is currently unavailable. ..."
  - "Thank you for your contribution of %1."
  - ...

Translated in civicrm.po (zh_TW):
  - "報名功能目前無法使用，請聯繫網站管理員以取得協助。"
  - "感謝您捐款 %1。"
  - ...

Files staged:
  l10n/pot/civicrm.pot
  l10n/zh_TW/civicrm.po

Please review the changes with `git diff --staged`, then commit when ready.
```

---

## Alternative: civistrings (for large file sets)

If `civistrings` is available and the changed file set is large (> 20 files), it may be faster to run it instead of AI extraction in Step 2:

```bash
which civistrings || ls /home/jimmy/bin/civistrings

EXTRACTED_POT=$(mktemp --suffix=.pot)
echo "$FILES" | sed "s|^|$CIVICRMPATH/|" \
  | civistrings --base="$CIVICRMPATH" -o "$EXTRACTED_POT" -

echo "Extracted: $(grep -c '^msgid "' "$EXTRACTED_POT") entries"
```

Then compare `$EXTRACTED_POT` against `civicrm.pot` to find new strings, and continue from Step 5 onwards.

---

## FAQ

**sync-po.sh shows orphaned strings — what do I do?**
Orphaned strings exist in the remote PO but not in the local POT (usually legacy entries). Show the list to the user, explain each one, and proceed only after they confirm.

**String contains HTML — how to translate?**
Keep HTML tags verbatim. Example: `Click <a href="%1">here</a>` → `點擊<a href="%1">此處</a>`

**Multi-line msgid — how to handle?**
Normalise to a single-line string for the msgid; translate the whole sentence as one unit.

**A string appears in multiple files — what goes in `#:`?**
List all source references on the same `#:` line, space-separated.
