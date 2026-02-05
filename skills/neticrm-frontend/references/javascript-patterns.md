# JavaScript Patterns and Best Practices

## Table of Contents
1. [jQuery Usage](#jquery-usage)
2. [CiviCRM API Patterns](#civicrm-api-patterns)
3. [Event Handling](#event-handling)
4. [Plugin Development](#plugin-development)
5. [Common Utilities](#common-utilities)
6. [Code Style](#code-style)
7. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

## jQuery Usage

### The `cj()` Function

CiviCRM uses `cj()` instead of `$` to avoid conflicts with other libraries (Drupal, Joomla, etc.).

#### In Smarty Templates

```smarty
<script type="text/javascript">
{literal}
cj(document).ready(function($) {
  // Use $ inside this closure
  $('#my-element').click(function() {
    console.log('Clicked');
  });
});
{/literal}
</script>
```

**Pattern breakdown:**
- `{literal}...{/literal}` prevents Smarty from parsing `{` and `}` in JavaScript
- `cj(document).ready()` ensures DOM is ready
- Function parameter `$` allows using `$` inside the closure for cleaner code
- Use `cj()` outside closures, `$` inside closures

#### In Standalone JS Files

```javascript
// Use cj() throughout the file
(function($) {
  'use strict';

  // $ is available here via parameter
  $(document).ready(function() {
    $('.my-class').each(function() {
      // Your code
    });
  });

})(cj); // Pass cj as $ parameter
```

### jQuery Version

CiviCRM bundles jQuery. Check version compatibility when using newer jQuery features.

## CiviCRM API Patterns

### The `.crmAPI()` Method

Custom jQuery method for calling CiviCRM API v3.

#### Basic Usage

```javascript
cj().crmAPI('Entity', 'action', {
  param1: value1,
  param2: value2
}, {
  success: function(result) {
    console.log('Success:', result);
  },
  error: function(result) {
    console.error('Error:', result.error_message);
  }
});
```

#### Common Patterns

**Get contact by ID:**
```javascript
cj().crmAPI('Contact', 'get', {
  id: contactId,
  sequential: 1
}, {
  success: function(result) {
    if (result.count > 0) {
      var contact = result.values[0];
      console.log('Contact name:', contact.display_name);
    }
  }
});
```

**Create contribution:**
```javascript
cj().crmAPI('Contribution', 'create', {
  contact_id: contactId,
  financial_type_id: 1,
  total_amount: 100,
  contribution_status_id: 1
}, {
  success: function(result) {
    cj('#msgbox').html('Contribution created: ' + result.id);
  },
  error: function(result) {
    alert('Error: ' + result.error_message);
  }
});
```

**Custom message handling:**
```javascript
cj().crmAPI('Entity', 'action', params, {
  msgbox: '#custom-msgbox',  // Custom message container
  successtxt: 'Operation completed successfully!',
  closetxt: '<span class="zmdi zmdi-close"></span>',
  callBack: function(result, settings) {
    // Custom callback logic
    if (result.is_error) {
      return settings.error.call(this, result, settings);
    }
    // Custom success handling
    console.log('Custom callback:', result);
    return settings.success.call(this, result, settings);
  }
});
```

#### Default Options

```javascript
{
  ajaxURL: '/civicrm/ajax/rest',
  msgbox: '#restmsg',
  closetxt: '<span class="zmdi zmdi-close" title="Close"></span>',
  successtxt: 'Saved',
  success: function(result, settings) { /* ... */ },
  error: function(result, settings) { /* ... */ },
  callBack: function(result, settings) { /* ... */ }
}
```

## Event Handling

### Event Delegation

Always use event delegation for dynamically added elements:

```javascript
// ❌ DON'T - Won't work for dynamic elements
cj('.dynamic-button').click(function() {
  console.log('Clicked');
});

// ✅ DO - Works for current and future elements
cj(document).on('click', '.dynamic-button', function() {
  console.log('Clicked');
});
```

### Common Event Patterns

**Form submission:**
```javascript
cj(document).on('submit', '#my-form', function(e) {
  e.preventDefault();

  var formData = cj(this).serialize();

  // Process form data
  cj.ajax({
    url: '/path/to/handler',
    type: 'POST',
    data: formData,
    success: function(response) {
      console.log('Form submitted');
    }
  });

  return false; // Prevent default submission
});
```

**Input change with debounce:**
```javascript
var searchTimeout;
cj(document).on('input', '#search-field', function() {
  var searchTerm = cj(this).val();

  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(function() {
    // Perform search after 300ms of no typing
    performSearch(searchTerm);
  }, 300);
});
```

**Select change:**
```javascript
cj(document).on('change', '#country-select', function() {
  var countryId = cj(this).val();

  // Load states for selected country
  loadStates(countryId);
});
```

### Preventing Multiple Submissions

```javascript
cj(document).on('submit', 'form.crm-form', function() {
  var $form = cj(this);
  var $submit = $form.find('[type="submit"]');

  // Disable submit button
  $submit.prop('disabled', true).val('Processing...');

  // Re-enable after 3 seconds (in case of no redirect)
  setTimeout(function() {
    $submit.prop('disabled', false).val('Submit');
  }, 3000);
});
```

## Plugin Development

### jQuery Plugin Pattern

```javascript
(function($) {
  'use strict';

  $.fn.myPlugin = function(options) {
    // Default settings
    var settings = $.extend({
      color: 'blue',
      fontSize: '14px'
    }, options);

    return this.each(function() {
      var $element = $(this);

      // Plugin logic
      $element.css({
        color: settings.color,
        fontSize: settings.fontSize
      });

      // Add events
      $element.on('click', function() {
        console.log('Plugin element clicked');
      });
    });
  };

})(cj);

// Usage
cj('.my-elements').myPlugin({
  color: 'red',
  fontSize: '16px'
});
```

### Existing CiviCRM Plugins

Check for these custom jQuery plugins in the codebase:

- `.crmAPI()` - API calls
- `.crmAccordion()` - Accordion UI
- `.crmTooltip()` - Tooltips
- `.crmAsmSelect()` - Advanced multi-select
- `.disableSubmit()` - Prevent double submission

## Common Utilities

### AJAX Patterns

```javascript
// Simple AJAX call
cj.ajax({
  url: '/civicrm/ajax/endpoint',
  type: 'POST',
  data: {
    key: 'value'
  },
  dataType: 'json',
  success: function(response) {
    if (response.success) {
      console.log('Success:', response.data);
    }
  },
  error: function(xhr, status, error) {
    console.error('Error:', error);
  }
});

// Get JSON
cj.getJSON('/civicrm/ajax/data', function(data) {
  console.log('Data:', data);
});
```

### DOM Manipulation

```javascript
// Find elements
var $element = cj('#my-id');
var $elements = cj('.my-class');
var $parent = $element.closest('.parent-class');

// Modify content
$element.html('<strong>New content</strong>');
$element.text('Plain text');
$element.val('Input value');

// Add/remove classes
$element.addClass('active');
$element.removeClass('inactive');
$element.toggleClass('expanded');

// Show/hide
$element.show();
$element.hide();
$element.fadeIn();
$element.fadeOut();
$element.slideToggle();

// Append/prepend
$element.append('<div>Append</div>');
$element.prepend('<div>Prepend</div>');
$element.after('<div>After</div>');
$element.before('<div>Before</div>');
```

### Data Attributes

```javascript
// Set data
cj('#element').data('contact-id', 123);

// Get data
var contactId = cj('#element').data('contact-id');

// From HTML
<div id="element" data-contact-id="123"></div>
```

### Iterating Collections

```javascript
// Each method
cj('.items').each(function(index, element) {
  var $item = cj(element);
  console.log('Item ' + index + ':', $item.text());
});

// Map method
var ids = cj('.items').map(function() {
  return cj(this).data('id');
}).get();
```

## Code Style

### General Conventions

- **Indentation**: 2 spaces (never tabs)
- **Quotes**: Single quotes for strings (`'text'`)
- **Semicolons**: Always required
- **Strict mode**: Use `'use strict';` in closures
- **Variable naming**: camelCase (`myVariable`)
- **Comparisons**: Use strict equality (`===` and `!==`)

### Function Declarations

```javascript
// Function declaration
function myFunction(param1, param2) {
  return param1 + param2;
}

// Function expression
var myFunction = function(param1, param2) {
  return param1 + param2;
};

// Arrow function (ES6+, check browser support)
var myFunction = (param1, param2) => param1 + param2;
```

### Variable Declarations

```javascript
// Declare at top of scope
var contactId = 123;
var contactName = 'John Doe';
var isActive = true;

// Multiple declarations
var contactId = 123,
    contactName = 'John Doe',
    isActive = true;
```

### Comments

```javascript
// Single-line comment for brief explanation

/*
 * Multi-line comment
 * for longer explanations
 */

/**
 * Function documentation
 * @param {number} contactId - The contact ID
 * @param {object} options - Configuration options
 * @return {boolean} Success status
 */
function updateContact(contactId, options) {
  // Implementation
}
```

## Anti-Patterns to Avoid

### ❌ Using `$` Directly

```javascript
// DON'T
$(document).ready(function() {
  $('#element').click(function() { });
});

// DO
cj(document).ready(function($) {
  $('#element').click(function() { });
});
```

### ❌ Not Handling API Errors

```javascript
// DON'T
cj().crmAPI('Contact', 'get', { id: 123 });

// DO
cj().crmAPI('Contact', 'get', { id: 123 }, {
  success: function(result) {
    console.log('Success:', result);
  },
  error: function(result) {
    console.error('Error:', result.error_message);
    alert('Failed to load contact');
  }
});
```

### ❌ Global Variables Pollution

```javascript
// DON'T - Pollutes global scope
var myData = [];
function processData() { }

// DO - Use closure
(function($) {
  'use strict';

  var myData = [];

  function processData() {
    // Private function
  }

  // Expose only what's needed
  window.MyNamespace = {
    publicMethod: function() {
      processData();
    }
  };

})(cj);
```

### ❌ Inefficient Selectors

```javascript
// DON'T - Searches entire document repeatedly
cj('.my-class').each(function() {
  cj('.my-class').doSomething();
});

// DO - Cache selectors
var $elements = cj('.my-class');
$elements.each(function() {
  $elements.doSomething();
});
```

### ❌ Not Preventing Default

```javascript
// DON'T - Form submits anyway
cj('#my-form').submit(function(e) {
  processForm();
});

// DO - Prevent default submission
cj('#my-form').submit(function(e) {
  e.preventDefault();
  processForm();
  return false;
});
```

### ❌ Mixing jQuery and Vanilla JS

```javascript
// DON'T - Inconsistent approach
var element = document.getElementById('my-id');
cj(element).addClass('active');
element.innerHTML = 'New content';

// DO - Choose one approach
var $element = cj('#my-id');
$element.addClass('active');
$element.html('New content');
```

## Performance Best Practices

1. **Cache jQuery objects**: Don't re-select repeatedly
2. **Use event delegation**: Especially for dynamic content
3. **Minimize DOM manipulations**: Batch changes when possible
4. **Avoid excessive animations**: Can impact performance
5. **Debounce rapid events**: Like scroll, resize, input
6. **Use `data-` attributes**: Instead of custom attributes

## Browser Compatibility

CiviCRM supports modern browsers. For older browser support:

- Avoid ES6+ features without transpilation
- Test arrow functions, const/let, template literals
- Use jQuery methods for cross-browser compatibility
- Check for console.log availability (IE issues)
