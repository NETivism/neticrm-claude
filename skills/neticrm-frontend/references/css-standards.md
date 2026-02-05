# CSS Standards and Best Practices

## Table of Contents
1. [CSS Variables](#css-variables)
2. [Grid System](#grid-system)
3. [Chinese Font Handling](#chinese-font-handling)
4. [Naming Conventions](#naming-conventions)
5. [Responsive Design (Mobile First)](#responsive-design)
   - Mobile First Principle (MANDATORY)
   - Standard Breakpoints
   - Media Query Patterns
6. [Common Patterns](#common-patterns)
7. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
   - Desktop First (max-width)
   - Custom Breakpoints

## CSS Variables

netiCRM uses CSS Custom Properties extensively. Always use defined variables instead of hardcoded values.

### Variable Categories

#### Color Variables
```css
/* Error states */
--color-error: #f44336
--color-error-dark: #b71c1c

/* Form inputs */
--color-form-input-border: #999

/* CRM-specific (customizable via --neticrm-* overrides) */
--color-crm-special-contribute-primary: var(--neticrm-color-crm-special-contribute-primary, #3f51b5)
--color-crm-special-contribute-info-link: var(--neticrm-color-crm-special-contribute-info-link, #c4ccff)
```

#### Recurring Form Module (RFM) Variables
```css
--rfm-card-bg: #fff
--rfm-card-border-color: #ccc
--rfm-card-border-radius: .625rem
--rfm-card-shadow: rgba(0, 0, 0, .07) 0 1px 8px
--rfm-primary-blue: #4a7bbb
--rfm-text-dark: #333
--rfm-spacing-base: clamp(.75rem, 2vw, 1.25rem)
--rfm-line-height: 1.5
--rfm-input-border: #ddd
--rfm-input-bg: #fcfcfc
--rfm-track-bg: #e9e9e9
--rfm-track-height: 4px
--rfm-icon-size: 1.75rem
--rfm-field-gap: 1.5rem
```

#### Contribution Page (PCP) Variables
```css
--pcp-progress-padding: 40px
--pcp-progress-amount-height: 40px
--pcp-progress-bar-height: 30px
--pcp-leading-height: calc(100dvh - var(--header-min-height) - ...)
```

#### Grid System Variables
```css
/* Breakpoints */
--ncg-breakpoint-sm: 576px
--ncg-breakpoint-md: 768px
--ncg-breakpoint-lg: 992px
--ncg-breakpoint-xl: 1200px
--ncg-breakpoint-xxl: 1400px

/* Container max-width */
--ncg-container-sm: 540px
--ncg-container-md: 720px
--ncg-container-lg: 960px
--ncg-container-xl: 1140px
--ncg-container-xxl: 1320px

/* Gutters */
--ncg-gutter-x: 1.5rem
--ncg-gutter-y: 0
```

### Variable Naming Convention

- **`--ncg-*`**: netiCRM Grid system variables
- **`--rfm-*`**: Recurring Form Module variables
- **`--pcp-*`**: Public Contribution Page variables
- **`--color-crm-*`**: CRM-specific color variables
- **`--neticrm-*`**: User-customizable override variables

**Best Practice**: When adding new variables, follow these prefixes to maintain consistency.

## Grid System

netiCRM uses a custom Bootstrap 5-inspired grid system with `ncg-` prefix to avoid conflicts.

### Basic Structure

```html
<div class="ncg-container">
  <div class="ncg-row">
    <div class="ncg-col-md-6">Column 1</div>
    <div class="ncg-col-md-6">Column 2</div>
  </div>
</div>
```

### Container Types

```html
<!-- Fixed-width container (responsive max-width) -->
<div class="ncg-container">...</div>

<!-- Full-width container -->
<div class="ncg-container-fluid">...</div>
```

### Column System

```html
<!-- Equal-width columns -->
<div class="ncg-col">Auto</div>
<div class="ncg-col">Auto</div>

<!-- Auto-width based on content -->
<div class="ncg-col-auto">Auto-width</div>

<!-- Fixed columns (1-12) -->
<div class="ncg-col-3">3/12</div>
<div class="ncg-col-9">9/12</div>

<!-- Responsive columns -->
<div class="ncg-col-12 ncg-col-md-6 ncg-col-lg-4">
  12 cols on mobile, 6 on tablet, 4 on desktop
</div>
```

### Gutter Control

```html
<!-- No gutters -->
<div class="ncg-row ncg-g-0">...</div>

<!-- Custom gutter spacing (0-5) -->
<div class="ncg-row ncg-g-3">...</div>  <!-- 1rem gutter -->
<div class="ncg-row ncg-gx-2">...</div> <!-- 0.5rem horizontal gutter -->
<div class="ncg-row ncg-gy-4">...</div> <!-- 1.5rem vertical gutter -->
```

### Responsive Breakpoints

| Breakpoint | Prefix | Min Width |
|------------|--------|-----------|
| Extra small | (none) | <576px |
| Small | `-sm-` | ≥576px |
| Medium | `-md-` | ≥768px |
| Large | `-lg-` | ≥992px |
| Extra large | `-xl-` | ≥1200px |
| Extra extra large | `-xxl-` | ≥1400px |

### Example: Responsive Layout

```html
<div class="ncg-container">
  <div class="ncg-row ncg-g-4">
    <!-- Sidebar: full width on mobile, 1/4 on desktop -->
    <aside class="ncg-col-12 ncg-col-lg-3">
      Sidebar
    </aside>

    <!-- Main: full width on mobile, 3/4 on desktop -->
    <main class="ncg-col-12 ncg-col-lg-9">
      Main content
    </main>
  </div>
</div>
```

## Chinese Font Handling

### Font Family Definition

Always use the standardized font stack for Chinese support:

```css
font-family: "PingFang TC", "Heiti TC", "Noto Sans TC", "Noto Sans CJK TC",
             NotoSansCJKtc-Regular, source-han-sans-traditional,
             "Microsoft JhengHei Fixed", "Microsoft JhengHei", "微軟正黑體",
             sans-serif;
```

This is available as a CSS variable:
```css
font-family: var(--font-sans-serif);
```

### Microsoft JhengHei Bold Spacing Fix

Microsoft JhengHei has spacing issues with certain characters (碧, 筵, 綰) when bold. Use the "Fixed" version:

```css
@font-face {
  font-family: "Microsoft JhengHei Fixed";
  unicode-range: U+7db0, U+78A7, U+7B75; /* 碧筵綰 */
  font-style: normal;
  font-weight: bold;
  src: local(Yu Gothic), local(MS Gothic);
}

@font-face {
  font-family: "Microsoft JhengHei Fixed";
  unicode-range: U+7db0, U+78A7, U+7B75;
  font-style: normal;
  font-weight: normal;
  src: local(Microsoft JhengHei), local(微軟正黑體);
}
```

**Why this matters**: Without this fix, certain Chinese characters display with incorrect spacing in bold text, affecting readability.

## Naming Conventions

### Class Naming Pattern

Follow CiviCRM conventions:

```css
/* Component-level */
.crm-container { }
.crm-block { }
.crm-form-block { }

/* Module-specific */
.crm-uf_group-form-block { }
.crm-contribute-form { }

/* State classes */
.crm-error { }
.crm-success { }
.messages.status { }

/* Utility classes */
.visually-hidden { }
.font-red { }
```

### ID vs Class

- **IDs**: Use for unique page elements or JavaScript hooks
  ```css
  #tiptip_holder
  #main-inner
  ```

- **Classes**: Use for styling and reusable components
  ```css
  .ncg-container
  .crm-accordion-wrapper
  ```

## CSS Selector Scoping

### The `.crm-container` Requirement

**IMPORTANT**: All CiviCRM-specific CSS selectors must be prefixed with `.crm-container` to ensure proper style isolation.

#### Why `.crm-container` is Required

CiviCRM uses `.crm-container` as a style isolation container for two critical reasons:

1. **Prevent polluting host websites**: CiviCRM is often embedded in various CMS platforms (WordPress, Drupal, Joomla, etc.)
2. **Protect from external styles**: Prevents CiviCRM styles from being overridden by host website CSS

#### Correct Selector Patterns

```css
/* ❌ WRONG - Pollutes global scope, can be overridden by external CSS */
.crm-submit-buttons {
  display: flex;
  gap: 0.5rem;
}

/* ✅ CORRECT - Properly scoped to CiviCRM container */
.crm-container .crm-submit-buttons {
  display: flex;
  gap: 0.5rem;
}

/* ✅ CORRECT - Using :has() selector for body-level styles */
body:has(.crm-container) {
  font-family: sans-serif;
  line-height: 1.5;
  background: #f5f5f5;
}
```

#### When to Use `:has()` Selector

For styles that must apply to `<body>` or other parent elements, use `:has(.crm-container)`:

```css
/* ✅ CORRECT - Only affects pages with CRM content */
body:has(.crm-container) {
  /* Global page styles when CRM is present */
}

/* ❌ WRONG - Affects ALL pages on host website */
body {
  /* This will pollute non-CRM pages */
}
```

**Why this matters**:
- CiviCRM is often embedded in other websites
- Without `:has()`, styles would affect the host website's all pages
- Using `:has(.crm-container)` ensures styles only apply when CRM content is present

#### Best Practices

1. **Always prefix with `.crm-container`** for CiviCRM-specific components
2. **Use `:has(.crm-container)`** for body/html-level styles
3. **Test in embedded contexts** to ensure no style leakage
4. **Avoid bare class selectors** that might conflict with host sites

## Responsive Design

### Mobile First Principle (Recommended)

**netiCRM recommends a mobile-first approach.** This means:

1. **Default styles target mobile devices** (smallest screens)
2. **Media queries use `min-width`** to progressively enhance for larger screens
3. **Avoid using `max-width`** media queries (desktop-first anti-pattern)

**Why mobile first?**
- Mobile traffic is significant in Taiwan and globally
- Better performance (mobile devices load less CSS)
- Progressive enhancement vs graceful degradation
- Easier to maintain and debug

### Standard Breakpoints (Recommended)

**Recommendation**: Use netiCRM grid system breakpoints. Avoid creating custom breakpoints.

```css
/* netiCRM Grid System Breakpoints */
--ncg-breakpoint-sm: 576px   /* Small devices (landscape phones) */
--ncg-breakpoint-md: 768px   /* Medium devices (tablets) */
--ncg-breakpoint-lg: 992px   /* Large devices (desktops) */
--ncg-breakpoint-xl: 1200px  /* Extra large devices */
--ncg-breakpoint-xxl: 1400px /* Extra extra large devices */
```

### Mobile First Media Query Pattern

```css
/* ✅ CORRECT - Mobile first with min-width */
.element {
  /* Mobile styles (default, <576px) */
  width: 100%;
  padding: 1rem;
  font-size: 14px;
}

@media (min-width: 768px) {
  /* Tablet and up (≥768px) */
  .element {
    width: 50%;
    padding: 1.5rem;
    font-size: 16px;
  }
}

@media (min-width: 992px) {
  /* Desktop and up (≥992px) */
  .element {
    width: 33.333%;
    padding: 2rem;
    font-size: 18px;
  }
}
```

### Using CSS Variables for Breakpoints (Recommended)

Recommended: Use CSS variables for consistency and maintainability:

```css
/* ✅ DO - Use CSS variables */
@media (min-width: var(--ncg-breakpoint-sm)) {
  /* Small devices and up */
}

@media (min-width: var(--ncg-breakpoint-md)) {
  /* Tablets and up */
}

@media (min-width: var(--ncg-breakpoint-lg)) {
  /* Desktops and up */
}

/* ❌ DON'T - Hardcoded values */
@media (min-width: 768px) { }
@media (min-width: 992px) { }
```

### Complete Responsive Example

```css
/* Mobile first: start with mobile styles */
.card {
  /* Mobile (default, all devices) */
  width: 100%;
  padding: 1rem;
  margin-bottom: 1rem;
  font-size: 14px;
}

.card-title {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

/* Small devices and up (≥576px) */
@media (min-width: var(--ncg-breakpoint-sm)) {
  .card {
    padding: 1.25rem;
  }
}

/* Tablets and up (≥768px) */
@media (min-width: var(--ncg-breakpoint-md)) {
  .card {
    width: 48%;
    padding: 1.5rem;
    font-size: 15px;
  }

  .card-title {
    font-size: 1.5rem;
  }
}

/* Desktops and up (≥992px) */
@media (min-width: var(--ncg-breakpoint-lg)) {
  .card {
    width: 31%;
    padding: 2rem;
    font-size: 16px;
  }

  .card-title {
    font-size: 1.75rem;
  }
}

/* Extra large screens (≥1200px) */
@media (min-width: var(--ncg-breakpoint-xl)) {
  .card {
    width: 23%;
  }
}
```

### Modern CSS Units

Prefer modern units for responsiveness:

```css
/* ✅ Fluid typography */
font-size: clamp(1rem, 2vw, 1.5rem);

/* ✅ Responsive spacing */
padding: clamp(1rem, 3vw, 2rem);

/* ✅ Dynamic viewport height */
height: calc(100dvh - var(--header-min-height));

/* ❌ Avoid fixed pixel values */
font-size: 16px; /* Inflexible */
```

## Common Patterns

### Loading Placeholder

```css
body:not(.special-page-finish) .crm-container>form>* {
  opacity: 0;
  position: absolute;
  z-index: -1;
}

.loading-placeholder-wrapper {
  transition: opacity .5s linear;
}

body:not(.special-page-finish) .crm-container>form>.loading-placeholder-wrapper {
  opacity: 1;
}

.special-page-finish .loading-placeholder-wrapper {
  opacity: 0;
}
```

### Accordion Pattern

```css
.crm-accordion-wrapper {
  border: 1px solid #ccc;
  margin-bottom: 1em;
}

.crm-accordion-header {
  padding: 10px;
  cursor: pointer;
  background: #f5f5f5;
}

.crm-accordion-body {
  padding: 15px;
  display: none;
}

.crm-accordion-open .crm-accordion-body {
  display: block;
}
```

### Form Layout

```css
.form-layout {
  width: 100%;
}

.form-layout td.label {
  text-align: right;
  padding-right: 1em;
  vertical-align: top;
  font-weight: bold;
}

.form-layout td.html-adjust {
  padding: 0.5em;
}
```

## Anti-Patterns to Avoid

### ❌ Hardcoding Colors

```css
/* DON'T */
.button-primary {
  background: #3f51b5;
}

/* DO */
.button-primary {
  background: var(--color-crm-special-contribute-primary);
}
```

### ❌ Custom Grid Classes

```css
/* DON'T - Creating custom grid */
.my-grid {
  display: flex;
  gap: 20px;
}
.my-col {
  flex: 1;
}

/* DO - Use existing ncg-* classes */
<div class="ncg-row ncg-g-4">
  <div class="ncg-col">...</div>
</div>
```

### ❌ Excessive !important

```css
/* DON'T */
.my-class {
  color: red !important;
  font-size: 16px !important;
}

/* DO - Fix specificity issues properly */
.crm-container .my-class {
  color: red;
  font-size: 16px;
}
```

### ❌ Deep Nesting

```css
/* DON'T - >3 levels of nesting */
.container .section .block .item .link {
  color: blue;
}

/* DO - Flatten hierarchy */
.item-link {
  color: blue;
}
```

### ❌ Ignoring Chinese Fonts

```css
/* DON'T */
body {
  font-family: Arial, sans-serif; /* No Chinese support */
}

/* DO */
body {
  font-family: var(--font-sans-serif);
}
```

### ❌ Pixel-based Media Queries

```css
/* DON'T - Hardcoded breakpoints */
@media (min-width: 800px) { }
@media (min-width: 1024px) { }

/* DO - Use netiCRM grid system variables */
@media (min-width: var(--ncg-breakpoint-md)) { }
@media (min-width: var(--ncg-breakpoint-lg)) { }
```

### ❌ Desktop First (max-width)

```css
/* DON'T - Desktop first approach with max-width */
.element {
  /* Desktop styles (default) */
  width: 33.333%;
  padding: 2rem;
  font-size: 18px;
}

@media (max-width: 991px) {
  .element {
    width: 50%;
    padding: 1.5rem;
  }
}

@media (max-width: 767px) {
  .element {
    width: 100%;
    padding: 1rem;
    font-size: 14px;
  }
}

/* DO - Mobile first with min-width */
.element {
  /* Mobile styles (default) */
  width: 100%;
  padding: 1rem;
  font-size: 14px;
}

@media (min-width: var(--ncg-breakpoint-md)) {
  .element {
    width: 50%;
    padding: 1.5rem;
  }
}

@media (min-width: var(--ncg-breakpoint-lg)) {
  .element {
    width: 33.333%;
    padding: 2rem;
    font-size: 18px;
  }
}
```

### ❌ Custom Breakpoints

```css
/* DON'T - Creating custom breakpoints */
@media (min-width: 650px) { }
@media (min-width: 900px) { }
@media (min-width: 1100px) { }

/* DO - Use only netiCRM grid system breakpoints */
@media (min-width: var(--ncg-breakpoint-sm)) { }  /* 576px */
@media (min-width: var(--ncg-breakpoint-md)) { }  /* 768px */
@media (min-width: var(--ncg-breakpoint-lg)) { }  /* 992px */
@media (min-width: var(--ncg-breakpoint-xl)) { }  /* 1200px */
```

## Performance Considerations

1. **Minimize specificity**: Keep selectors simple
2. **Avoid universal selectors**: `*` is expensive
3. **Use CSS variables**: Reduces duplication
4. **Combine similar rules**: Group related styles
5. **Avoid layout thrashing**: Batch DOM reads/writes in JS

## Code Style

- **Indentation**: 2 spaces (never tabs)
- **Property order**: Logical grouping (positioning → box model → typography → visual)
- **Semicolons**: Always required (even on last property)
- **Quotes**: Double quotes for strings and URLs
- **Color format**: Prefer hex for solid colors, `rgba()` for transparency
- **Zero units**: Omit units for zero values (`margin: 0` not `margin: 0px`)
