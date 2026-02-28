# PHP Coding Style — netiCRM/CiviCRM

Rules: PSR1 + PSR2 + PSR12 subset via `.php-cs-fixer.php`. 2-space indentation throughout.

---

## Annotated Example

Read the inline comments — each one labels the rule being demonstrated.

```php
<?php

class CRM_Example_BAO_Record extends CRM_Example_DAO_Record {  // PascalCase; { same line

  const STATUS_ACTIVE = 'active';                    // class constant: UPPER_CASE

  private static $_singleton = NULL;                 // NULL uppercase; _camelCase; explicit visibility
  private static $_cache = [];                       // [] short array, never array()

  protected $_contactId;
  protected $_formValues = [];

  // Return type: no space before colon  (`: self`)
  // FALSE uppercase
  public static function &singleton($reset = FALSE): self {
    if ($reset || self::$_singleton === NULL) {       // self lowercase; === strict equality
      self::$_singleton = new CRM_Example_BAO_Record();  // new always with parentheses
    }
    return self::$_singleton;
  }

  // ?self  — nullable return: ? prefix, no space between ? and type
  public static function create(array $params): ?self {
    $record = new CRM_Example_BAO_Record();
    $record->copyValues($params);

    $transaction = new CRM_Core_Transaction();
    try {
      $record->save();
      $transaction->commit();
      return $record;
    }
    catch (Exception $e) {                           // catch: next line after }, never on same line
      $transaction->rollback();
      throw $e;
    }
  }

  // Multiline args: every arg on its own line when spanning multiple lines
  // ?string: nullable param with null default
  // FALSE/NULL uppercase; return type array
  public function process(
    int $contactId,
    ?string $note = NULL,
    bool $sendEmail = FALSE
  ): array {
    $results = [];
    $contactId = (int) $contactId;                   // type cast: lowercase short form

    if ($contactId <= 0) {
      return $results;
    }
    elseif (!$this->_isAllowed($contactId)) {        // elseif: next line after }; ! unary no space
      CRM_Core_Session::setStatus(
        ts('Not allowed'),
        ts('Error'),
        'error'
      );
      return $results;
    }
    else {                                           // else: next line after }
      $label = $note ?? ts('Default');
      $count = count($results);                      // count() not sizeof()
      $status = $count > 0 ? self::STATUS_ACTIVE : 'inactive';  // ternary: spaced
      $path = rtrim($label, '/') . '/' . (string) $contactId;   // binary .: spaced; (string) cast
      $results[] = [
        'id'     => $contactId,
        'status' => $status,
        'path'   => $path,
      ];
    }

    return $results;
  }

  // Private method: _ prefix convention
  private function _isAllowed(int $contactId): bool {
    return CRM_Core_Permission::check('access CiviCRM') && $contactId > 0;
  }

  // static lowercase; anonymous function: space after `function`
  public static function buildOptions(?string $type = NULL): array {
    $scale = 2 ** 4;                                 // ** instead of pow(); PHP 5.6+
    $fn = function ($item) use ($scale) {            // `function` keyword: one space after; closure use
      return (int) $item['value'] * $scale;
    };
    return array_map($fn, static::getDefaults());    // static lowercase
  }

  protected static function getDefaults(): array {
    return [];
  }
}
```

---

## Rules Quick Reference

| Rule | Correct | Wrong |
|------|---------|-------|
| Indentation | 2 spaces | tabs / 4 spaces |
| Boolean/null constants | `TRUE` `FALSE` `NULL` | `true` `false` `null` |
| Array literal | `[]` | `array()` |
| Brace — opening | same line as keyword | next line |
| Brace — `else`/`elseif`/`catch` | next line after `}` | `} else {` same line |
| Static refs | `self::` `static::` `parent::` | `Self::` `SELF::` |
| `new` | `new Foo()` | `new Foo` |
| Nullable type | `?string` | `? string` |
| Return type colon | `): array` | `) : array` |
| Type cast | `(int)` `(bool)` `(string)` | `(integer)` `(boolean)` |
| Binary operators | spaced: `$a . $b` | `$a.$b` |
| Unary operators | no space: `!$x` `$x++` | `! $x` |
| `pow()` | `2 ** 3` | `pow(2, 3)` |
| `sizeof()` | `count($arr)` | `sizeof($arr)` |
| Naming — class | `CRM_Core_ClassLoader` | `CrmCoreClassLoader` |
| Naming — method | `loadClass()` | `load_class()` |
| Naming — property | `$_contactId` | `$contactId` |
| Visibility | always explicit | omitted |
| Multiline args | every arg own line | mixed |

---

## php-cs-fixer CLI

Run from the CiviCRM root (where `.php-cs-fixer.php` lives):

```bash
# Check without modifying
php-cs-fixer fix --dry-run --diff

# Fix a single file
php-cs-fixer fix CRM/Core/Config.php

# Fix all (uses finder config in .php-cs-fixer.php)
php-cs-fixer fix

# Show which rules triggered
php-cs-fixer fix --dry-run --diff --verbose CRM/Core/Config.php
```
