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

Benchmarked against the most popular Python i18n libraries (10,000 iterations, Python 3.12.8):

| Operation | i18n_modern | python-i18n | pyi18n-v2 | i18nice |
| ----------- | :-----------: | :-----------: | :---------: | :-------: |
| Simple key access | **0.23µs** | 0.79µs | 0.40µs | 1.51µs |
| Nested key access | **0.17µs** | 66.90µs | 0.64µs | 1.55µs |
| Parameter substitution | **0.43µs** | 0.99µs | 0.83µs | 1.91µs |
| Conditional logic | **0.75µs** | ✗ | ✗ | ✗ |

> **384x faster** than python-i18n for nested key access. See [BENCHMARK_REPORT.md](BENCHMARK_REPORT.md) for the full analysis.

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

# Now you can access all translations
print(i18n.get("auth.login"))      # From auth.yml
print(i18n.get("common.welcome"))  # From common.yml
print(i18n.get("document.create")) # From document.yml
```

### Changing Default Locale

```python
i18n.default_locale = "es"
translation = i18n.get("welcome")  # Now uses Spanish
```

## API Reference

### `I18nModern(default_locale, locales=None)`

Constructor for the i18n instance.

- `default_locale` (str): The default locale identifier
- `locales` (dict or str, optional): Initial locales dictionary or path to locale file

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

### `load_from_directory(directory_path, locale_identify=None)`

Load all translation files from a directory concurrently.

- `directory_path` (str): Path to directory containing locale files (JSON, YAML, TOML)
- `locale_identify` (str, optional): Locale identifier. If None, uses the directory name
- All files in the directory are merged together into a single locale entry

**Supported file formats in directory:** `.json`, `.yaml`, `.yml`, `.toml`

**Example:**

```python
i18n = I18nModern("es_MX")
# Loads all .json, .yaml, .yml, and .toml files from the directory
i18n.load_from_directory("locales/es_MX")

# With custom locale identifier
i18n.load_from_directory("locales/es_MX", locale_identify="spanish")
```

### `load_from_value(locales, locale_identify)`

Load translations from a dictionary.

- `locales` (dict): Translations dictionary
- `locale_identify` (str): Locale identifier

### Properties

- `default_locale`: Get or set the default locale

## License

MIT

## Credits

Inspired by [i18n_modern](https://github.com/UrielCuriel/i18n_modern) for JavaScript.
