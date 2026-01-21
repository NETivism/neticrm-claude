# CSS Modules Guidelines

CSS Modules 是一種讓 CSS class 自動具有局部作用域的解決方案,避免全域命名衝突。

## 基本概念

### 檔案命名規範

```
Component.module.css    ← React/Next.js 慣例
component.module.css    ← 也可接受
styles.module.css       ← 通用名稱
```

### 基本使用

```css
/* Button.module.css */
.button {
  padding: 0.5rem 1rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
}

.button:hover {
  background: #0056b3;
}

.primary {
  background: #007bff;
}

.secondary {
  background: #6c757d;
}
```

```jsx
// Button.jsx
import styles from './Button.module.css';

function Button({ variant = 'primary', children }) {
  return (
    <button className={styles.button + ' ' + styles[variant]}>
      {children}
    </button>
  );
}
```

編譯後的 class 名稱會變成: `Button_button__x7d2f` (自動加上 hash,避免衝突)

## 命名規範

### ✅ 使用 camelCase

```css
/* ✅ 推薦 */
.buttonPrimary { }
.cardHeader { }
.navLink { }

/* ❌ 避免使用 kebab-case (需要用方括號存取) */
.button-primary { }  /* JS 中要寫 styles['button-primary'] */
```

### ✅ 語意化命名

```css
/* ✅ 功能導向 */
.container { }
.header { }
.footer { }
.primaryButton { }

/* ❌ 外觀導向 */
.blueBox { }
.bigText { }
```

## Composition (組合)

### 使用 `composes` 關鍵字

```css
/* Button.module.css */
.button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.primary {
  composes: button;
  background: #007bff;
  color: white;
}

.secondary {
  composes: button;
  background: #6c757d;
  color: white;
}

.large {
  composes: button;
  padding: 0.75rem 1.5rem;
  font-size: 1.125rem;
}
```

```jsx
// 使用時只需單一 class
<button className={styles.primary}>Primary</button>
<button className={styles.large}>Large Button</button>
```

### 從其他檔案組合

```css
/* base.module.css */
.resetButton {
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  cursor: pointer;
}
```

```css
/* Button.module.css */
.button {
  composes: resetButton from './base.module.css';
  padding: 0.5rem 1rem;
  background: #007bff;
  color: white;
}
```

## Global Styles

### 使用 `:global` 選擇器

```css
/* App.module.css */

/* 局部作用域 (預設) */
.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 全域作用域 */
:global(.dark-mode) .container {
  background: #1a1a1a;
}

:global {
  /* 整個區塊都是全域 */
  body {
    margin: 0;
    font-family: -apple-system, sans-serif;
  }
}
```

### Global CSS 檔案

對於真正的全域樣式,建議使用獨立的 `.css` 檔案:

```css
/* global.css (不用 .module.css) */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
```

```jsx
// App.jsx
import './global.css';  // 全域樣式
import styles from './App.module.css';  // 局部樣式
```

## 動態 Class Names

### 使用 classnames 套件

```bash
npm install classnames
```

```jsx
import styles from './Button.module.css';
import classNames from 'classnames';

function Button({ variant, size, disabled, children }) {
  return (
    <button 
      className={classNames(
        styles.button,
        styles[variant],
        styles[size],
        { [styles.disabled]: disabled }
      )}
    >
      {children}
    </button>
  );
}
```

### 不用套件的簡單方法

```jsx
function Button({ isPrimary, isLarge }) {
  const className = [
    styles.button,
    isPrimary && styles.primary,
    isLarge && styles.large
  ].filter(Boolean).join(' ');
  
  return <button className={className}>Click me</button>;
}
```

## 與 Sass/SCSS 整合

CSS Modules 可以和 SCSS 一起使用:

```scss
/* Button.module.scss */
$primary-color: #007bff;
$secondary-color: #6c757d;

.button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  
  &:hover {
    opacity: 0.9;
  }
}

.primary {
  composes: button;
  background: $primary-color;
  color: white;
}

.secondary {
  composes: button;
  background: $secondary-color;
  color: white;
}
```

## 最佳實踐

### 1. 一個元件一個 module.css

```
components/
├── Button/
│   ├── Button.jsx
│   └── Button.module.css
├── Card/
│   ├── Card.jsx
│   └── Card.module.css
```

### 2. 避免深層嵌套

```css
/* ❌ 過深的嵌套 */
.card .header .title .text {
  font-size: 1.5rem;
}

/* ✅ 扁平化結構 */
.cardTitle {
  font-size: 1.5rem;
}
```

### 3. 共用樣式使用 composition

```css
/* ❌ 重複程式碼 */
.buttonPrimary {
  padding: 0.5rem 1rem;
  border: none;
  background: blue;
}

.buttonSecondary {
  padding: 0.5rem 1rem;
  border: none;
  background: gray;
}

/* ✅ 使用 composition */
.button {
  padding: 0.5rem 1rem;
  border: none;
}

.primary {
  composes: button;
  background: blue;
}

.secondary {
  composes: button;
  background: gray;
}
```

### 4. 使用 CSS Variables 管理主題

```css
/* theme.module.css */
:root {
  --color-primary: #007bff;
  --color-secondary: #6c757d;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
}

/* Button.module.css */
.button {
  padding: var(--spacing-md);
  background: var(--color-primary);
}
```

## TypeScript 支援

### 自動生成型別定義

安裝套件:
```bash
npm install -D typescript-plugin-css-modules
```

配置 `tsconfig.json`:
```json
{
  "compilerOptions": {
    "plugins": [
      { "name": "typescript-plugin-css-modules" }
    ]
  }
}
```

現在可以獲得自動完成:
```tsx
import styles from './Button.module.css';

// TypeScript 會知道 styles 有哪些 class
<button className={styles.button}>  {/* ✅ 自動完成 */}
```

## Next.js 特定配置

Next.js 預設支援 CSS Modules,無需額外配置。

### App Router (Next.js 13+)

```jsx
// app/components/Button/Button.jsx
import styles from './Button.module.css';

export default function Button({ children }) {
  return <button className={styles.button}>{children}</button>;
}
```

### Pages Router (傳統方式)

```jsx
// pages/_app.js
import '../styles/globals.css';  // 全域樣式

// pages/index.js
import styles from '../styles/Home.module.css';  // 局部樣式
```

## 常見問題

### Q1: 如何套用多個 class?

```jsx
// 方法 1: 字串拼接
<div className={`${styles.card} ${styles.featured}`}>

// 方法 2: 陣列 join
<div className={[styles.card, styles.featured].join(' ')}>

// 方法 3: classnames 套件 (推薦)
<div className={classNames(styles.card, styles.featured)}>
```

### Q2: 如何覆蓋第三方套件樣式?

```css
/* ✅ 使用 :global 包裹第三方 class */
:global(.react-select__control) {
  border-color: #007bff;
}

/* 或在全域 CSS 檔案處理 */
```

### Q3: CSS Modules vs Tailwind 該選哪個?

**CSS Modules 適合:**
- 需要完全客製化的設計
- 團隊習慣傳統 CSS 寫法
- 專案已有大量自訂樣式

**Tailwind 適合:**
- 快速開發原型
- 設計系統較標準化
- 重視 utility-first 方法論

**兩者可以並用:**
```jsx
import styles from './Card.module.css';

<div className={`${styles.card} p-4 shadow-md`}>
  {/* CSS Modules + Tailwind */}
</div>
```

## 效能考量

### 1. CSS Modules 會自動 tree-shaking

未使用的 class 不會被打包進最終的 CSS 檔案。

### 2. 避免過大的 module 檔案

```css
/* ❌ 單一檔案包含所有樣式 */
/* styles.module.css - 500+ 行 */

/* ✅ 拆分成多個模組 */
/* Button.module.css */
/* Card.module.css */
/* Layout.module.css */
```

### 3. 使用 composes 而非重複樣式

```css
/* ❌ 重複定義 */
.button { padding: 1rem; }
.buttonLarge { padding: 1rem; font-size: 1.2rem; }

/* ✅ 使用 composition */
.button { padding: 1rem; }
.buttonLarge { composes: button; font-size: 1.2rem; }
```

## 總結檢查清單

- [ ] 檔案命名使用 `.module.css`
- [ ] Class 名稱使用 camelCase
- [ ] 使用 `composes` 避免重複樣式
- [ ] 全域樣式使用 `:global` 或獨立 `.css` 檔案
- [ ] 避免深層嵌套選擇器
- [ ] 使用 CSS Variables 管理主題變數
- [ ] 動態 class 使用 classnames 套件
- [ ] TypeScript 專案啟用型別定義
