# Tool Use Guidelines

Use the minimum tool calls needed. Never read more content than required.

## Read — always use offset/limit

Never `Read` an entire file to look for something — use `Grep` first, then read only the relevant range.

```bash
# Step 1: locate the function line number
grep -n "function completeTransaction" CRM/Contribute/BAO/Contribution.php

# Step 2: read only the relevant range (function start − 5 lines, ~100 lines total)
Read CRM/Contribute/BAO/Contribution.php offset=<line-5> limit=100
```

For Layer 3 (class header only): `offset=0 limit=40` — do not re-read the whole file if it was already partially read in Layer 2.

## Grep — two-step for codebase-wide search (Layer 4)

```bash
# Step 1: list affected files only
grep -rl "functionName" . --include="*.php"

# Step 2: get line numbers in matched files only
grep -n "functionName" path/to/matched_file.php
```

Do not use `grep -r` without `-l` first when searching the entire codebase.

## Bash — issue independent commands in the same turn

When multiple Bash calls are independent (e.g., Pattern B searching all three repos, Pattern C showing recent logs across repos), issue them in the same response turn — do not wait for one to finish before starting the next.

## git diff — scope to paths when review is module-specific

If the user asks to review a specific module, add a path filter to reduce output:

```bash
git diff <hash1>..<hash2> -- neticrm/ CRM/Contribute/
```
