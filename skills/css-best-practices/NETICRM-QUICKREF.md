# netiCRM CSS 快速參考卡 🚀

## 🔴 最重要的規則 (必須遵守)

### Rule #1: `.crm-container` 前綴

**所有 `.crm-` 開頭的選擇器都必須加上 `.crm-container` 前綴**

```css
/* ❌ 錯誤 */
.crm-actions-ribbon { }
.crm-button { }
.crm-form-block { }

/* ✅ 正確 */
.crm-container .crm-actions-ribbon { }
.crm-container .crm-button { }
.crm-container .crm-form-block { }
```

### 例外 (需特別注意)

**全域元素使用 :has()**

```css
/* ❌ 錯誤 - 會影響所有頁面 */
body { font-family: sans-serif; }

/* ✅ 正確 - 只影響有 CRM 的頁面 */
body:has(.crm-container) { 
  font-family: sans-serif; 
}

/* ✅ 或直接在容器內設定 */
.crm-container {
  font-family: sans-serif;
}
```

**容器外元素 (必須確認)**

只有**確認**不在 `.crm-container` 內的元素才可省略：

```css
/* ✅ 確認在容器外 */
#civicrm-menu { }
.crm-notify-container { }
```

## 📋 常用模式

### 表單元素

```css
.crm-container .crm-form-block { }
.crm-container .crm-form-row { }
.crm-container .crm-form-label { }
.crm-container .crm-form-input { }
```

### 按鈕

```css
.crm-container .crm-button { }
.crm-container .crm-button-primary { }
.crm-container .crm-button-secondary { }
.crm-container .crm-button-delete { }
```

### 佈局

```css
.crm-container .crm-section { }
.crm-container .crm-section-header { }
.crm-container .crm-section-body { }
```

## 🎨 現代 CSS

### 使用 Grid/Flexbox

```css
/* ✅ 使用 Grid */
.crm-container .crm-dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

/* ✅ 使用 Flexbox */
.crm-container .crm-toolbar {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
```

### 避免過時方法

```css
/* ❌ 不要用 */
float: left;
clear: both;
display: table;

/* ✅ 改用 */
display: grid;
display: flex;
```

## 🎯 響應式設計

### Mobile-First

```css
/* 預設 mobile */
.crm-container .crm-grid {
  grid-template-columns: 1fr;
}

/* Tablet (768px+) */
@media (min-width: 768px) {
  .crm-container .crm-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .crm-container .crm-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## 🔧 CSS Variables

```css
/* ✅ 定義在 .crm-container 內 */
.crm-container {
  /* 顏色 */
  --crm-color-primary: #0073aa;
  --crm-color-secondary: #6c757d;
  
  /* 間距 */
  --crm-spacing-sm: 0.5rem;
  --crm-spacing-md: 1rem;
  --crm-spacing-lg: 1.5rem;
}

/* 使用 */
.crm-container .crm-button {
  background: var(--crm-color-primary);
  padding: var(--crm-spacing-sm) var(--crm-spacing-md);
}
```

## ✅ 自動檢查

```bash
# 自動偵測 CiviCRM (檔名含 'crm' 或 'civi')
python check_css_quality.py neticrm-styles.css

# 強制 CiviCRM 模式
python check_css_quality.py styles.css --civicrm
```

## 🚨 常見錯誤

### 錯誤 1: 忘記加前綴

```css
/* ❌ */
.crm-actions-ribbon { display: flex; }

/* ✅ */
.crm-container .crm-actions-ribbon { display: flex; }
```

### 錯誤 2: 使用舊的 float

```css
/* ❌ */
.crm-container .crm-col { float: left; width: 50%; }

/* ✅ */
.crm-container .crm-two-column {
  display: grid;
  grid-template-columns: 1fr 1fr;
}
```

### 錯誤 3: 過度嵌套

```css
/* ❌ */
.crm-container .crm-form .crm-section .crm-row .crm-label { }

/* ✅ */
.crm-container .crm-form-label { }
```

## 📚 完整文件

詳細資訊請參考:
- `SKILL.md` - 完整 CSS 最佳實踐
- `references/neticrm-guidelines.md` - netiCRM 詳細指引
- `scripts/check_css_quality.py --help` - 檢查工具說明

---

**記住**: `.crm-container` 不是過度限定,而是 CiviCRM 架構的必要隔離! 🎯
