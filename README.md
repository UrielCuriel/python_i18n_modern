# Python i18n Modern

A modern internationalization (i18n) library for Python, inspired by [i18n_modern](https://github.com/UrielCuriel/i18n_modern) for JavaScript.

## Features

- 🌍 Simple and intuitive API for translations
- 📁 Support for multiple file formats: JSON, YAML, and TOML
- 🔄 Nested translation keys with dot notation
- 🎯 Conditional translations based on values
- 📝 Template string interpolation with `[placeholder]` syntax
- 💾 Built-in memoization for better performance
- 🔗 Deep object merging for locale inheritance
- ⚡ Flat locale structure for O(1) key lookups at runtime

## Performance

Benchmarked against popular Python i18n libraries using `pytest-benchmark` on Linux and Windows (latest baseline: `v0.2.3`).

| Operation | Resultado consistente |
| ----------- | ----------- |
| Simple key access | **i18n_modern** is fastest in both Linux and Windows |
| Nested key access | **i18n_modern** is fastest in both Linux and Windows |
| Parameter substitution | **i18n_modern** is fastest in both Linux and Windows |
| Conditional logic | Available in **i18n_modern** benchmark suite |

> Up to **580x faster** than python-i18n on nested key access (Windows benchmark run).

For complete numbers, environment details, and per-library ranking, see [BENCHMARK_REPORT.md](BENCHMARK_REPORT.md).

## Installation

```bash
# Basic installation (JSON support only)
pip install i18n_modern

# With YAML support
pip install i18n_modern[yaml]

# With TOML support (Python < 3.11)
pip install i18n_modern[toml]

# With all formats
pip install i18n_modern[all]
```

## Quick Start

### Loading from Dictionary

```python
from i18n_modern import I18nModern

locales = {
    "greeting": "Hello, [name]!",
    "items": {
        "0": "No items",
        "1": "One item",
        "default": "[count] items"
    }
}

i18n = I18nModern("en", locales)
print(i18n.get("greeting", values={"name": "World"}))  # Hello, World!
```

### Loading from Files

```python
from i18n_modern import I18nModern

# Load from JSON
i18n = I18nModern("en", "locales/en.json")

# Load from YAML
i18n = I18nModern("es", "locales/es.yaml")

# Load from TOML
i18n = I18nModern("fr", "locales/fr.toml")
```

### Example Files

### locales/en.json

```json
{
    "welcome": "Welcome to our app!",
    "greeting": "Hello, [name]!",
    "messages": {
        "success": "Operation successful",
        "error": "An error occurred"
    },
    "items": {
        "0": "No items",
        "1": "One item",
        "default": "[count] items"
    }
}
```

### locales/es.yaml

```yaml
welcome: "¡Bienvenido a nuestra aplicación!"
greeting: "¡Hola, [name]!"
messages:
  success: "Operación exitosa"
  error: "Ocurrió un error"
items:
  "0": "Sin elementos"
  "1": "Un elemento"
  default: "[count] elementos"
```

### locales/fr.toml

```toml
welcome = "Bienvenue dans notre application!"
greeting = "Bonjour, [name]!"

[messages]
success = "Opération réussie"
error = "Une erreur s'est produite"

[items]
"0" = "Aucun élément"
"1" = "Un élément"
default = "[count] éléments"
```

## Usage

### Basic Translation

```python
i18n = I18nModern("en", locales)
translation = i18n.get("welcome")
```

### Nested Keys

```python
translation = i18n.get("messages.success")
```

### Template Interpolation

```python
translation = i18n.get("greeting", values={"name": "Alice"})
# Output: Hello, Alice!
```

### Conditional Translations

```python
# Using exact matches
print(i18n.get("items", values={"count": 0}))  # No items
print(i18n.get("items", values={"count": 1}))  # One item
print(i18n.get("items", values={"count": 5}))  # 5 items

# Using comparisons
locales = {
    "age_group": {
        "[age] < 18": "Minor",
        "[age] >= 18": "Adult",
        "default": "Unknown"
    }
}

i18n = I18nModern("en", locales)
print(i18n.get("age_group", values={"age": 15}))  # Minor
print(i18n.get("age_group", values={"age": 25}))  # Adult
```

### Multiple Locales

```python
i18n = I18nModern("en")
i18n.load_from_file("locales/en.json", "en")
i18n.load_from_file("locales/es.json", "es")

# Use default locale (en)
print(i18n.get("greeting", values={"name": "World"}))

# Use specific locale
print(i18n.get("greeting", locale="es", values={"name": "Mundo"}))
```

### Loading from Directory

You can load all translation files from a directory at once. This is useful when you have multiple files for a single locale.

```python
# Structure:
# locales/
# ├── es_MX/
# │   ├── auth.yml
# │   ├── common.yml
# │   ├── document.yml
# │   └── roles.yml

i18n = I18nModern("es_MX")

# Load all files from directory - they will be merged together
# The directory name (es_MX) is used as the locale identifier
i18n.load_from_directory("locales/es_MX")

# Or specify a custom locale identifier
i18n.load_from_directory("locales/es_MX", locale_identify="spanish_mexico")

# Use filename as namespace for this specific call
i18n.load_from_directory("locales/es_MX", use_filename_as_namespace=True)

# Now you can access all translations
print(i18n.get("auth.login"))      # From auth.yml
print(i18n.get("common.welcome"))  # From common.yml
print(i18n.get("document.create")) # From document.yml
```

You can also enable this behavior at instance level:

```python
i18n = I18nModern("es_MX", use_filename_as_namespace=True)
i18n.load_from_directory("locales/es_MX")

# Or toggle it later
i18n.use_filename_as_namespace = True
```

### Changing Default Locale

```python
i18n.default_locale = "es"
translation = i18n.get("welcome")  # Now uses Spanish
```

## API Reference

### `I18nModern(default_locale, locales=None, use_filename_as_namespace=False)`

Constructor for the i18n instance.

- `default_locale` (str): The default locale identifier
- `locales` (dict or str, optional): Initial locales dictionary or path to locale file
- `use_filename_as_namespace` (bool, optional): Default behavior for directory
    imports. When `True`, each file is namespaced by filename stem (for example,
    `common.yml` -> `common.*`)

### `get(key, locale=None, values=None)`

Get a translation.

- `key` (str): Translation key (supports dot notation)
- `locale` (str, optional): Locale override
- `values` (dict, optional): Values for placeholder replacement
- Returns: Translated string

### `load_from_file(file_path, locale_identify)`

Load translations from a file.

- `file_path` (str): Path to JSON, YAML, or TOML file
- `locale_identify` (str): Locale identifier

### `load_from_directory(directory_path, locale_identify=None, use_filename_as_namespace=None)`

Load all translation files from a directory concurrently.

- `directory_path` (str): Path to directory containing locale files (JSON, YAML, TOML)
- `locale_identify` (str, optional): Locale identifier. If None, uses the directory name
- `use_filename_as_namespace` (bool, optional): Per-call override. If `True`, wraps
    every file under its filename stem; if `None`, uses the instance setting
- All files in the directory are merged together into a single locale entry

**Supported file formats in directory:** `.json`, `.yaml`, `.yml`, `.toml`

**Example:**

```python
i18n = I18nModern("es_MX")
# Loads all .json, .yaml, .yml, and .toml files from the directory
i18n.load_from_directory("locales/es_MX")

# With custom locale identifier
i18n.load_from_directory("locales/es_MX", locale_identify="spanish")

# With per-call namespace override
i18n.load_from_directory("locales/es_MX", use_filename_as_namespace=True)
```

### `load_from_value(locales, locale_identify)`

Load translations from a dictionary.

- `locales` (dict): Translations dictionary
- `locale_identify` (str): Locale identifier

### Properties

- `default_locale`: Get or set the default locale
- `use_filename_as_namespace`: Get or set filename namespacing behavior for
    directory imports

## License

MIT

## Credits

Inspired by [i18n_modern](https://github.com/UrielCuriel/i18n_modern) for JavaScript.
