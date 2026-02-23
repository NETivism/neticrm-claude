# JavaScript Patterns and Best Practices

## Table of Contents
1. [jQuery Usage](#jquery-usage)
2. [Native JS Usage](#native-js-usage)
3. [CiviCRM API Patterns](#civicrm-api-patterns)
4. [Event Handling](#event-handling)
5. [Plugin Development](#plugin-development)
6. [Common Utilities](#common-utilities)
7. [Code Style](#code-style)
8. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

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

## Native JS Usage

### When to Use Native JS vs jQuery

jQuery (`cj()`) is the primary tool for DOM work. Choose native JS when:

| Situation | Recommendation |
|-----------|----------------|
| DOM selection, manipulation, event binding | jQuery (`cj()`) |
| Modern browser APIs (fetch, MutationObserver) | Native JS |
| Utility functions that don't touch the DOM | Native JS |
| ES6+ syntax (const, arrow functions, etc.) | Use anywhere alongside jQuery |
| New standalone modules with no jQuery dependency | Native JS |

### ES6+ Syntax

ES6+ syntax can be used in any JS file alongside jQuery — these are syntax improvements, not a separate approach.

**`const` and `let` instead of `var`:**

```javascript
// const for values that won't be reassigned
const contactId = cj('#contact-id').val();

// let when reassignment is needed
let retryCount = 0;
```

**Arrow functions:**

```javascript
// Good for callbacks where 'this' context is irrelevant
cj('.items').each((index, element) => {
  cj(element).addClass('active');
});

// Use regular functions when 'this' refers to the DOM element
cj('.items').each(function() {
  cj(this).addClass('active'); // 'this' is the element
});
```

**Template literals:**

```javascript
const name = 'John';
const message = `Hello ${name}, you have ${count} messages.`;
cj('#notice').text(message);
```

**Destructuring:**

```javascript
// Object destructuring
const { display_name, email } = contact;

// Array destructuring
const [first, ...rest] = items;
```

**Promise / async-await:**

```javascript
async function loadContact(id) {
  try {
    const data = await fetchContact(id);
    cj('#contact-name').text(data.display_name);
  } catch (error) {
    console.error('Load failed:', error);
  }
}
```

### Modern DOM API

Use native DOM API for standalone utilities or when operating outside jQuery context:

```javascript
// querySelector - equivalent to cj('selector')[0]
const element = document.querySelector('#my-id');
const elements = document.querySelectorAll('.my-class');

// classList - equivalent to jQuery addClass/removeClass
element.classList.add('active');
element.classList.remove('inactive');
element.classList.toggle('expanded');
element.classList.contains('active'); // returns boolean

// dataset - read data-* attributes
// <div data-contact-id="123">
const contactId = element.dataset.contactId; // '123'
```

### Fetch API

Use `fetch` for new standalone modules that don't rely on CiviCRM's `.crmAPI()`.
For CiviCRM API calls, always use `.crmAPI()` — not fetch.

```javascript
async function postData(url, params) {
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Fetch failed:', error);
  }
}
```

### MutationObserver

jQuery has no equivalent. Use `MutationObserver` to react to DOM changes added by other scripts:

```javascript
// Watch for dynamically added elements
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    mutation.addedNodes.forEach((node) => {
      if (node.nodeType === 1 && node.matches('.crm-container')) {
        // Safely hand off newly added elements back to jQuery
        cj(node).find('.my-class').doSomething();
      }
    });
  });
});

observer.observe(document.body, { childList: true, subtree: true });

// Stop observing when done
observer.disconnect();
```

### Coexisting with jQuery

When a file uses both jQuery and native JS, keep each tool in a clearly purposeful role:

```javascript
(function($) {
  'use strict';

  // jQuery for DOM interaction (its strength)
  $(document).on('click', '.crm-button', function() {
    const contactId = $(this).data('contact-id');
    loadContact(contactId);
  });

  // Native JS async function — not a jQuery concern
  async function loadContact(id) {
    const data = await fetch(`/civicrm/ajax/contact?id=${id}`)
      .then(r => r.json());
    $('#contact-name').text(data.display_name);
  }

})(cj);
```

Each tool handles what it does best, within clearly separated logical units.

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

### ❌ Mixing jQuery and Vanilla JS in the Same Operation

The anti-pattern is mixing both approaches **within a single operation**: selecting with native JS then passing to `cj()`, or vice versa. This creates inconsistency and confusion.

```javascript
// DON'T - Select with native JS, then hand off to jQuery
var element = document.getElementById('my-id');
cj(element).addClass('active');  // Why wrap it now?
element.innerHTML = 'New content'; // Switching back to native

// DO - Pick one approach and stay consistent for that operation
var $element = cj('#my-id');
$element.addClass('active');
$element.html('New content');
```

**However**, using native JS for a different purpose in the same file is fine. The rule is about **consistency within a logical unit**, not about banning native JS from jQuery files entirely. See [Native JS Usage](#native-js-usage) for when to choose each approach.

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
