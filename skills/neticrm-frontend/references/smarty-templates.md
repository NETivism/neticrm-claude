# Smarty Templates Guide

## Table of Contents
1. [Smarty Version](#smarty-version)
2. [Basic Syntax](#basic-syntax)
3. [Translation System](#translation-system)
4. [Custom Plugins](#custom-plugins)
5. [Form Elements](#form-elements)
6. [Asset Loading](#asset-loading)
7. [Control Structures](#control-structures)
8. [Security and Escaping](#security-and-escaping)
9. [Common Patterns](#common-patterns)
10. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

## Smarty Version

CiviCRM uses **Smarty 2**. Some Smarty 3 features are not available.

## Basic Syntax

### Variable Output

```smarty
{* Basic variable *}
{$variableName}

{* Array access *}
{$contact.first_name}
{$contact['email']}

{* Object property *}
{$form->_values.id}

{* With modifiers *}
{$description|truncate:50}
{$email|escape}
{$date|date_format:"%Y-%m-%d"}
```

### Comments

```smarty
{* Single-line comment *}

{*
  Multi-line
  comment
*}
```

### Variable Assignment

```smarty
{assign var="pageTitle" value="Contact Details"}
{assign var="count" value=5}
{assign var="isAdmin" value=true}

{* Use assigned variable *}
<h1>{$pageTitle}</h1>
```

### Including Templates

```smarty
{* Include another template *}
{include file="CRM/common/header.tpl"}

{* Include with parameters *}
{include file="CRM/common/formButtons.tpl" location="top"}
```

## Translation System

### Basic Translation

```smarty
{* Simple text *}
{ts}Hello World{/ts}

{* Result: Translated version of "Hello World" *}
```

### Translation with Parameters

```smarty
{* Numbered parameters (recommended) *}
{ts 1=$contactName}Hello %1{/ts}
{ts 1=$firstName 2=$lastName}Welcome %1 %2{/ts}

{* Multiple parameters *}
{ts 1=$count 2=$total}Showing %1 of %2 results{/ts}
```

### Translation Context

```smarty
{* JavaScript context (CRITICAL) *}
<script>
{literal}
var message = '{/literal}{ts escape='js'}Are you sure?{/ts}{literal}';
{/literal}
</script>

{* Without escape='js', quotes in translation can break JavaScript *}
```

### Plural Forms

```smarty
{ts count=$n plural='%count items'}One item{/ts}

{* When count=1: "One item" *}
{* When count>1: "5 items" *}
```

### Translation Best Practices

1. **Always use `{ts}` for user-facing text**
   ```smarty
   {* ✅ DO *}
   <button>{ts}Save{/ts}</button>

   {* ❌ DON'T *}
   <button>Save</button>
   ```

2. **Use numbered parameters, not variable interpolation**
   ```smarty
   {* ✅ DO *}
   {ts 1=$name}Hello %1{/ts}

   {* ❌ DON'T *}
   {ts}Hello {$name}{/ts}
   ```

3. **Don't break sentences across multiple `{ts}` blocks**
   ```smarty
   {* ✅ DO *}
   {ts 1=$count}You have %1 new messages{/ts}

   {* ❌ DON'T *}
   {ts}You have{/ts} {$count} {ts}new messages{/ts}
   ```

4. **Always use `escape='js'` in JavaScript context**
   ```smarty
   {* ✅ DO *}
   alert('{ts escape='js'}Confirm action{/ts}');

   {* ❌ DON'T *}
   alert('{ts}Confirm action{/ts}');
   ```

## Custom Plugins

CiviCRM provides custom Smarty plugins for common tasks.

### `{crmURL}` - Generate URLs

```smarty
{* Basic URL *}
<a href="{crmURL p='civicrm/contact/view' q='reset=1&cid=123'}">
  View Contact
</a>

{* With parameters *}
{crmURL p='civicrm/contribute/transact' q="reset=1&id=`$contributionPageId`"}

{* Absolute URL *}
{crmURL p='civicrm/event/register' q='reset=1' a=1}

{* Frontend URL (non-admin) *}
{crmURL p='civicrm/profile/create' q='reset=1' fe=1}
```

**Parameters:**
- `p` - Path (required)
- `q` - Query string
- `a` - Absolute URL (1 or 0)
- `fe` - Frontend URL (1 or 0)

### `{crmMoney}` - Format Currency

```smarty
{* Format amount *}
{$amount|crmMoney}
{* Output: $1,234.56 (based on site currency settings) *}

{* With specific currency *}
{$amount|crmMoney:'USD'}
```

### `{crmDate}` - Format Date

```smarty
{* Format date *}
{$dateValue|crmDate}

{* Custom format *}
{$dateValue|crmDate:"%B %d, %Y"}
{* Output: January 15, 2024 *}
```

### `{crmAPI}` - Call API from Template

```smarty
{* Get contact data *}
{crmAPI var='contactResult' entity='Contact' action='get' id=$contactId sequential=1}

{* Use result *}
{if $contactResult.is_error}
  <p class="error">{$contactResult.error_message}</p>
{else}
  {assign var="contact" value=$contactResult.values.0}
  <p>Contact: {$contact.display_name}</p>
{/if}
```

**Warning**: API calls in templates can impact performance. Use sparingly and cache results when possible.

## Form Elements

### Rendering Form Fields

```smarty
{* Field label *}
{$form.fieldName.label}

{* Field input *}
{$form.fieldName.html}

{* Complete field (label + input) *}
<tr>
  <td class="label">{$form.email.label}</td>
  <td>{$form.email.html}</td>
</tr>
```

### Form Buttons

```smarty
{* Standard form buttons *}
{include file="CRM/common/formButtons.tpl" location="bottom"}

{* Custom location *}
{include file="CRM/common/formButtons.tpl" location="top"}
```

### Checkbox and Radio

```smarty
{* Checkbox *}
{$form.is_active.html} {$form.is_active.label}

{* Radio group *}
{foreach from=$form.gender item=option}
  {$option.html} {$option.label}<br>
{/foreach}
```

### Select Elements

```smarty
{* Basic select *}
{$form.country_id.html}

{* With description *}
{$form.payment_processor.html}
<div class="description">{ts}Select payment processor{/ts}</div>
```

## Asset Loading

### Loading JavaScript

```smarty
{* Basic JS load *}
{js src=packages/myScript.js}{/js}

{* With group and weight (Drupal 7) *}
{js src=packages/myScript.js group=999 weight=997}{/js}

{* With library (Drupal 10 required) *}
{js src=packages/mailingEditor/mailingEditor.js group=999 weight=997 library=civicrm/civicrm-js-mailingeditor}{/js}
```

**Parameters:**
- `src` - Path relative to CiviCRM root
- `group` - Loading group (higher = later)
- `weight` - Order within group (higher = later)
- `library` - Drupal 10 library name (required for D10)

### Loading CSS

```smarty
{* Link tag method *}
<link rel="stylesheet" href="{$config->resourceBase}packages/myStyle.css?v{$config->ver}">

{* With cache busting *}
<link rel="stylesheet" href="{$config->resourceBase}css/civicrm.css?v{$config->ver}">
```

### Inline JavaScript

```smarty
<script type="text/javascript">
{literal}
cj(document).ready(function($) {
  // Use $ inside this closure
  $('#my-element').click(function() {
    alert('{/literal}{ts escape='js'}Button clicked{/ts}{literal}');
  });
});
{/literal}
</script>
```

**Important**:
- Use `{literal}...{/literal}` to prevent Smarty from parsing JavaScript
- Use `{ts escape='js'}` for translated strings in JavaScript
- Break out of `{literal}` blocks to output Smarty variables

## Control Structures

### If/Else

```smarty
{if $condition}
  Content when true
{elseif $otherCondition}
  Content when other is true
{else}
  Default content
{/if}

{* Comparison operators *}
{if $count > 0}
{if $status == 'active'}
{if $isAdmin}
```

### Foreach Loop

```smarty
{* Basic loop *}
{foreach from=$contacts item=contact}
  <p>{$contact.display_name}</p>
{/foreach}

{* With key *}
{foreach from=$options key=id item=label}
  <option value="{$id}">{$label}</option>
{/foreach}

{* With counter *}
{foreach from=$items item=item name=itemLoop}
  <div class="item-{$smarty.foreach.itemLoop.iteration}">
    {$item.name}
  </div>
{/foreach}

{* Check if empty *}
{foreach from=$contacts item=contact}
  <p>{$contact.display_name}</p>
{foreachelse}
  <p>{ts}No contacts found{/ts}</p>
{/foreach}
```

### Section Loop

```smarty
{section name=row loop=$rows}
  <tr>
    <td>{$rows[row].name}</td>
    <td>{$rows[row].email}</td>
  </tr>
{/section}
```

## Security and Escaping

### Escaping Output

```smarty
{* HTML escape (default when using {$var}) *}
{$userInput|escape}

{* JavaScript context *}
{$var|escape:'javascript'}
<script>var data = '{$data|escape:'javascript'}';</script>

{* URL context *}
<a href="?name={$name|escape:'url'}">Link</a>

{* HTML entities *}
{$html|escape:'htmlall'}
```

### When to Escape

1. **User input**: Always escape user-provided data
2. **Database values**: Escape when displaying in HTML
3. **JavaScript strings**: Use `|escape:'javascript'` or `{ts escape='js'}`
4. **URLs**: Use `|escape:'url'` for query parameters

### Trusted Content

```smarty
{* When content is already HTML and trusted *}
{$richTextContent}

{* Explicit no-escape *}
{$trustedHtml nofilter}
```

**Warning**: Only use unescaped output for trusted, sanitized content.

## Common Patterns

### Accordion/Collapsible Section

```smarty
<div class="crm-accordion-wrapper crm-accordion_title-accordion crm-accordion-open">
  <div class="crm-accordion-header">
    <div class="zmdi crm-accordion-pointer"></div>
    {ts}Section Title{/ts}
  </div>
  <div class="crm-accordion-body">
    {* Section content *}
    <p>{ts}Content here{/ts}</p>
  </div>
</div>
```

### Data Table

```smarty
<table class="selector row-highlight">
  <thead>
    <tr>
      <th>{ts}Name{/ts}</th>
      <th>{ts}Email{/ts}</th>
      <th>{ts}Actions{/ts}</th>
    </tr>
  </thead>
  <tbody>
    {foreach from=$contacts item=contact}
      <tr class="{cycle values="odd-row,even-row"}">
        <td>{$contact.display_name}</td>
        <td>{$contact.email}</td>
        <td>
          <a href="{crmURL p='civicrm/contact/view' q="reset=1&cid=`$contact.id`"}">
            {ts}View{/ts}
          </a>
        </td>
      </tr>
    {foreachelse}
      <tr>
        <td colspan="3">{ts}No records found{/ts}</td>
      </tr>
    {/foreach}
  </tbody>
</table>
```

### Form Layout

```smarty
<div class="crm-block crm-form-block crm-myform-block">
  <div class="crm-submit-buttons">
    {include file="CRM/common/formButtons.tpl" location="top"}
  </div>

  <table class="form-layout">
    <tr class="crm-myform-form-block-field_name">
      <td class="label">{$form.field_name.label}</td>
      <td class="html-adjust">
        {$form.field_name.html}
        <div class="description">{ts}Help text here{/ts}</div>
      </td>
    </tr>
  </table>

  <div class="crm-submit-buttons">
    {include file="CRM/common/formButtons.tpl" location="bottom"}
  </div>
</div>
```

### Icon with Text

```smarty
<i class="zmdi zmdi-check-circle"></i> {ts}Success{/ts}
<i class="zmdi zmdi-alert-triangle"></i> {ts}Warning{/ts}
<i class="zmdi zmdi-info"></i> {ts}Information{/ts}
```

### Help Link

```smarty
{help id='id-field-name' file="CRM/MyModule/Form/MyForm.hlp"}
```

## Anti-Patterns to Avoid

### ❌ Breaking Sentences in Translation

```smarty
{* DON'T *}
<p>{ts}You have{/ts} {$count} {ts}new messages{/ts}</p>

{* DO *}
<p>{ts 1=$count}You have %1 new messages{/ts}</p>
```

### ❌ Missing `escape='js'` in JavaScript

```smarty
{* DON'T *}
<script>
var message = '{ts}Confirm delete?{/ts}';
</script>

{* DO *}
<script>
var message = '{ts escape='js'}Confirm delete?{/ts}';
</script>
```

### ❌ Forgetting `{literal}` for JavaScript

```smarty
{* DON'T - Smarty will try to parse { } *}
<script>
if (x > 0) { doSomething(); }
</script>

{* DO *}
<script>
{literal}
if (x > 0) { doSomething(); }
{/literal}
</script>
```

### ❌ Direct Variable in Translation

```smarty
{* DON'T *}
{ts}Hello {$name}{/ts}

{* DO *}
{ts 1=$name}Hello %1{/ts}
```

### ❌ Unescaped User Input

```smarty
{* DON'T *}
<div>{$userComment}</div>

{* DO *}
<div>{$userComment|escape}</div>
```

### ❌ Hardcoded URLs

```smarty
{* DON'T *}
<a href="/civicrm/contact/view?cid=123">View</a>

{* DO *}
<a href="{crmURL p='civicrm/contact/view' q='cid=123'}">View</a>
```

## Template File Naming

Templates follow the PHP class structure:

```
PHP Class: CRM_Contribute_Form_Contribution
Template:  templates/CRM/Contribute/Form/Contribution.tpl

PHP Class: CRM_Contact_Page_View_Summary
Template:  templates/CRM/Contact/Page/View/Summary.tpl
```

## Debugging

```smarty
{* Debug variable *}
{debug}

{* Output variable structure *}
{$variable|@debug_print_var}

{* Check if variable is set *}
{if isset($variable)}
  Variable exists
{/if}
```

## Performance Tips

1. **Avoid API calls in templates**: Pre-fetch data in PHP controller
2. **Cache repeated calculations**: Use `{assign}` for reused values
3. **Minimize includes**: Each include has overhead
4. **Use `{strip}` for output compression**: Removes extra whitespace
   ```smarty
   {strip}
     <div>
       Content
     </div>
   {/strip}
   ```
