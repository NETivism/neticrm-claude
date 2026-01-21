# Tailwind CSS Guidelines

## 避免 Class 名稱幻覺 (Hallucination)

### 常見幻覺範例

AI 經常「發明」不存在的 Tailwind class,以下是常見錯誤:

#### ❌ 不存在的 Class

```html
<!-- 這些 class 都不存在! -->
<div class="text-shadow-md">           <!-- Tailwind 沒有 text-shadow utilities -->
<div class="border-gradient">          <!-- 不存在 gradient border -->
<div class="bg-blur">                  <!-- 應該用 backdrop-blur -->
<div class="flex-center">              <!-- 不存在,應分開用 justify-center items-center -->
<div class="transition-smooth">        <!-- 不存在,應用 transition-all 或 transition -->
<div class="shadow-soft">              <!-- 不存在,只有 shadow-sm, shadow, shadow-md 等 -->
<div class="rounded-circle">           <!-- 應該用 rounded-full -->
<div class="text-gradient">            <!-- 需要用 bg-gradient + bg-clip-text -->
```

#### ✅ 正確的 Class

```html
<!-- 正確使用現有 utilities -->
<div class="backdrop-blur-sm">         <!-- 背景模糊 -->
<div class="justify-center items-center flex"> <!-- 置中 -->
<div class="transition-all duration-300">      <!-- 過渡效果 -->
<div class="shadow-md">                <!-- 陰影 -->
<div class="rounded-full">             <!-- 圓形 -->
<div class="bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">
  <!-- 漸層文字 -->
</div>
```

## Tailwind 核心 Class 速查

### 佈局 (Layout)

```html
<!-- Container -->
<div class="container mx-auto">

<!-- Display -->
<div class="block">
<div class="inline-block">
<div class="flex">
<div class="grid">
<div class="hidden">

<!-- Position -->
<div class="static">
<div class="relative">
<div class="absolute">
<div class="fixed">
<div class="sticky">
```

### Flexbox

```html
<!-- Direction -->
<div class="flex flex-row">       <!-- 預設 -->
<div class="flex flex-col">

<!-- Justify (主軸) -->
<div class="flex justify-start">
<div class="flex justify-center">
<div class="flex justify-between">
<div class="flex justify-around">

<!-- Align (交叉軸) -->
<div class="flex items-start">
<div class="flex items-center">
<div class="flex items-end">
<div class="flex items-stretch">

<!-- Wrap -->
<div class="flex flex-wrap">
<div class="flex flex-nowrap">

<!-- Gap -->
<div class="flex gap-4">
<div class="flex gap-x-4 gap-y-2">
```

### Grid

```html
<!-- Columns -->
<div class="grid grid-cols-1">
<div class="grid grid-cols-2">
<div class="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6">

<!-- Auto-fit responsive grid -->
<div class="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))]">

<!-- Gap -->
<div class="grid gap-4">

<!-- Span -->
<div class="col-span-2">
<div class="row-span-3">
```

### Spacing (間距)

數字對應: `1` = 0.25rem (4px)

```html
<!-- Margin -->
<div class="m-4">        <!-- margin: 1rem (16px) -->
<div class="mx-4">       <!-- margin-left + margin-right -->
<div class="my-4">       <!-- margin-top + margin-bottom -->
<div class="mt-4">       <!-- margin-top -->
<div class="mr-4">       <!-- margin-right -->
<div class="mb-4">       <!-- margin-bottom -->
<div class="ml-4">       <!-- margin-left -->

<!-- Padding (同理) -->
<div class="p-4">
<div class="px-4 py-2">

<!-- 負值 margin -->
<div class="-mt-4">

<!-- Auto margin (置中) -->
<div class="mx-auto">
```

### Sizing

```html
<!-- Width -->
<div class="w-full">        <!-- 100% -->
<div class="w-1/2">         <!-- 50% -->
<div class="w-64">          <!-- 16rem (256px) -->
<div class="w-screen">      <!-- 100vw -->
<div class="w-fit">         <!-- fit-content -->
<div class="w-min">         <!-- min-content -->
<div class="w-max">         <!-- max-content -->

<!-- Height (同理) -->
<div class="h-screen">      <!-- 100vh -->
<div class="h-full">

<!-- Min/Max Width -->
<div class="min-w-0 max-w-md">
```

### Typography

```html
<!-- Font Size -->
<div class="text-xs">       <!-- 0.75rem (12px) -->
<div class="text-sm">       <!-- 0.875rem (14px) -->
<div class="text-base">     <!-- 1rem (16px) -->
<div class="text-lg">       <!-- 1.125rem (18px) -->
<div class="text-xl">       <!-- 1.25rem (20px) -->
<div class="text-2xl">      <!-- 1.5rem (24px) -->

<!-- Font Weight -->
<div class="font-normal">   <!-- 400 -->
<div class="font-medium">   <!-- 500 -->
<div class="font-semibold"> <!-- 600 -->
<div class="font-bold">     <!-- 700 -->

<!-- Text Align -->
<div class="text-left">
<div class="text-center">
<div class="text-right">

<!-- Text Color -->
<div class="text-gray-900">
<div class="text-red-500">

<!-- Line Height -->
<div class="leading-tight">
<div class="leading-normal">
<div class="leading-relaxed">
```

### Colors

色彩範圍: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950

```html
<!-- Background -->
<div class="bg-blue-500">
<div class="bg-gray-100">

<!-- Text -->
<div class="text-red-600">

<!-- Border -->
<div class="border-green-500">

<!-- Ring (focus 狀態常用) -->
<div class="ring-2 ring-blue-500">
```

### Borders

```html
<!-- Border Width -->
<div class="border">        <!-- 1px -->
<div class="border-2">      <!-- 2px -->
<div class="border-t">      <!-- 只有 top -->

<!-- Border Radius -->
<div class="rounded">       <!-- 4px -->
<div class="rounded-md">    <!-- 6px -->
<div class="rounded-lg">    <!-- 8px -->
<div class="rounded-full">  <!-- 9999px (圓形) -->
<div class="rounded-t-lg">  <!-- 只有 top -->
```

### Effects

```html
<!-- Shadow -->
<div class="shadow-sm">
<div class="shadow">
<div class="shadow-md">
<div class="shadow-lg">
<div class="shadow-xl">
<div class="shadow-2xl">

<!-- Opacity -->
<div class="opacity-0">     <!-- 完全透明 -->
<div class="opacity-50">    <!-- 半透明 -->
<div class="opacity-100">   <!-- 不透明 -->

<!-- Backdrop -->
<div class="backdrop-blur-sm">
<div class="backdrop-brightness-50">
```

### Transitions

```html
<!-- Transition Property -->
<div class="transition-none">
<div class="transition-all">
<div class="transition-colors">
<div class="transition-opacity">
<div class="transition-transform">

<!-- Duration -->
<div class="duration-75">
<div class="duration-150">
<div class="duration-300">  <!-- 常用 -->
<div class="duration-500">

<!-- Timing Function -->
<div class="ease-linear">
<div class="ease-in">
<div class="ease-out">
<div class="ease-in-out">

<!-- 組合使用 -->
<button class="transition-all duration-300 hover:scale-105 hover:shadow-lg">
```

## 響應式設計

Tailwind 使用 mobile-first breakpoints:

```html
<!-- Breakpoints: sm(640px), md(768px), lg(1024px), xl(1280px), 2xl(1536px) -->

<div class="w-full md:w-1/2 lg:w-1/3">
  <!-- mobile: 100%, tablet: 50%, desktop: 33.33% -->
</div>

<div class="text-sm md:text-base lg:text-lg">
  <!-- 響應式字體大小 -->
</div>

<div class="hidden md:block">
  <!-- mobile 隱藏, tablet+ 顯示 -->
</div>
```

## 何時使用 @apply

### ✅ 適合使用 @apply

```css
/* 1. 重複使用的 component 樣式 */
.btn-primary {
  @apply px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors;
}

/* 2. 第三方套件的客製化 */
.react-select__control {
  @apply border-gray-300 rounded-md shadow-sm;
}

/* 3. 基礎樣式重置 */
@layer base {
  h1 {
    @apply text-3xl font-bold mb-4;
  }
}
```

### ❌ 避免使用 @apply

```css
/* ❌ 不要為了「整潔」而過度使用 @apply */
.card {
  @apply w-full h-full p-4 bg-white;  
}
/* 這樣不如直接在 HTML 用 class="w-full h-full p-4 bg-white" */

/* ❌ 不要用 @apply 重建整個設計系統 */
.my-custom-spacing-4 {
  @apply p-4;
}
/* 這違反了 Tailwind 的設計理念 */
```

**原則**: 只在真正需要提取 component 時使用 @apply,大部分情況直接用 utility classes 更好。

## 常見模式

### 1. Card Component

```html
<div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
  <h3 class="text-xl font-semibold mb-2">Card Title</h3>
  <p class="text-gray-600">Card content goes here.</p>
</div>
```

### 2. Button Variants

```html
<!-- Primary -->
<button class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors">
  Primary
</button>

<!-- Secondary -->
<button class="px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300">
  Secondary
</button>

<!-- Outline -->
<button class="px-4 py-2 border-2 border-blue-500 text-blue-500 rounded-md hover:bg-blue-50">
  Outline
</button>
```

### 3. Centered Container

```html
<div class="container mx-auto px-4 max-w-7xl">
  <!-- Content -->
</div>
```

### 4. Responsive Navigation

```html
<nav class="flex flex-col md:flex-row items-start md:items-center gap-4">
  <a href="#" class="text-gray-700 hover:text-blue-500">Home</a>
  <a href="#" class="text-gray-700 hover:text-blue-500">About</a>
  <a href="#" class="text-gray-700 hover:text-blue-500">Contact</a>
</nav>
```

### 5. Grid Gallery

```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="aspect-square bg-gray-200 rounded-lg"></div>
  <div class="aspect-square bg-gray-200 rounded-lg"></div>
  <div class="aspect-square bg-gray-200 rounded-lg"></div>
</div>
```

## 效能優化

### 1. 使用 PurgeCSS (內建於 Tailwind v3)

```js
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
    './public/index.html',
  ],
  // ...
}
```

### 2. 使用 JIT Mode (Just-In-Time)

Tailwind v3+ 預設啟用,按需生成 CSS,大幅減小檔案大小。

### 3. 使用 @layer 組織樣式

```css
@layer base {
  /* 基礎樣式 */
}

@layer components {
  /* Component classes */
}

@layer utilities {
  /* Custom utilities */
}
```

## Dark Mode

```html
<!-- 在 HTML 加上 dark class -->
<html class="dark">

<!-- 使用 dark: 前綴 -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  <!-- Content -->
</div>
```

```js
// tailwind.config.js
module.exports = {
  darkMode: 'class', // 或 'media' (使用系統偏好)
  // ...
}
```

## 除錯技巧

### 1. 檢查 class 是否被 purge

開啟瀏覽器 DevTools,檢查 Computed styles 確認 class 是否生效。

### 2. 使用 Tailwind CSS IntelliSense

VS Code 擴充套件,提供自動完成和 class 預覽,**強烈建議安裝以避免幻覺**。

### 3. 參考官方文件

遇到不確定的 class,先查 [Tailwind CSS 官方文件](https://tailwindcss.com/docs) 確認是否存在。

## 總結檢查清單

- [ ] 所有 class 名稱都確實存在於 Tailwind 中
- [ ] 沒有使用 `@apply` 過度提取樣式
- [ ] 響應式設計使用 mobile-first
- [ ] 顏色使用一致的 scale (50-950)
- [ ] Spacing 使用 Tailwind 的數字系統
- [ ] 沒有自訂 arbitrary values 除非真的必要 (如 `w-[237px]`)
