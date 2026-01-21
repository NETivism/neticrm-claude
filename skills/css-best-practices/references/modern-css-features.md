# 現代 CSS 特性支援表 (2024)

本文件列出現代 CSS 特性及其瀏覽器支援狀況,幫助判斷是否可以安全使用。

## 安全使用 (>95% 瀏覽器支援)

這些特性可以放心使用,無需考慮相容性問題。

### 佈局

| 特性 | 說明 | 支援度 |
|------|------|--------|
| **Flexbox** | 一維佈局系統 | ✅ 99%+ |
| **CSS Grid** | 二維佈局系統 | ✅ 96%+ |
| **gap** (Grid/Flex) | 間距屬性 | ✅ 95%+ |
| **aspect-ratio** | 寬高比 | ✅ 94%+ |

```css
/* Flexbox */
.container {
  display: flex;
  gap: 1rem;
  justify-content: space-between;
}

/* Grid */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

/* Aspect Ratio */
.video {
  aspect-ratio: 16 / 9;
}
```

### 選擇器

| 特性 | 說明 | 支援度 |
|------|------|--------|
| **:is()** | 簡化選擇器 | ✅ 95%+ |
| **:where()** | 零權重選擇器 | ✅ 95%+ |
| **:not()** | 否定選擇器 | ✅ 99%+ |
| **:has()** | 父層選擇器 | ✅ 90%+ |

```css
/* :is() - 簡化選擇器 */
:is(h1, h2, h3) {
  margin-block: 1rem;
}

/* :where() - 零權重,易於覆蓋 */
:where(ul, ol) {
  padding-left: 0;
}

/* :has() - 根據子元素選擇父層 */
.card:has(img) {
  display: grid;
  grid-template-columns: 200px 1fr;
}
```

### 數值與單位

| 特性 | 說明 | 支援度 |
|------|------|--------|
| **clamp()** | 動態範圍值 | ✅ 95%+ |
| **min()** / **max()** | 最小/最大值 | ✅ 96%+ |
| **calc()** | 計算 | ✅ 99%+ |
| **CSS Variables** | 自訂屬性 | ✅ 99%+ |

```css
/* clamp() - 響應式字體 */
h1 {
  font-size: clamp(1.5rem, 4vw, 3rem);
}

/* min() - 限制最大寬度 */
.container {
  width: min(100%, 1200px);
}

/* CSS Variables */
:root {
  --color-primary: #007bff;
  --spacing: 1rem;
}

.button {
  background: var(--color-primary);
  padding: var(--spacing);
}
```

### 顏色

| 特性 | 說明 | 支援度 |
|------|------|--------|
| **rgba()** / **hsla()** | 透明色 | ✅ 99%+ |
| **currentColor** | 繼承文字色 | ✅ 99%+ |
| **color-mix()** | 混色 | ⚠️ 86% |

```css
/* rgba */
.overlay {
  background: rgba(0, 0, 0, 0.5);
}

/* currentColor */
.icon {
  fill: currentColor;
}

/* color-mix (需注意支援度) */
.button {
  background: color-mix(in srgb, blue 70%, white);
}
```

### 過渡與動畫

| 特性 | 說明 | 支援度 |
|------|------|--------|
| **transition** | 過渡效果 | ✅ 99%+ |
| **animation** | 關鍵影格動畫 | ✅ 99%+ |
| **@keyframes** | 定義動畫 | ✅ 99%+ |

```css
.button {
  transition: all 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.element {
  animation: fadeIn 1s ease-in-out;
}
```

## 謹慎使用 (85-94% 支援)

這些特性大多數瀏覽器支援,但需考慮 fallback。

### 容器查詢 (Container Queries)

**支援度: ✅ 91%**

```css
.container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card-content {
    display: grid;
    grid-template-columns: 1fr 2fr;
  }
}

/* Fallback */
@supports not (container-type: inline-size) {
  @media (min-width: 768px) {
    .card-content {
      display: grid;
      grid-template-columns: 1fr 2fr;
    }
  }
}
```

### Logical Properties (邏輯屬性)

**支援度: ✅ 94%**

```css
/* 邏輯屬性 - 支援 RTL */
.element {
  margin-inline-start: 1rem;  /* 取代 margin-left */
  margin-inline-end: 1rem;    /* 取代 margin-right */
  margin-block-start: 2rem;   /* 取代 margin-top */
  margin-block-end: 2rem;     /* 取代 margin-bottom */
}

/* 簡寫 */
.element {
  margin-inline: 1rem;   /* 左右 margin */
  margin-block: 2rem;    /* 上下 margin */
  padding-block: 1rem;
  border-inline: 1px solid;
}
```

### Subgrid

**支援度: ⚠️ 85%**

```css
.parent {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.child {
  display: grid;
  grid-column: span 3;
  grid-template-columns: subgrid;  /* 繼承父層的欄 */
}

/* Fallback */
@supports not (grid-template-columns: subgrid) {
  .child {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### backdrop-filter

**支援度: ⚠️ 94%**

```css
.glass-effect {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.7);
}

/* Fallback */
@supports not (backdrop-filter: blur(10px)) {
  .glass-effect {
    background: rgba(255, 255, 255, 0.9);
  }
}
```

## 實驗性 / 部分支援 (<85%)

這些特性仍在發展中,使用時需提供完整的 fallback。

### @layer (Cascade Layers)

**支援度: ⚠️ 90%**

```css
@layer reset, base, components, utilities;

@layer reset {
  * { margin: 0; padding: 0; }
}

@layer components {
  .button { padding: 0.5rem 1rem; }
}

@layer utilities {
  .hidden { display: none !important; }
}
```

### :focus-visible

**支援度: ✅ 96%**

```css
/* 只在鍵盤 focus 時顯示外框 */
button:focus-visible {
  outline: 2px solid blue;
  outline-offset: 2px;
}

button:focus:not(:focus-visible) {
  outline: none;
}
```

### color() / oklch()

**支援度: ⚠️ 80%**

```css
/* 更寬廣的色域 */
.element {
  color: oklch(0.6 0.2 200);
}

/* Fallback */
.element {
  color: #4a90e2;  /* 先定義 fallback */
  color: oklch(0.6 0.2 200);
}
```

### @property (註冊自訂屬性)

**支援度: ⚠️ 87%**

```css
@property --gradient-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

.gradient {
  background: linear-gradient(var(--gradient-angle), blue, red);
  animation: rotate 2s infinite;
}

@keyframes rotate {
  to { --gradient-angle: 360deg; }
}
```

### content-visibility

**支援度: ⚠️ 85%**

```css
/* 效能優化 - 延遲渲染 */
.long-list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px;
}
```

### View Transitions API

**支援度: ⚠️ 76%**

```css
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.3s;
}
```

## 避免使用 (已淘汰或不推薦)

### 已淘汰特性

```css
/* ❌ 不要使用 */
-webkit-box-orient: vertical;   /* 舊版 Flexbox */
-ms-grid-columns: 1fr 1fr;      /* IE Grid */
filter: progid:DXImageTransform; /* IE 濾鏡 */
zoom: 1.5;                       /* 非標準 */
```

### 不推薦的佈局方法

```css
/* ❌ 避免用於佈局 */
float: left;                    /* 使用 Flexbox/Grid */
display: table;                 /* 使用 Grid */
position: absolute;             /* 過度使用會難維護 */
margin: 0 auto;                 /* 使用 Flexbox justify-content */
```

## 瀏覽器支援檢查工具

### @supports 查詢

```css
/* 特性檢測 */
@supports (display: grid) {
  .container {
    display: grid;
  }
}

@supports not (display: grid) {
  .container {
    display: flex;
    flex-wrap: wrap;
  }
}

/* 多條件檢測 */
@supports (display: grid) and (gap: 1rem) {
  .grid {
    display: grid;
    gap: 1rem;
  }
}
```

### JavaScript 檢測

```javascript
// 檢測 CSS 特性支援
if (CSS.supports('display', 'grid')) {
  console.log('Grid 已支援');
}

// 檢測 Container Queries
if ('container' in document.documentElement.style) {
  console.log('Container Queries 已支援');
}
```

## 實用資源

- **Can I Use**: https://caniuse.com/ - 瀏覽器支援查詢
- **MDN Web Docs**: https://developer.mozilla.org/zh-TW/ - 完整文件
- **Baseline**: https://web.dev/baseline/ - 跨瀏覽器支援狀態

## 決策流程圖

```
需要使用新特性?
│
├─ 支援度 >95%? → ✅ 直接使用
│
├─ 支援度 85-94%? 
│  └─ 是否可提供 fallback? 
│     ├─ 是 → ⚠️ 謹慎使用 + fallback
│     └─ 否 → ❌ 不使用
│
└─ 支援度 <85%?
   └─ 是否為漸進增強?
      ├─ 是 → ⚠️ 可使用 (非核心功能)
      └─ 否 → ❌ 等到支援度提升
```

## 總結建議

1. **優先使用高支援度特性** (>95%): Flexbox, Grid, CSS Variables
2. **謹慎使用中等支援度特性** (85-94%): 提供 fallback
3. **漸進增強使用低支援度特性** (<85%): 僅用於非核心功能
4. **使用 @supports 檢測**: 確保優雅降級
5. **定期查閱 Can I Use**: 支援度會隨時間改善
6. **測試目標瀏覽器**: 確認實際使用者環境
