# netiCRM `.claude` — AI 開發輔助設定

本目錄為 [Claude Code](https://claude.ai/code) 的專案層設定，包含 netiCRM/CiviCRM 專屬的 **Agents**、**Skills** 及 **權限設定**，讓 AI 能依循本專案的架構、慣例與品質標準協助開發。

---

## 目錄結構

```
.claude/
├── CLAUDE.md                    # 主要開發指南（Claude 每次啟動時自動讀取）
├── README.md                    # 本文件
├── settings.local.json          # 本機 Bash 指令白名單（不納入版控）
├── agents/                      # 專責 AI Agent 定義
│   ├── php-engineer.md
│   ├── frontend-engineer.md
│   ├── drupal-module-developer.md
│   ├── database-agent.md
│   ├── structure-planner.md
│   └── translation-extractor.md
└── skills/                      # 可呼叫的 Skill 定義
    ├── neticrm-backend/
    ├── neticrm-frontend/
    ├── neticrm-api/
    ├── playwright-testing/
    ├── extract-i18n/
    └── neticrm-review/
```

---

## CLAUDE.md — 主要開發指南

`CLAUDE.md` 是 Claude Code 每次對話啟動時自動載入的核心指南，涵蓋：

| 主題 | 內容摘要 |
|------|---------|
| **程式碼風格** | 2 空格縮排、嚴格相等（`===`）、PHP PascalCase、JS 單引號+分號 |
| **目錄結構** | `/CRM/`、`/api/v3/`、`/templates/`、`/xml/schema/`、`/neticrm/`、`/drupal/` |
| **路由定義** | `CRM/*/xml/Menu/*.xml`：`<path>`、`<page_callback>`、`<access_arguments>` |
| **權限系統** | `CRM_Core_Permission::check()`，定義位於 `basicPermissions()` 與 `Info.php` |
| **多語系翻譯** | PHP `ts()`、Smarty `{ts}`、Drupal `t()` 的語法與佔位符格式 |
| **分支策略** | `develop`（新功能）→ `master`（穩定版）→ `hotfix`（緊急修正）|

---

## Agents — 專責 AI Agent

Agent 是具備特定技能與工具存取範圍的獨立 AI 執行單元，適合需要深度鑽研特定領域的任務。由 Claude Code 主代理根據任務性質決定是否啟用。

### `php-engineer` · 模型：Opus

**適用場景**：實作 BAO 業務邏輯、修改 Form 處理流程、建立 API v3 端點、撰寫排程任務

**工作範圍**：
- `/CRM/` — BAO、DAO、Form 核心類別
- `/api/v3/` — API 端點
- `/external/` — 外部整合模組

**技能載入**：`neticrm-backend`

---

### `frontend-engineer` · 模型：Sonnet

**適用場景**：編輯 `.tpl`/`.css`/`.js` 檔案、建立 UI 功能、修復 CSS 版面問題、整合前端資源

**工作範圍**：
- `/templates/CRM/` — Smarty 模板
- `/js/` — JavaScript
- `/css/` — 樣式表
- `/CRM/Core/Smarty/plugins/` — 自訂 Smarty 外掛

**技能載入**：`neticrm-frontend`

---

### `drupal-module-developer` · 模型：Sonnet

**適用場景**：實作 Drupal Hooks、建立 Drupal 表單、Drupal 使用者與 CiviCRM 聯絡人同步、`/neticrm/` 子模組相關修改

**工作範圍**：`/neticrm/`、`/drupal/`（submodule 目錄）

**重要**：執行前必須先確認目前分支（`7.x-*` = Drupal 7；`10.x-*` = Drupal 10），以使用正確的 API。

**技能載入**：`neticrm-backend`

---

### `database-agent` · 模型：Sonnet

**適用場景**：任何資料庫 schema 變更需求，完整工作流程：XML schema 定義 → GenCode 產生 DAO → 建立 migration 腳本

**工作範圍**：
- `/xml/schema/` — Schema XML 定義
- `/CRM/**/DAO/` — 自動產生的 DAO（禁止手動修改）
- `/neticrm/neticrm_update/update/` — Migration 腳本
- `/sql/*.mysql` — SQL 檔案

**標準流程**：
1. 修改 `/xml/schema/` 中的 XML 定義
2. 執行 `cd xml && php GenCode.php` 重新產生 DAO
3. 建立 `/neticrm/neticrm_update/update/neticrm_xNNN.inc` migration 腳本
4. 將 XML、DAO、migration 腳本一起提交

**技能載入**：`neticrm-backend`

---

### `structure-planner` · 模型：Opus

**適用場景**：任何觸及多個 PHP 檔案的變更、複雜業務邏輯修改、外部 API 整合、或不清楚對下游元件影響時，應在實作前先用此 agent 規劃

**方法論**：Discovery（結構探索）→ Analysis（分析技術債）→ Planning（分步驟規劃）→ Validation（驗證與測試策略）

**技能載入**：`neticrm-backend`、`neticrm-frontend`

---

### `translation-extractor` · 模型：Haiku

**適用場景**：任何新增使用者面向文字後，自動提取翻譯字串、更新 civicrm.pot，並推送至 Transifex

**觸發方式**：使用者輸入 `extract translations for #NNNNN` 或 `/extract-i18n NNNNN`

**技能載入**：`neticrm-backend`、`neticrm-frontend`、`extract-i18n`

---

## Skills — 可呼叫的技能

Skills 是包含詳細參考文件的知識模組，供 Agent 或主代理在處理任務時載入。

### `neticrm-backend` — PHP 後端開發規範

為 CiviCRM 的 DAO/BAO/Form/API 分層架構提供完整的 PHP 開發規範。

**觸發時機**：在 `/CRM/` 撰寫 PHP、實作 BAO 業務邏輯、建立 API v3 端點、設定路由 XML、檢查權限

| 參考文件 | 內容 |
|---------|------|
| `references/php-patterns.md` | BAO/Form 類別結構、路由、權限、`ts()`、通用工具、測試、安全性 |
| `references/php-coding-style.md` | 完整 PSR 規則、括號位置、常數大小寫、陣列語法、php-cs-fixer |
| `references/hook-system.md` | Form hooks、資料 hooks（pre/post）、`CRM_Utils_Hook` 方法、實際模組範例 |
| `references/database-schema.md` | XML schema 結構、欄位型別/屬性、命名規則、索引/FK 樣式、GenCode 流程 |
| `references/api-endpoints.md` | 端點檔案結構、函式命名、CRUD 輔助函式、spec 函式、自訂 actions |

---

### `neticrm-frontend` — 前端開發規範

為 HTML、CSS、JavaScript、Smarty 模板提供 netiCRM 專屬的前端開發規範。

**觸發時機**：編輯 `.tpl`/`.css`/`.js` 檔案、修復 CSS 版面、撰寫 jQuery 程式碼、實作 Smarty 邏輯、檢查瀏覽器相容性

| 參考文件 | 內容 |
|---------|------|
| `references/css-standards.md` | 選擇器範圍（`.crm-container`）、CSS 變數、響應式設計（`ncg-*`）|
| `references/javascript-patterns.md` | `cj()` vs `$` 衝突、事件委派、`.crmAPI()` 呼叫模式 |
| `references/smarty-templates.md` | `{ts}` 翻譯、`{literal}` 區塊、`{crmURL}`、安全跳脫 |
| `references/html-conventions.md` | 語義化 HTML 結構、表單元素、資料表格、ZMDI 字體圖示 |
| `references/browser-support-policy.md` | 瀏覽器相容性政策（使用新 CSS 前必讀）|

**重要**：使用任何新 CSS 技術前，**必須**查閱 `references/browser-support-policy.md`。

---

### `neticrm-api` — API v3 文件規範

netiCRM REST API v3 的文件撰寫標準與呼叫參考。

**觸發時機**：撰寫或更新 API 文件、查閱 entity actions、實作 API 端點

| 參考文件 | 內容 |
|---------|------|
| `references/authentication.md` | API 金鑰設定、Header 格式、REST 權限 |
| `references/request-response.md` | 分頁、排序、過濾、巢狀查詢、curl 範例 |
| `references/entities.md` | 各 entity 支援的 actions 與必填欄位 |
| `references/php-api.md` | PHP 內部呼叫（`civicrm_api3`）、spec 函式、回傳值格式 |

---

### `playwright-testing` — E2E 測試規範

使用 Playwright 撰寫 netiCRM 前端整合測試的完整規範。

**觸發時機**：撰寫、修改或執行 `tests/playwright/` 下的測試

**重要原則**：
- 測試資料**優先透過 Admin UI 建立**，僅在 UI 無法建立時才使用 JS API（需向使用者說明並獲得同意）
- AI 產生的測試放在 `tests/playwright/tests/specific/`，預設不納入 CI
- **撰寫新測試前必須先讀 `references/test-index.md`**

| 參考文件 | 內容 |
|---------|------|
| `references/test-index.md` | 所有現有測試檔案與描述（**撰寫前必讀**）|
| `references/utilities.md` | `utils.js` 共用函式、日期選擇器、只讀欄位繞過 |
| `references/civicrm-ui-patterns.md` | Accordion、Selector、錯誤檢查、頁面標題模式 |
| `references/test-data.md` | 透過 Admin UI 建立測試資料、sort name、今日日期 |
| `references/validation-patterns.md` | 驗證測試模式、常見錯誤 |
| `references/civicrm-js-api.md` | `crmAPI`、AJAX、CSRF 處理 |

---

### `extract-i18n` — i18n 字串提取工作流程

**觸發方式**：`/extract-i18n NNNNN`（issue 編號）

完整 8 步驟流程：
1. 從 issue 相關 commits 收集變更檔案
2. AI 掃描 `ts()`/`{ts}` 模式提取字串
3. 同步 Transifex 遠端狀態（`pull-translation.sh`、`sync-pot.sh`）
4. 確認 `l10n/` 無未提交的變更
5. AI 翻譯為繁體中文（台灣），使用者確認
6. 驗證無重複字串
7. 追加到 `civicrm.pot` 與 `l10n/zh_TW/civicrm.po`，重新產生 `.mo`
8. 顯示摘要，提示使用者驗證後推送 Transifex

---

### `neticrm-review` — Code Review 工作流

**觸發方式**：`/neticrm-review`（加可選參數）

netiCRM 專屬的 code review skill，支援各開發階段的審查需求，輸出分層嚴重性報告。

**觸發時機**：
- **提交前自我審查**：推送前的程式碼自我檢查
- **PR 前審查**：feature branch 合併前的品質把關
- **合併後追查**：已合併的程式碼補審（Junior 審查、安全稽核、時間段審查）

**輸入模式**：

| 輸入格式 | 範例 | 行為 |
|---------|------|------|
| `#issue hash1 hash2` | `#45339 abc1234 def5678` | 顯示 commits，確認後 diff 指定 hash 範圍 |
| `#issue` | `#45339` | 搜尋所有相關 commits，選擇範圍後 diff |
| （無參數）| `/neticrm-review` | 詢問審查模式：未提交變更 / 與 develop 比較 / 最近合併的 branch / 指定範圍 |
| （貼上 diff）| 直接貼 diff 文字 | 直接審查貼上的 diff |

**審查分層**：

- **Layer 1（必做）**：掃描所有 `+` 行，對照 checklist 檢查風格與明顯問題
- **Layer 2（觸發）**：DB query、使用者輸入、資料寫入 → 讀取完整函式上下文
- **Layer 3（觸發）**：架構疑慮（Form 中有業務邏輯、API 中有直接 SQL）→ 讀取類別 header
- **Layer 4（觸發）**：公開函式簽名變更 → 搜尋所有呼叫端

**輸出格式**：
```
### 🔴 Critical (must fix)
### 🟡 Warning (recommended fix)
### 🔵 Suggestion (optional improvement)
```

**重要**：review skill 只輸出報告，**不會自動修正任何程式碼**；若需修正，請明確指示 AI 處理哪些項目。

| 參考文件 | 適用層 | 內容 |
|---------|-------|------|
| `references/php-checklist.md` | PHP | 風格、架構分層、安全性常見錯誤 |
| `references/frontend-checklist.md` | CSS / JS / Smarty | 選擇器範圍、`cj()` 規則、`{ts}` 翻譯 |
| `references/database-checklist.md` | Database | Schema/DAO 規範、migration 冪等守衛 |
| `references/drupal-checklist.md` | Drupal | D7/D10 API 差異、CiviCRM 初始化規則 |
| `references/security-checklist.md` | **全層（必載）** | SQL Injection、XSS、權限、GET 危險操作 |

---

## settings.local.json — 本機權限設定

此檔案設定 Claude Code 在本機不需每次詢問確認的 Bash 指令白名單。**已加入 `.gitignore`，不納入版控**，因為各開發者的本機環境路徑不同。

常見已授權的操作類型：
- `grep`、`mysql`、`git`、`php` 相關指令
- Docker 操作（`docker exec`、`docker compose`）
- 翻譯工作流程腳本（`tx push`、`msgfmt`、`sync-pot.sh`）
- 特定 WebFetch 網域（Drupal、GitHub、CKEditor 等文件站）

若需新增授權，使用 `/update-config` skill 或直接編輯 `settings.local.json`。

---

## 如何新增或修改設定

### 新增 Agent

在 `agents/` 建立 `<agent-name>.md`，包含 frontmatter：

```markdown
---
name: my-agent
description: "觸發條件與使用場景說明（供 Claude 判斷何時啟用）"
tools: Read, Write, Edit, Bash, Grep, Glob
model: sonnet   # opus / sonnet / haiku
skills:
  - neticrm-backend
---

# Agent 說明
...
```

### 新增 Skill

在 `skills/<skill-name>/` 建立 `SKILL.md` 作為入口，再在 `references/` 放置詳細參考文件。

### 新增本機權限

```bash
# 開啟 Claude Code 設定
/update-config
```

或直接編輯 `settings.local.json` 的 `permissions.allow` 陣列。

---

## 相關資源

- [Claude Code 文件](https://docs.anthropic.com/en/docs/claude-code)
- [CiviCRM 開發者文件](https://docs.civicrm.org/dev/en/latest/)
- [netiCRM GitHub](https://github.com/NETivism/netiCRM)
