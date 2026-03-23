---
name: extract-i18n
description: "CiviCRM i18n extraction and translation workflow. Find changed files from issue-related commits, extract new strings with civistrings, sync Transifex, and auto-translate to zh_TW (Taiwan). Use when the user says 'extract translations for #NNNNN' or '/extract-i18n NNNNN'."
---

# i18n String Extraction and Translation Workflow

## Overview

Find all files changed by commits referencing a specific issue, extract new translatable strings using `civistrings`, sync with Transifex, and auto-translate into Traditional Chinese (Taiwan).

**Required input**: issue number (e.g. `45479`, without `#`). Ask the user if not provided.

---

## Pre-flight Checks

```bash
# civistrings — primary extraction tool (at /home/jimmy/bin/civistrings or in PATH)
which civistrings || ls /home/jimmy/bin/civistrings

# gettext tools
which msgmerge msgattrib msgfmt

# Transifex CLI
which tx
```

If `civistrings` is unavailable, fall back to the AI-based extraction described in the **Fallback** section below.

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

Show the commit and file list to the user and confirm before proceeding.

---

## Step 2: Sync Remote State (Pull Before Modifying)

**Always pull the latest remote state before making any local changes.**

```bash
SCRIPTS="$CIVICRMPATH/tools/scripts"

echo "=== Pulling latest translations from Transifex ==="
"$SCRIPTS/pull-translation.sh"

echo ""
echo "=== Checking local POT vs remote PO (sync-pot) ==="
"$SCRIPTS/sync-pot.sh"
```

`sync-pot.sh` prompts `[y/N]` when it finds orphaned msgids. If it does, explain the listed strings to the user and ask whether to confirm. If the user declines, stop and ask them to reconcile `civicrm.pot` manually before continuing.

---

## Step 3: Extract Strings with civistrings

```bash
EXTRACTED_POT=$(mktemp --suffix=.pot)

# Pass absolute paths via stdin; --base ensures #: comments use paths relative to CIVICRMPATH
echo "$FILES" | sed "s|^|$CIVICRMPATH/|" \
  | civistrings --base="$CIVICRMPATH" -o "$EXTRACTED_POT" -

echo "Extracted: $(grep -c '^msgid "' "$EXTRACTED_POT") entries (including header)"
```

`civistrings` handles `ts()` in PHP, `{ts}` in Smarty, and translatable patterns in JS. It outputs proper GNU gettext POT format with `#:` source references.

---

## Step 4: Identify New Strings

Compare extracted msgids against the existing `civicrm.pot` to find strings not yet registered.

```bash
POT_FILE="$CIVICRMPATH/l10n/pot/civicrm.pot"

mapfile -t NEW_STRINGS < <(
  grep '^msgid "' "$EXTRACTED_POT" \
  | grep -v '^msgid ""$' \
  | sed 's/^msgid "//; s/"$//' \
  | while IFS= read -r msgid; do
      escaped=$(printf '%s' "$msgid" | sed 's/\\/\\\\/g; s/"/\\"/g')
      if ! grep -qF "msgid \"${escaped}\"" "$POT_FILE"; then
        printf '%s\n' "$msgid"
      fi
    done
)

echo "New strings: ${#NEW_STRINGS[@]}"

if [ ${#NEW_STRINGS[@]} -eq 0 ]; then
  echo "All strings are already in civicrm.pot. Nothing to add."
  rm -f "$EXTRACTED_POT"
  exit 0
fi

printf '  - %s\n' "${NEW_STRINGS[@]}"
```

Show the new string list to the user and confirm before writing.

---

## Step 5: Append New Strings to civicrm.pot

Batch-write all new strings then push once — do not call `add-source-string.sh` per string (it pulls and pushes every time, which is slow for multiple strings).

```bash
for msgid in "${NEW_STRINGS[@]}"; do
  escaped=$(printf '%s' "$msgid" | sed 's/\\/\\\\/g; s/"/\\"/g')

  # Retrieve the #: source references from the extracted POT
  sources=$(grep -B5 "^msgid \"${escaped}\"$" "$EXTRACTED_POT" \
    | grep '^#:' | sed 's/^#: //' | tr '\n' ' ' | sed 's/ $//')

  if [ -n "$sources" ]; then
    printf '\n#: %s\nmsgid "%s"\nmsgstr ""\n' "$sources" "$escaped" >> "$POT_FILE"
  else
    printf '\nmsgid "%s"\nmsgstr ""\n' "$escaped" >> "$POT_FILE"
  fi

  echo "Added to POT: $msgid"
done

rm -f "$EXTRACTED_POT"

echo ""
echo "Pushing source to Transifex ..."
cd "$CIVICRMPATH" && tx push -s
```

---

## Step 6: Translate and Write to zh_TW/civicrm.po

Translate each new string into **Traditional Chinese (Taiwan style)** and batch-append to the PO file, then push once.

```bash
PO_FILE="$CIVICRMPATH/l10n/zh_TW/civicrm.po"

for msgid in "${NEW_STRINGS[@]}"; do
  escaped_msgid=$(printf '%s' "$msgid" | sed 's/\\/\\\\/g; s/"/\\"/g')
  # Claude provides the translation here
  escaped_msgstr=$(printf '%s' "TRANSLATION" | sed 's/\\/\\\\/g; s/"/\\"/g')

  printf '\nmsgid "%s"\nmsgstr "%s"\n' "$escaped_msgid" "$escaped_msgstr" >> "$PO_FILE"
  echo "Translated: $msgid → TRANSLATION"
done

echo ""
echo "Pushing zh_TW translation to Transifex ..."
cd "$CIVICRMPATH" && tx push -t -l zh_TW

echo "Regenerating MO file ..."
msgfmt "$PO_FILE" -o "$CIVICRMPATH/l10n/zh_TW/LC_MESSAGES/civicrm.mo"
echo "Done."
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

---

## Step 7: Verify Consistency and Stage Commit

```bash
# Check for orphaned strings: in PO but missing from POT
TEMP_CHECK=$(mktemp --suffix=.po)
msgmerge --no-fuzzy-matching --quiet "$PO_FILE" "$POT_FILE" -o "$TEMP_CHECK" 2>/dev/null
ORPHANED=$(msgattrib --only-obsolete "$TEMP_CHECK" \
  | grep '^#~ msgid "' | grep -v '^#~ msgid ""$')
rm -f "$TEMP_CHECK"

if [ -n "$ORPHANED" ]; then
  echo "Warning: the following strings exist in PO but are missing from POT — please review:"
  echo "$ORPHANED" | sed 's/^#~ msgid "//; s/"$//'
else
  echo "OK: PO and POT are consistent."
fi

# Stage both files
git -C "$CIVICRMPATH" add "$POT_FILE" "$PO_FILE"
git -C "$CIVICRMPATH" status
```

Show the diff and tell the user: "Please review the translation changes above. Run `/commit` when ready."

---

## Fallback: AI-based Extraction (when civistrings is unavailable)

When `civistrings` is not found, Claude reads each changed file directly and extracts translatable strings by recognising the patterns below. This handles multi-line and complex cases that grep cannot.

### PHP — `ts()` calls
```php
ts('Simple string')
ts("With double quotes")
ts('With placeholder %1', [1 => $var])
ts('Multi %1 placeholders %2', [1 => $a, 2 => $b])
```

### Smarty — `{ts}` blocks
```smarty
{ts}Simple string{/ts}
{ts 1=$var}Hello %1{/ts}
{ts escape='js'}String in JS context{/ts}
```

For each identified string, Claude:
1. Records the source file and line number for the `#:` reference
2. Skips strings already present in `civicrm.pot`
3. Continues from **Step 4** onwards with the collected strings

---

## FAQ

**sync-pot.sh shows orphaned strings — what do I do?**
These are strings in the remote PO that the local POT doesn't know about (usually legacy entries). Show the list to the user, explain each one, and proceed only after they confirm.

**String contains HTML — how to translate?**
Keep HTML tags verbatim. Example: `Click <a href="%1">here</a>` → `點擊<a href="%1">此處</a>`

**Multi-line msgid (contains `\n`) — how to handle?**
`civistrings` formats these automatically. Preserve the formatting; translate each segment naturally.

**A string appears in multiple files — what goes in `#:`?**
`civistrings` merges all source paths onto one `#:` line automatically.

**Commits span multiple branches (develop, hotfix) — any issue?**
No. `git log --all --grep` covers all branches; Step 1 needs no adjustment.
