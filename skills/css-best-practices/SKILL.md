---
name: css-best-practices
description: 撰寫高品質、符合現代最佳實踐的 CSS 程式碼。專為 netiCRM/CiviCRM 專案優化，強制要求選擇器加上 .crm-container 前綴以隔離樣式。解決 AI 常見問題：避免暴力解法(如濫用 !important)、使用現代 CSS 特性取代舊方法、建立可維護的架構、正確理解 Box Model 和 Stacking Context。當需要撰寫、修改、檢查、審查、分析、評估 CSS 程式碼品質時使用。可自動執行品質檢查腳本。
---

# CSS Best Practices

本 skill 協助 Claude 撰寫高品質、可維護的 CSS 程式碼,特別針對 AI 在 CSS 撰寫中的常見問題提供解決方案。

## 🚨 重要：CSS 檢查流程

**當使用者要求「檢查」、「審查」、「分析」、「評估」CSS 程式碼時，必須執行以下流程：**

### 步驟 1: 儲存 CSS 檔案
如果 CSS 是字串形式，先儲存到檔案：
```bash
cat > /tmp/check.css << 'EOF'
[CSS 內容]
EOF
```

### 步驟 2: 執行品質檢查腳本

**務必實際執行以下命令：**

```bash
# CiviCRM/netiCRM 專案
python scripts/check_css_quality.py /tmp/check.css --civicrm

# 一般專案  
python scripts/check_css_quality.py /tmp/check.css
```

**注意**: 必須**實際執行**這個 Python 腳本，不是只說明如何執行。使用 `bash_tool` 或 `code_execution` 工具來執行。

### 步驟 3: 解讀結果並提供建議

根據腳本輸出的錯誤和警告，向使用者說明：
- 發現了什麼問題
- 為什麼這些是問題
- 如何修正

### 檢查腳本功能

此腳本會檢測：
- ❌ **CiviCRM 前綴缺失**（`--civicrm` 模式）
- ❌ **body/html 沒有使用 :has()**（`--civicrm` 模式）
- ❌ **:root 中的 --crm- 變數**（`--civicrm` 模式）
- ❌ 使用過時的 float 佈局
- ❌ clearfix hack
- ⚠️ !important 濫用
- ⚠️ vendor prefixes
- ⚠️ 過度限定選擇器

---

## ⚠️ netiCRM/CiviCRM 專案特殊規範

**CRITICAL**: 在 netiCRM/CiviCRM 專案中撰寫 CSS 時,**必須遵循以下規則**:

### 強制使用 `.crm-container` 前綴

CiviCRM 的主要頁面內容都包在 `.crm-container` 容器內,為了避免樣式污染全域和被外部樣式覆蓋,**所有選擇器都應該加上 `.crm-container` 前綴**。

```css
/* ❌ 錯誤 - 缺少 .crm-container 前綴 */
.crm-actions-ribbon {
  background: #f5f5f5;
}

.crm-submit-buttons {
  margin-top: 1rem;
}

/* ✅ 正確 - 加上 .crm-container 前綴 */
.crm-container .crm-actions-ribbon {
  background: #f5f5f5;
}

.crm-container .crm-submit-buttons {
  margin-top: 1rem;
}
```

### 例外情況與特殊處理

#### 1. 全域元素需使用 `:has()` 選擇器

對於 `body`、`html` 等全域元素，**必須使用 `:has(.crm-container)` 確保只影響包含 CRM 的頁面**：

```css
/* ❌ 錯誤 - 會影響所有頁面 */
body {
  font-family: sans-serif;
}

/* ✅ 正確 - 只影響有 CRM 的頁面 */
body:has(.crm-container) {
  font-family: sans-serif;
  background: #f5f5f5;
}

/* ✅ 或者直接在 .crm-container 內設定 */
.crm-container {
  font-family: sans-serif;
}
```

#### 2. CRM 容器外的特定元素

**只有**以下明確在 `.crm-container` 外的元素可以不加前綴：

```css
/* ✅ CiviCRM 頂部選單 (確實在 container 外) */
#civicrm-menu {
  position: fixed;
  z-index: 9999;
}

/* ✅ 通知訊息 (通常在 container 外) */
.crm-notify-container {
  position: fixed;
  top: 20px;
  right: 20px;
}
```

**重要**: 使用前必須確認該元素真的不在 `.crm-container` 內！

### 為何這與一般最佳實踐不同?

一般 CSS 最佳實踐建議**避免過度限定選擇器**,但 CiviCRM 是個例外:

1. **隔離性需求**: CiviCRM 經常嵌入在其他網站中,需要隔離樣式
2. **避免污染**: 防止 CiviCRM 樣式影響外部網站
3. **避免被覆蓋**: 防止外部網站樣式覆蓋 CiviCRM
4. **框架設計**: 這是 CiviCRM 框架的既定架構

**在 netiCRM/CiviCRM 專案中,`.crm-container` 前綴是必要的架構層級,而非過度限定。**

### 快速檢查清單

撰寫 CiviCRM CSS 前,確認:
- [ ] 是否為 netiCRM/CiviCRM 專案?
- [ ] 目標元素是否在 `.crm-container` 內?
- [ ] 如果是,選擇器是否加上 `.crm-container` 前綴?
- [ ] 如果要設定 body/html,是否使用 `body:has(.crm-container)` 或在 `.crm-container` 內設定?
- [ ] 如果是容器外的元素(如 #civicrm-menu),是否已確認它真的不在容器內?

---

## 核心原則

### 1. 視覺化思維 (Spatial Reasoning)

在撰寫 CSS 前,**必須先理解 DOM 結構和視覺關係**:

```markdown
撰寫流程:
1. 分析 HTML 結構 → 識別父子關係、兄弟關係
2. 理解定位上下文 → position、stacking context、containing block
3. 規劃佈局方式 → Grid、Flexbox、或組合使用
4. 考慮響應式需求 → 斷點、流式佈局
5. 撰寫 CSS → 從外到內、從佈局到細節
```

**關鍵問題檢查清單:**
- `position: absolute` 的參考點是誰? (最近的 positioned ancestor)
- 這個元素的 `z-index` 在哪個 stacking context 中?
- 使用 Flexbox 還是 Grid? (一維 vs 二維佈局)
- 這個寬度百分比是相對於誰計算的?

### 2. 現代 CSS 優先 (Modern CSS First)

**永遠使用現代 CSS 特性,拒絕過時方法:**

#### ✅ 使用 (2020+)
- **佈局**: CSS Grid, Flexbox, `gap` property
- **響應式**: Container Queries, `clamp()`, `min()`, `max()`
- **定位**: Logical Properties (`margin-inline`, `padding-block`)
- **顏色**: `oklch()`, CSS Variables (`--color-primary`)
- **層疊**: `@layer` 管理樣式優先順序

#### ❌ 避免 (2015 以前)
- **禁止 `float` 用於佈局** (除非文字環繞圖片的特殊情境)
- **禁止 `clearfix` hack**
- **禁止 `display: table` 模擬表格佈局**
- **禁止 vendor prefixes** (使用 autoprefixer 工具處理)
- **禁止 `position: absolute` 硬編碼像素定位** (除非明確需求)

**範例對比:**

```css
/* ❌ 舊方法 (2010) - 禁止使用 */
.container::after {
  content: "";
  display: table;
  clear: both;
}
.item {
  float: left;
  width: 33.33%;
}

/* ✅ 現代方法 (2024) */
.container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}
```

### 3. CSS 技術可行性評估

**CRITICAL**: 在使用任何「現代 CSS 特性」前，**必須先評估瀏覽器支援度是否符合公司政策**。

#### ⚠️ 強制性規則：禁止依賴知識截止日期

**CRITICAL - 必須遵守**：

在評估任何 CSS 技術的瀏覽器支援度時，**嚴禁**直接基於 Claude 的知識截止日期（2025年1月）來判斷支援度。

**原因**：
- 瀏覽器支援度會隨時間快速變化
- 新技術可能在知識截止日期後獲得廣泛支援
- 依賴過時資訊會導致錯誤的技術決策

**強制要求**：在評估 CSS 技術前，**必須先使用 WebSearch 或 WebFetch 查詢最新的瀏覽器支援資訊**，然後才能給出結論。

**必須查詢的情況**：
- ✅ 任何看起來是「新的」、「實驗性」或「不常見」的 CSS 技術
- ✅ 任何使用 `::` 偽元素、`@` 規則（除了基本的 @media）的技術
- ✅ 包含 `scroll-`、`container-`、`@layer`、`@property` 等關鍵字的技術
- ✅ 使用者明確要求評估瀏覽器支援度時
- ✅ 當你對技術的支援度「不確定」或「沒有把握」時

**可不查詢的例外**：
- ❌ 非常成熟且廣為人知的基礎技術（Flexbox、CSS Grid、CSS Variables、transition、animation）
- ❌ 已在 modern-css-features.md 明確標註為「安全使用 >95% 支援」的技術

**執行方式**：
```
# 查詢範例
WebSearch: "::scroll-button caniuse 2026"
WebFetch: https://caniuse.com/?search=scroll-button
```

**如果違反此規則**：給出基於過時知識的錯誤判斷，將導致專案使用不相容的 CSS 技術。

---

#### 為何需要評估？

netiCRM/CiviCRM 專案需要支援：
- **iOS/iPadOS N-2 滾動式支援政策**（N = 當前最新版本）
- **iOS WebKit 限制**：所有瀏覽器（包含 Chrome、Firefox）都使用 Safari WebKit 引擎
- 這意味著某些「現代」CSS 特性在舊版 iOS 上可能無法使用

#### 核心概念：核心功能 vs 加分特效

**核心功能**（影響網站主要架構排版或內容顯示）
- 必須支援到「僅確保基本瀏覽」版本（N-2）
- 建議達到 [Baseline Widely available](https://developer.mozilla.org/en-US/docs/Glossary/Baseline/Compatibility#baseline_badges) 標準
- 範例：CSS Grid、Flexbox、`:has()` 選擇器

**加分特效**（提升體驗的裝飾性質）
- 只需支援「完整支援」版本（N 和 N-1）
- 建議達到 [Baseline Newly available](https://developer.mozilla.org/en-US/docs/Glossary/Baseline/Compatibility#baseline_badges) 標準
- 可使用漸進增強（Graceful Degradation）
- 範例：Scroll-driven Animations、text-autospace

#### 評估流程（必須執行）

**步驟 1: 確認當前支援政策**

使用 WebSearch 查詢最新 iOS 版本：
```
查詢語句範例：
"iOS version history" site:wikipedia.org
"latest iOS version 2026"
```

確認當前的 N、N-1、N-2 值（例如：2026.01 時為 26、18、17）

**步驟 2: 查詢技術支援度**

使用 WebFetch 或 WebSearch 查詢該 CSS 技術的瀏覽器支援度：

```
WebFetch 範例：
URL: https://caniuse.com/?search=[CSS技術名稱]
Prompt: "請提取這個 CSS 技術的瀏覽器支援資訊，特別是 iOS Safari 的最低支援版本和 Baseline 狀態"

WebSearch 範例：
"CSS Grid browser support iOS Safari"
"CSS :has() caniuse iOS"
```

**步驟 3: 判斷技術類型**

- 這個技術是「核心功能」還是「加分特效」？
- 核心功能：若不支援會導致版面崩壞或內容無法顯示
- 加分特效：若不支援僅缺少額外效果，但不影響基本閱讀

**步驟 4: 做出決策**

- **核心功能**：iOS 最低支援版本必須 <= N-2
- **加分特效**：iOS 最低支援版本建議 <= N-1，若不符合則使用漸進增強

#### 快速決策範例

```css
/* ✅ CSS Grid - 核心功能，iOS 10.3+ 支援，遠低於 N-2 */
.container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}

/* ✅ :has() - 核心功能，iOS 15.4+ 支援，已覆蓋 N-2 */
.card:has(img) {
  display: grid;
}

/* ⚠️ CSS Nesting - 核心功能，但 iOS 17.0-17.1 僅部分支援 */
/* 需使用 SCSS/SASS 轉譯，或等到支援度提升 */

/* ✅ text-autospace - 加分特效，iOS 18.4+ 支援 */
/* 可使用，舊版自然降級不影響閱讀 */
.content {
  text-autospace: normal;
}

/* ✅ Scroll-driven Animations - 加分特效，iOS 18+ 支援 */
/* 可使用，舊版無動畫但不影響功能 */
```

#### 詳細評估指引

參考 [browser-support-policy.md](references/browser-support-policy.md) 了解：
- 完整的瀏覽器支援政策
- iOS WebKit 限制說明
- 詳細的評估流程和決策樹
- 實際案例分析（CSS Grid、CSS Nesting、:has()、text-autospace 等）

**重要**: 每次使用新的 CSS 技術前，務必執行評估流程，確保符合公司支援政策。

### 4. 架構優先,避免暴力解法

#### 權重管理 (Specificity)

**權重階層 (由低到高):**
```
元素選擇器 (1)  <  類別選擇器 (10)  <  ID 選擇器 (100)  <  內聯樣式 (1000)  <  !important (10000)
```

**撰寫規則:**
1. **優先使用單一 class** (`.button` 而非 `div.container > ul > li.item`)
2. **禁止使用 `!important`** 除非:
   - 覆蓋第三方套件樣式 (並註解說明原因)
   - Utility classes (如 Tailwind 的 `.hidden`)
3. **使用 `@layer` 管理權重:**

```css
/* ✅ 使用 @layer 管理階層 */
@layer reset, base, components, utilities;

@layer reset {
  * { margin: 0; padding: 0; }
}

@layer components {
  .button { 
    padding: 0.5rem 1rem;
    background: var(--color-primary);
  }
}

@layer utilities {
  .hidden { display: none !important; } /* 這裡可以用 !important */
}
```

#### 避免過度限定 (Over-qualification)

```css
/* ❌ 過度限定 - 難以重用、權重過高 */
div.container > ul.list > li.item > a.link {
  color: blue;
}

/* ✅ 使用 BEM 或單一 class */
.nav-link {
  color: blue;
}

/* ⚠️ CiviCRM 專案例外: .crm-container 前綴是必要的 */
/* 在 netiCRM/CiviCRM 專案中這樣寫是正確的: */
.crm-container .crm-actions-ribbon {
  background: #f5f5f5;
}
/* 這不算過度限定,因為 .crm-container 是架構層級的隔離容器 */
```

### 5. 語意化命名與可維護性

#### 命名規範 (推薦 BEM 或功能性命名)

```css
/* ✅ BEM 命名 */
.card { }
.card__header { }
.card__title { }
.card--featured { }

/* ✅ 功能性命名 (Utility-first) */
.flex { display: flex; }
.gap-4 { gap: 1rem; }
.text-center { text-align: center; }

/* ❌ 避免無意義命名 */
.box1 { }
.div-2 { }
.style-new { }
```

#### 提取共用樣式

```css
/* ❌ 重複造輪子 */
.crm-container .crm-button-primary { 
  padding: 0.5rem 1rem; border-radius: 4px; font-weight: 600; 
}
.crm-container .crm-button-secondary { 
  padding: 0.5rem 1rem; border-radius: 4px; font-weight: 400; 
}
.crm-container .crm-button-danger { 
  padding: 0.5rem 1rem; border-radius: 4px; font-weight: 600; 
}

/* ✅ 提取共用基類 (netiCRM 風格) */
.crm-container .crm-button {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 600;
}
.crm-container .crm-button.crm-button-secondary { 
  font-weight: 400; 
}
.crm-container .crm-button.crm-button-danger { 
  background: var(--color-danger); 
}
```

### 6. 響應式設計最佳實踐

```css
/* ✅ 使用 Mobile-First 方法 */
.container {
  /* 預設 mobile 樣式 */
  padding: 1rem;
}

@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}

/* ✅ 使用 clamp() 實現流式大小 */
.title {
  font-size: clamp(1.5rem, 4vw, 3rem);
}

/* ✅ 使用 Container Queries (現代方法) */
@container (min-width: 400px) {
  .card { 
    grid-template-columns: 1fr 2fr; 
  }
}
```

## 常見問題與解決方案

**注意**: 以下範例為通用 CSS,在 netiCRM/CiviCRM 專案中使用時，記得加上 `.crm-container` 前綴。

### 問題 1: 垂直置中

```css
/* ❌ 舊方法 */
.crm-container .crm-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* ✅ 現代方法 - Flexbox (netiCRM 範例) */
.crm-container .crm-form-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* ✅ 現代方法 - Grid (netiCRM 範例) */
.crm-container .crm-modal-content {
  display: grid;
  place-items: center;
}
```

### 問題 2: 多欄佈局

```css
/* ❌ 舊方法 */
.crm-container .crm-col { 
  float: left; 
  width: 33.33%; 
}

/* ✅ 現代方法 - Grid with auto-fit (netiCRM 範例) */
.crm-container .crm-grid-layout {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}
```

### 問題 3: Sticky Footer

```css
/* ❌ 複雜的舊方法 */
html, body { height: 100%; }
.crm-container .crm-wrapper { 
  min-height: 100%; 
  margin-bottom: -50px; 
}
.crm-container .crm-footer { 
  height: 50px; 
}

/* ✅ 現代方法 - 使用 :has() 確保只影響 CRM 頁面 */
body:has(.crm-container) {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

/* ✅ 或者在 .crm-container 內處理 */
.crm-container {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}
```

### 問題 4: 隱藏元素

```css
/* 不同的隱藏方式有不同用途 */

/* 完全移除 (不佔空間、不可互動、不被螢幕閱讀器讀取) */
.crm-container .crm-hidden {
  display: none;
}

/* 視覺隱藏但保留在 DOM (佔空間、可被螢幕閱讀器讀取) */
.crm-container .crm-visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* 視覺隱藏但不佔空間 */
.invisible {
  visibility: hidden;
}

/* 透明但仍可互動 */
.transparent {
  opacity: 0;
}
```

## 撰寫檢查清單

在完成 CSS 程式碼前,逐一檢查:

### 瀏覽器支援度評估
- [ ] **[強制性]** 如使用「新的」或「不常見」的 CSS 技術，是否已**實際執行** WebSearch/WebFetch 查詢？（禁止依賴知識截止日期）
- [ ] **[使用新 CSS 技術]** 是否已查詢當前的 iOS 版本支援政策（N, N-1, N-2）?
- [ ] **[使用新 CSS 技術]** 是否已在 caniuse.com 或 MDN 查詢該技術的支援度?
- [ ] **[使用新 CSS 技術]** 是否已確認該技術在 iOS Safari 的最低支援版本?
- [ ] **[使用新 CSS 技術]** 是否已判斷該技術是「核心功能」還是「加分特效」?
- [ ] **[核心功能]** 確認最低支援版本 <= N-2?
- [ ] **[加分特效]** 確認可在舊版自然降級，不影響基本瀏覽?

### netiCRM/CiviCRM 專案規範
- [ ] **[CiviCRM 專案]** 如果是 netiCRM/CiviCRM,選擇器是否加上 `.crm-container` 前綴?
- [ ] **[CiviCRM 專案]** 如果設定 body/html 樣式，是否使用 `body:has(.crm-container)` 或在 `.crm-container` 內設定?

### 程式碼品質
- [ ] 是否使用了現代 CSS 特性? (Grid/Flexbox 而非 float)
- [ ] 選擇器權重是否合理? (避免過度限定,但 CiviCRM 的 `.crm-container` 除外)
- [ ] 是否使用了 `!important`? (如果有,是否真的必要並加上註解?)
- [ ] class 命名是否語意化? (功能導向而非外觀導向)
- [ ] 是否有重複的樣式可以提取?

### 響應式與無障礙
- [ ] 響應式設計是否使用 mobile-first?
- [ ] 是否考慮了 accessibility? (focus states, screen readers)
- [ ] 顏色對比度是否符合 WCAG 標準?

### 架構與維護性
- [ ] 是否使用了 CSS Variables 管理主題變數?
- [ ] position/z-index 的定位上下文是否正確?

## 框架特定指引

### netiCRM/CiviCRM 專案

參考 [neticrm-guidelines.md](references/neticrm-guidelines.md) 了解:
- `.crm-container` 前綴的完整規範和例外情況
- 與 Drupal 整合的注意事項
- Bootstrap 整合和衝突避免
- 命名規範和常見模式
- 自動化檢查工具使用方式

### 使用 Tailwind CSS 時

參考 [tailwind-guidelines.md](references/tailwind-guidelines.md) 了解:
- 正確的 class 名稱 (避免幻覺產生不存在的 class)
- 何時提取 component class
- 如何使用 `@apply` 的最佳時機

### 使用 CSS Modules 時

參考 [css-modules-guidelines.md](references/css-modules-guidelines.md) 了解:
- 命名規範
- 如何處理 global styles
- composition 的使用時機

## 效能考量

```css
/* ✅ 使用 CSS containment 優化效能 */
.card {
  contain: layout style paint;
}

/* ✅ 使用 will-change 提示瀏覽器 (但不要濫用) */
.animated-element {
  will-change: transform;
}

/* ✅ 使用 content-visibility 延遲渲染 */
.long-content {
  content-visibility: auto;
}
```

## 除錯技巧

當樣式不如預期時:

1. **使用瀏覽器 DevTools 檢查:**
   - Computed styles (計算後的實際值)
   - Box model visualization
   - Stacking context inspector

2. **常見問題排查:**
   - 父層是否設定了 `overflow: hidden`?
   - 是否有更高權重的樣式覆蓋?
   - `position` 和 `z-index` 的 stacking context 是否正確?
   - Flexbox/Grid container 是否有設定正確的屬性?

3. **暫時性除錯樣式:**
   ```css
   * { outline: 1px solid red; } /* 檢視所有元素邊界 */
   ```

## 參考資源

- **瀏覽器支援政策與評估指引**: [browser-support-policy.md](references/browser-support-policy.md) - 公司瀏覽器支援規格、iOS WebKit 限制、CSS 技術可行性評估流程
- **現代 CSS 特性支援表**: [modern-css-features.md](references/modern-css-features.md) - 現代 CSS 特性列表與支援度查詢方法
- **netiCRM/CiviCRM 專案指引**: [neticrm-guidelines.md](references/neticrm-guidelines.md) - `.crm-container` 前綴規範與完整說明
- 詳細的 Tailwind CSS 指引: [tailwind-guidelines.md](references/tailwind-guidelines.md)
- CSS Modules 使用規範: [css-modules-guidelines.md](references/css-modules-guidelines.md)
