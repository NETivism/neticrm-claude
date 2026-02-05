# HTML Structure and Conventions

## Table of Contents
1. [CiviCRM Class Naming](#civicrm-class-naming)
2. [Component Structures](#component-structures)
3. [Icon Usage (ZMDI)](#icon-usage-zmdi)
4. [Form Patterns](#form-patterns)
5. [Table Patterns](#table-patterns)
6. [Accessibility](#accessibility)
7. [Semantic HTML](#semantic-html)
8. [Common Layouts](#common-layouts)

## CiviCRM Class Naming

### Block-Level Classes

```html
<!-- Main container -->
<div class="crm-container">
  <!-- Generic block -->
  <div class="crm-block">
    <!-- Form-specific block -->
    <div class="crm-form-block">
      <!-- Component-specific block -->
      <div class="crm-contact-form-block">
        Content
      </div>
    </div>
  </div>
</div>
```

### Naming Pattern

**Format**: `crm-{module}-{type}-block-{field}`

Examples:
```html
<div class="crm-uf_group-form-block">...</div>
<div class="crm-contribute-form-block">...</div>
<div class="crm-event-page-block">...</div>
<tr class="crm-contact-form-block-first_name">...</tr>
```

### State Classes

```html
<!-- Success/info messages -->
<div class="messages status">Operation successful</div>

<!-- Error messages -->
<div class="messages crm-error">An error occurred</div>

<!-- Warning messages -->
<div class="messages warning">Please note...</div>

<!-- Active/inactive states -->
<div class="crm-accordion-wrapper crm-accordion-open">...</div>
<div class="crm-accordion-wrapper crm-accordion-closed">...</div>
```

### Utility Classes

```html
<!-- Hide visually but keep accessible -->
<span class="visually-hidden">Screen reader text</span>

<!-- Color utilities -->
<span class="font-red">Error text</span>

<!-- Clear floats -->
<div class="clear"></div>

<!-- Action buttons -->
<div class="action-link-button">
  <a href="#" class="button">Action</a>
</div>
```

## Component Structures

### Accordion/Collapsible

```html
<div class="crm-accordion-wrapper crm-accordion_title-accordion crm-accordion-open">
  <div class="crm-accordion-header">
    <div class="zmdi crm-accordion-pointer"></div>
    <span>Section Title</span>
  </div>
  <div class="crm-accordion-body">
    <!-- Content here -->
    <p>This section can be collapsed</p>
  </div>
</div>
```

**Classes:**
- `.crm-accordion-wrapper` - Container
- `.crm-accordion-open` - Initially expanded (default)
- `.crm-accordion-closed` - Initially collapsed
- `.crm-accordion-header` - Clickable header
- `.crm-accordion-body` - Collapsible content
- `.zmdi.crm-accordion-pointer` - Arrow icon

### Tab Interface

```html
<div id="mainTabContainer">
  <ul class="ui-tabs-nav">
    <li class="ui-tabs-active">
      <a href="#tab1">Tab 1</a>
    </li>
    <li>
      <a href="#tab2">Tab 2</a>
    </li>
  </ul>

  <div id="tab1" class="ui-tabs-panel">
    Tab 1 content
  </div>

  <div id="tab2" class="ui-tabs-panel" style="display:none;">
    Tab 2 content
  </div>
</div>
```

### Modal/Dialog

```html
<div id="myDialog" class="crm-container" style="display:none;">
  <div class="crm-block">
    <h3>Dialog Title</h3>
    <div class="crm-section">
      Dialog content
    </div>
    <div class="crm-submit-buttons">
      <button type="button" class="button">OK</button>
      <button type="button" class="button cancel">Cancel</button>
    </div>
  </div>
</div>
```

### Message Boxes

```html
<!-- Success message -->
<div class="messages status">
  <i class="zmdi zmdi-check-circle"></i>
  <strong>Success!</strong> Your changes have been saved.
</div>

<!-- Error message -->
<div class="messages crm-error">
  <i class="zmdi zmdi-alert-triangle"></i>
  <strong>Error:</strong> Unable to process request.
</div>

<!-- Info message -->
<div class="messages help">
  <i class="zmdi zmdi-info"></i>
  <strong>Note:</strong> This is informational.
</div>

<!-- Warning message -->
<div class="messages warning">
  <i class="zmdi zmdi-alert-circle"></i>
  <strong>Warning:</strong> Please review before continuing.
</div>
```

## Icon Usage (ZMDI)

### Material Design Iconic Font

netiCRM uses ZMDI (Zavoloklom Material Design Iconic Font).

### Common Icons

```html
<!-- Actions -->
<i class="zmdi zmdi-edit"></i>         <!-- Edit -->
<i class="zmdi zmdi-delete"></i>       <!-- Delete -->
<i class="zmdi zmdi-plus"></i>         <!-- Add -->
<i class="zmdi zmdi-close"></i>        <!-- Close/Remove -->
<i class="zmdi zmdi-check"></i>        <!-- Confirm -->
<i class="zmdi zmdi-search"></i>       <!-- Search -->

<!-- Status -->
<i class="zmdi zmdi-check-circle"></i>    <!-- Success -->
<i class="zmdi zmdi-alert-triangle"></i>  <!-- Error -->
<i class="zmdi zmdi-alert-circle"></i>    <!-- Warning -->
<i class="zmdi zmdi-info"></i>            <!-- Info -->

<!-- Navigation -->
<i class="zmdi zmdi-arrow-left"></i>   <!-- Back -->
<i class="zmdi zmdi-arrow-right"></i>  <!-- Forward -->
<i class="zmdi zmdi-chevron-down"></i> <!-- Expand -->
<i class="zmdi zmdi-chevron-up"></i>   <!-- Collapse -->

<!-- Common entities -->
<i class="zmdi zmdi-account"></i>      <!-- Contact/User -->
<i class="zmdi zmdi-money"></i>        <!-- Contribution -->
<i class="zmdi zmdi-calendar"></i>     <!-- Event/Date -->
<i class="zmdi zmdi-email"></i>        <!-- Email -->
<i class="zmdi zmdi-group"></i>        <!-- Group -->
```

### Icon Sizing

```html
<!-- Default size -->
<i class="zmdi zmdi-account"></i>

<!-- Sized icons -->
<i class="zmdi zmdi-account zmdi-hc-lg"></i>   <!-- Large -->
<i class="zmdi zmdi-account zmdi-hc-2x"></i>   <!-- 2x -->
<i class="zmdi zmdi-account zmdi-hc-3x"></i>   <!-- 3x -->
<i class="zmdi zmdi-account zmdi-hc-4x"></i>   <!-- 4x -->
<i class="zmdi zmdi-account zmdi-hc-5x"></i>   <!-- 5x -->

<!-- Fixed width (for alignment) -->
<i class="zmdi zmdi-account zmdi-hc-fw"></i>
```

### Spinning/Animated Icons

```html
<!-- Spinning loader -->
<i class="zmdi zmdi-spinner zmdi-hc-spin"></i>

<!-- Pulse animation -->
<i class="zmdi zmdi-spinner zmdi-hc-pulse"></i>
```

### Icon Reference

Access full icon reference at: `/civicrm/admin/zmdi`

### Icon with Text Pattern

```html
<button>
  <i class="zmdi zmdi-save"></i>
  Save Changes
</button>

<a href="#">
  <i class="zmdi zmdi-account"></i>
  View Contact
</a>

<div class="status-message">
  <i class="zmdi zmdi-check-circle"></i>
  <span>Operation completed successfully</span>
</div>
```

## Form Patterns

### Standard Form Layout

```html
<div class="crm-block crm-form-block">
  <!-- Top buttons -->
  <div class="crm-submit-buttons">
    <button type="submit" class="button">Save</button>
    <button type="button" class="cancel button">Cancel</button>
  </div>

  <!-- Form fields -->
  <table class="form-layout">
    <tr class="crm-form-block-field_name">
      <td class="label">
        <label for="field-id">Field Label</label>
      </td>
      <td class="html-adjust">
        <input type="text" id="field-id" name="field_name">
        <div class="description">Help text for this field</div>
      </td>
    </tr>
  </table>

  <!-- Bottom buttons -->
  <div class="crm-submit-buttons">
    <button type="submit" class="button">Save</button>
    <button type="button" class="cancel button">Cancel</button>
  </div>
</div>
```

### Form Field Row

```html
<tr class="crm-{module}-form-block-{fieldname}">
  <td class="label">
    <label for="email">Email Address</label>
    {* Optional: required indicator *}
    <span class="crm-marker">*</span>
  </td>
  <td class="html-adjust">
    <input type="email" id="email" name="email" required>
    <div class="description">
      Your primary email address
    </div>
  </td>
</tr>
```

### Checkbox Pattern

```html
<tr class="crm-form-block-is_active">
  <td class="label"></td>
  <td class="html-adjust">
    <input type="checkbox" id="is_active" name="is_active" value="1">
    <label for="is_active">Active</label>
  </td>
</tr>
```

### Radio Group Pattern

```html
<tr class="crm-form-block-gender">
  <td class="label">Gender</td>
  <td class="html-adjust">
    <label>
      <input type="radio" name="gender" value="1"> Female
    </label>
    <label>
      <input type="radio" name="gender" value="2"> Male
    </label>
    <label>
      <input type="radio" name="gender" value="3"> Other
    </label>
  </td>
</tr>
```

### Select Pattern

```html
<tr class="crm-form-block-country">
  <td class="label">
    <label for="country">Country</label>
  </td>
  <td class="html-adjust">
    <select id="country" name="country_id">
      <option value="">- select -</option>
      <option value="1228">Taiwan</option>
      <option value="1229">United States</option>
    </select>
  </td>
</tr>
```

## Table Patterns

### Data Table

```html
<table class="selector row-highlight">
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th class="right">Amount</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr class="odd-row">
      <td>John Doe</td>
      <td>john@example.com</td>
      <td class="right">$100.00</td>
      <td>
        <a href="#">Edit</a> |
        <a href="#">Delete</a>
      </td>
    </tr>
    <tr class="even-row">
      <td>Jane Smith</td>
      <td>jane@example.com</td>
      <td class="right">$250.00</td>
      <td>
        <a href="#">Edit</a> |
        <a href="#">Delete</a>
      </td>
    </tr>
  </tbody>
</table>
```

### Report Table

```html
<table class="report-layout">
  <thead>
    <tr class="columnheader">
      <th>Column 1</th>
      <th>Column 2</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    <tr class="crm-report">
      <td>Data 1</td>
      <td>Data 2</td>
      <td class="report-total">$500.00</td>
    </tr>
  </tbody>
  <tfoot>
    <tr class="grand-total">
      <th colspan="2">Grand Total</th>
      <th>$500.00</th>
    </tr>
  </tfoot>
</table>
```

### Form Layout Table

```html
<table class="form-layout-compressed">
  <tr>
    <td class="label">Short Label</td>
    <td>Value</td>
    <td class="label">Another Label</td>
    <td>Another Value</td>
  </tr>
</table>
```

## Accessibility

### Semantic HTML

```html
<!-- Use semantic elements -->
<header>...</header>
<nav>...</nav>
<main>...</main>
<article>...</article>
<aside>...</aside>
<footer>...</footer>
```

### Form Accessibility

```html
<!-- Associate labels with inputs -->
<label for="email">Email Address</label>
<input type="email" id="email" name="email">

<!-- Required fields -->
<input type="text" id="name" name="name" required aria-required="true">
<span class="crm-marker">*</span>

<!-- Error states -->
<input type="email" id="email" aria-invalid="true" aria-describedby="email-error">
<div id="email-error" class="crm-error">Invalid email format</div>
```

### ARIA Attributes

```html
<!-- Button roles -->
<div role="button" tabindex="0" aria-pressed="false">Toggle</div>

<!-- Hidden content -->
<div aria-hidden="true">Decorative content</div>

<!-- Live regions -->
<div aria-live="polite" aria-atomic="true">
  Status updates appear here
</div>

<!-- Expanded/collapsed -->
<button aria-expanded="false" aria-controls="content-id">
  Expand Section
</button>
<div id="content-id" hidden>
  Content
</div>
```

### Skip Links

```html
<a href="#main-content" class="visually-hidden">
  Skip to main content
</a>

<main id="main-content">
  <!-- Main content -->
</main>
```

## Semantic HTML

### Heading Hierarchy

```html
<h1>Page Title</h1>
  <h2>Section Title</h2>
    <h3>Subsection Title</h3>
    <h3>Another Subsection</h3>
  <h2>Another Section</h2>
```

**Don't skip heading levels** (e.g., h1 → h3)

### Lists

```html
<!-- Unordered list -->
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>

<!-- Ordered list -->
<ol>
  <li>Step 1</li>
  <li>Step 2</li>
</ol>

<!-- Definition list -->
<dl>
  <dt>Term</dt>
  <dd>Definition</dd>
</dl>
```

### Buttons vs Links

```html
<!-- Button: Performs action -->
<button type="button" onclick="doSomething()">
  Click Me
</button>

<!-- Link: Navigates to URL -->
<a href="/page">
  Go to Page
</a>
```

## Common Layouts

### Two-Column Layout

```html
<div class="ncg-container">
  <div class="ncg-row">
    <aside class="ncg-col-md-3">
      <!-- Sidebar -->
    </aside>
    <main class="ncg-col-md-9">
      <!-- Main content -->
    </main>
  </div>
</div>
```

### Three-Column Layout

```html
<div class="ncg-container">
  <div class="ncg-row">
    <aside class="ncg-col-lg-2">
      <!-- Left sidebar -->
    </aside>
    <main class="ncg-col-lg-8">
      <!-- Main content -->
    </main>
    <aside class="ncg-col-lg-2">
      <!-- Right sidebar -->
    </aside>
  </div>
</div>
```

### Card Layout

```html
<div class="ncg-row ncg-g-4">
  <div class="ncg-col-md-6 ncg-col-lg-4">
    <div class="crm-card">
      <div class="crm-card-header">
        <h3>Card Title</h3>
      </div>
      <div class="crm-card-body">
        Card content
      </div>
      <div class="crm-card-footer">
        <a href="#" class="button">Action</a>
      </div>
    </div>
  </div>
</div>
```

### Dashboard Layout

```html
<div class="crm-container">
  <div class="crm-block crm-content-block">
    <h1>Dashboard</h1>

    <div class="ncg-row ncg-g-4">
      <div class="ncg-col-md-4">
        <div class="dashboard-widget">
          <h3>Widget 1</h3>
          <p>Content</p>
        </div>
      </div>
      <div class="ncg-col-md-4">
        <div class="dashboard-widget">
          <h3>Widget 2</h3>
          <p>Content</p>
        </div>
      </div>
      <div class="ncg-col-md-4">
        <div class="dashboard-widget">
          <h3>Widget 3</h3>
          <p>Content</p>
        </div>
      </div>
    </div>
  </div>
</div>
```

## HTML5 Input Types

```html
<!-- Email -->
<input type="email" name="email" placeholder="user@example.com">

<!-- URL -->
<input type="url" name="website" placeholder="https://example.com">

<!-- Tel -->
<input type="tel" name="phone" placeholder="(123) 456-7890">

<!-- Number -->
<input type="number" name="age" min="0" max="120">

<!-- Date -->
<input type="date" name="birth_date">

<!-- Time -->
<input type="time" name="event_time">

<!-- Search -->
<input type="search" name="q" placeholder="Search...">

<!-- Color -->
<input type="color" name="color_preference">
```

## Code Style

- **Indentation**: 2 spaces
- **Attributes**: Double quotes (`class="my-class"`)
- **Boolean attributes**: Use short form (`required`, not `required="required"`)
- **Self-closing tags**: Optional slash (`<br>` or `<br />`)
- **Lowercase tags**: All HTML tags and attributes in lowercase
- **ID naming**: kebab-case (`my-element-id`)
- **Class naming**: Follow CiviCRM conventions (`.crm-block`)
