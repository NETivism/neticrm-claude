# netiCRM/CiviCRM CSS 撰寫指引

## 專案背景

netiCRM 是基於 CiviCRM 的非營利組織客戶關係管理系統,採用 Drupal 7/10 作為底層框架。CiviCRM 的設計理念是可以嵌入在各種網站中,因此需要嚴格的樣式隔離。

## 核心規範: .crm-container 前綴

### 為什麼需要 .crm-container?

CiviCRM 使用 `.crm-container` 作為樣式隔離的容器,原因包括:

1. **避免污染宿主網站**: CiviCRM 常嵌入在各種網站中(WordPress, Drupal, Joomla等)
2. **防止被外部樣式覆蓋**: 保護 CiviCRM 的樣式不被外部 CSS 影響
3. **命名空間隔離**: 類似 CSS Modules 的概念,但是手動實現
4. **框架約定**: 這是 CiviCRM 15+ 年來的既定架構

### 強制規則

**所有針對 CiviCRM 內容的選擇器都必須加上 `.crm-container` 前綴。**

```css
/* ❌ 錯誤 - 會污染全域,也可能被外部覆蓋 */
.crm-actions-ribbon {
  background: #f5f5f5;
}

.crm-submit-buttons {
  display: flex;
  gap: 0.5rem;
}

/* ✅ 正確 - 正確隔離樣式 */
.crm-container .crm-actions-ribbon {
  background: #f5f5f5;
}

.crm-container .crm-submit-buttons {
  display: flex;
  gap: 0.5rem;
}
```

### 例外情況

#### 1. 全域元素 (body, html)

**重要**: 對於 `body`、`html` 等全域元素，應該使用 `:has(.crm-container)` 選擇器，確保只影響包含 CRM 內容的頁面：

```css
/* ❌ 錯誤 - 會影響所有頁面，包括非 CRM 頁面 */
body {
  font-family: sans-serif;
  line-height: 1.5;
}

html {
  box-sizing: border-box;
}

/* ✅ 正確方法 1: 使用 :has() 選擇器 */
body:has(.crm-container) {
  font-family: sans-serif;
  line-height: 1.5;
  background: #f5f5f5;
}

/* ✅ 正確方法 2: 直接在 .crm-container 內設定 */
.crm-container {
  font-family: sans-serif;
  line-height: 1.5;
}

/* ✅ 通用重置可以直接寫（影響所有頁面） */
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

**為什麼要這樣做？**
- CiviCRM 常嵌入在其他網站中
- 不使用 `:has()` 會影響宿主網站的所有頁面
- 使用 `:has(.crm-container)` 確保只在有 CRM 內容時才套用樣式

#### 2. CiviCRM 容器外的特定元素

#### 2. CiviCRM 容器外的特定元素

**只有**當元素**確實**不在 `.crm-container` 內時才可省略前綴：

```css
/* ✅ CiviCRM 頂部選單 (在 container 外，已確認) */
#civicrm-menu {
  position: fixed;
  top: 0;
  z-index: 9999;
}

/* ✅ 通知訊息容器 (通常在 container 外) */
.crm-notify-container {
  position: fixed;
  top: 20px;
  right: 20px;
}
```

**警告**: 在省略前綴前，必須先檢查 HTML 結構確認該元素真的不在 `.crm-container` 內！如果不確定，建議還是加上前綴。

#### 3. CSS Variables 定義

CSS Variables 應該定義在 `.crm-container` 內，而非 `:root`：

```css
/* ❌ 避免 - 會污染全域命名空間 */
:root {
  --crm-color-primary: #0073aa;
  --crm-spacing: 1rem;
}

/* ✅ 正確 - 定義在 .crm-container 內 */
.crm-container {
  --crm-color-primary: #0073aa;
  --crm-color-secondary: #6c757d;
  --crm-spacing: 1rem;
}

/* ✅ 如果真的需要在其他地方也能用，使用 :has() */
:root:has(.crm-container) {
  --crm-color-primary: #0073aa;
}
```

## 命名規範

### Class 命名格式

netiCRM/CiviCRM 使用 **BEM-like** 命名,但不完全遵循嚴格 BEM:

```css
/* 組件名稱使用 crm- 前綴 */
.crm-container .crm-component-name { }

/* 子元素使用 - 連接 */
.crm-container .crm-component-name-element { }

/* 狀態/變體也使用 - 連接 */
.crm-container .crm-component-name-active { }
.crm-container .crm-component-name-disabled { }
```

### 常見命名模式

```css
/* 表單相關 */
.crm-container .crm-form-block { }
.crm-container .crm-form-row { }
.crm-container .crm-form-label { }
.crm-container .crm-form-input { }

/* 按鈕 */
.crm-container .crm-button { }
.crm-container .crm-button-primary { }
.crm-container .crm-button-secondary { }
.crm-container .crm-button-delete { }

/* 佈局 */
.crm-container .crm-section { }
.crm-container .crm-section-header { }
.crm-container .crm-section-body { }

/* 狀態 */
.crm-container .crm-item-active { }
.crm-container .crm-item-disabled { }
.crm-container .crm-item-hidden { }
```

## 與 Drupal 整合

### Drupal 7 (舊版 netiCRM)

```css
/* Drupal 的樣式在 .crm-container 外 */
#block-system-main { }
.region-sidebar { }

/* CiviCRM 的樣式在 .crm-container 內 */
.crm-container .crm-contact-view { }
```

### Drupal 10 (新版 netiCRM)

```css
/* Drupal 10 使用 Classy/Stable theme */
.layout-container { }
.block { }

/* CiviCRM 樣式保持一致 */
.crm-container .crm-contact-view { }
```

## 權重管理

### .crm-container 不算過度限定

雖然一般 CSS 最佳實踐建議避免選擇器嵌套,但 `.crm-container` 是**架構層級的必要隔離**:

```css
/* ⚠️ 一般專案中這是過度限定 */
.container .nav-link { }

/* ✅ 但在 CiviCRM 中這是必要的隔離 */
.crm-container .crm-nav-link { }
```

### 避免過深嵌套

即使有 `.crm-container`,仍應避免過深的選擇器嵌套:

```css
/* ❌ 過深嵌套 - 難以維護 */
.crm-container .crm-form .crm-section .crm-row .crm-label {
  font-weight: bold;
}

/* ✅ 使用更扁平的結構 */
.crm-container .crm-form-label {
  font-weight: bold;
}
```

### 權重建議

```css
/* 權重: 20 (.crm-container + .crm-button) */
.crm-container .crm-button {
  padding: 0.5rem 1rem;
}

/* 權重: 30 (.crm-container + .crm-button + .crm-button-primary) */
.crm-container .crm-button.crm-button-primary {
  background: var(--crm-color-primary);
}

/* ❌ 避免: 權重過高 */
.crm-container div.crm-form-block > ul.crm-list > li.crm-item {
  /* 這樣太複雜了 */
}
```

## 響應式設計

### Mobile-First 方法

```css
/* 預設為 mobile 樣式 */
.crm-container .crm-dashboard {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
  .crm-container .crm-dashboard {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .crm-container .crm-dashboard {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### 常用斷點

netiCRM 建議的響應式斷點:

```css
/* Mobile: 預設 */
/* Tablet: 768px */
/* Desktop: 1024px */
/* Large Desktop: 1440px */

@media (min-width: 768px) { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
@media (min-width: 1440px) { /* Large Desktop */ }
```

## 主題變數

### 使用 CSS Variables

```css
/* 定義變數 (可在 :root 或 .crm-container) */
.crm-container {
  /* 顏色 */
  --crm-color-primary: #0073aa;
  --crm-color-secondary: #6c757d;
  --crm-color-success: #28a745;
  --crm-color-danger: #dc3545;
  --crm-color-warning: #ffc107;
  
  /* 間距 */
  --crm-spacing-xs: 0.25rem;
  --crm-spacing-sm: 0.5rem;
  --crm-spacing-md: 1rem;
  --crm-spacing-lg: 1.5rem;
  --crm-spacing-xl: 2rem;
  
  /* 字體 */
  --crm-font-size-sm: 0.875rem;
  --crm-font-size-base: 1rem;
  --crm-font-size-lg: 1.125rem;
  
  /* 邊框 */
  --crm-border-radius: 4px;
  --crm-border-color: #dee2e6;
}

/* 使用變數 */
.crm-container .crm-button {
  padding: var(--crm-spacing-sm) var(--crm-spacing-md);
  background: var(--crm-color-primary);
  border-radius: var(--crm-border-radius);
}
```

## 與 Bootstrap 整合

netiCRM 可能同時使用 Bootstrap,注意以下事項:

### 避免衝突

```css
/* ❌ 可能與 Bootstrap 衝突 */
.btn {
  /* 這會影響所有 Bootstrap buttons */
}

/* ✅ 使用 .crm-container 隔離 */
.crm-container .crm-btn {
  /* 只影響 CiviCRM 內的按鈕 */
}
```

### 選擇性引用 Bootstrap

```css
/* 如果需要使用 Bootstrap utilities */
.crm-container .d-flex {
  display: flex;
}

.crm-container .justify-content-between {
  justify-content: space-between;
}
```

## 除錯技巧

### 檢查是否正確隔離

```javascript
// 在瀏覽器 console 測試
document.querySelectorAll('.crm-actions-ribbon').length; // 應該是 0
document.querySelectorAll('.crm-container .crm-actions-ribbon').length; // 應該 > 0
```

### DevTools 檢查

1. 開啟瀏覽器 DevTools
2. 檢查元素的 Computed Styles
3. 確認樣式來源是 `.crm-container .crm-xxx` 而非 `.crm-xxx`

### 常見問題排查

#### 樣式沒有生效

```css
/* 問題: 選擇器權重不夠 */
.crm-button { /* 權重: 10 */ }

/* 被覆蓋 */
.crm-container .crm-button { /* 權重: 20 */ }

/* 解決: 加上 .crm-container */
.crm-container .crm-button { /* 權重: 20 */ }
```

#### 外部樣式污染

```css
/* 問題: 外部網站的樣式影響到 CiviCRM */
.button {
  /* 外部網站的樣式 */
  background: red;
}

/* CiviCRM 的按鈕被影響 */
<button class="button crm-button">Click</button>

/* 解決: 使用 .crm-container 隔離 */
.crm-container .crm-button {
  background: blue; /* 權重更高,不會被覆蓋 */
}
```

## 自動化檢查

使用 `check_css_quality.py` 腳本自動檢查:

```bash
# 自動偵測 CiviCRM 檔案
python check_css_quality.py neticrm-styles.css

# 明確指定 CiviCRM 模式
python check_css_quality.py styles.css --civicrm
```

腳本會自動檢查:
- ✅ `.crm-container` 前綴是否正確使用
- ✅ 是否使用過時的 float 佈局
- ✅ 是否濫用 !important
- ✅ 選擇器是否過度複雜

## 總結檢查清單

撰寫 netiCRM/CiviCRM CSS 前,確認:

- [ ] 所有 `.crm-` 開頭的選擇器都加上 `.crm-container` 前綴
- [ ] 對於 body/html 樣式，使用 `body:has(.crm-container)` 或在 `.crm-container` 內設定
- [ ] CSS Variables 定義在 `.crm-container` 內，而非 `:root`
- [ ] 容器外元素（如 #civicrm-menu）已確認真的不在 `.crm-container` 內
- [ ] 使用現代 CSS (Grid/Flexbox 而非 float)
- [ ] 避免過深的選擇器嵌套
- [ ] 測試在 Drupal 環境中樣式是否正確隔離
- [ ] 使用自動化工具檢查程式碼品質

## 參考資源

- CiviCRM 官方文件: https://docs.civicrm.org/
- netiCRM 專案: https://neticrm.tw/
- Drupal Theming: https://www.drupal.org/docs/theming-drupal
