# CSS Standards and Best Practices

## Table of Contents
1. [CSS Variables](#css-variables)
2. [Grid System](#grid-system)
3. [Chinese Font Handling](#chinese-font-handling)
4. [Naming Conventions](#naming-conventions)
5. [Responsive Design](#responsive-design)
6. [Common Patterns](#common-patterns)
7. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

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

## Responsive Design

### Media Query Pattern

```css
/* Mobile-first approach */
.element {
  /* Mobile styles (default) */
  width: 100%;
}

@media (min-width: 768px) {
  .element {
    /* Tablet styles */
    width: 50%;
  }
}

@media (min-width: 992px) {
  .element {
    /* Desktop styles */
    width: 33.333%;
  }
}
```

### Use CSS Variables for Breakpoints

```css
@media (min-width: var(--ncg-breakpoint-md)) {
  /* Tablet and up */
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
/* DON'T */
@media (min-width: 800px) { }

/* DO - Use standard breakpoints */
@media (min-width: var(--ncg-breakpoint-md)) { }
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
