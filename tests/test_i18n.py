"""Tests for i18n_modern library."""

import pytest

from i18n_modern import I18nModern
from i18n_modern.types import LocaleDict


@pytest.fixture
def basic_locales():
    """Basic locale data for testing."""
    return {"welcome": "Welcome!", "greeting": "Hello, [name]!"}


@pytest.fixture
def nested_locales():
    """Nested locale data for testing."""
    return {"messages": {"success": "Success!", "error": "Error!"}}


@pytest.fixture
def conditional_locales():
    """Conditional locale data for testing."""
    return {"items": {"0": "No items", "1": "One item", "default": "[count] items"}}


@pytest.fixture
def comparison_locales():
    """Comparison condition locale data for testing."""
    return {
        "age_group": {
            "[age] < 18": "Minor",
            "[age] >= 18": "Adult",
            "default": "Unknown",
        }
    }


@pytest.fixture
def memoization_locales():
    """Locale data for memoization testing."""
    return {"greeting": "Hello, [name]!"}


class TestI18nModern:
    """Test class for I18nModern functionality."""

    def test_basic_translation(self, basic_locales: LocaleDict) -> None:
        """Test basic translation."""
        i18n = I18nModern("en", basic_locales)
        assert i18n.get("welcome") == "Welcome!"
        assert i18n.get("greeting", values={"name": "World"}) == "Hello, World!"

    def test_nested_keys(self, nested_locales: LocaleDict) -> None:
        """Test nested translation keys."""
        i18n = I18nModern("en", nested_locales)
        assert i18n.get("messages.success") == "Success!"
        assert i18n.get("messages.error") == "Error!"

    def test_conditional_translations(self, conditional_locales: LocaleDict) -> None:
        """Test conditional translations."""
        i18n = I18nModern("en", conditional_locales)
        assert i18n.get("items", values={"count": 0}) == "No items"
        assert i18n.get("items", values={"count": 1}) == "One item"
        assert i18n.get("items", values={"count": 5}) == "5 items"

    def test_comparison_conditions(self, comparison_locales: LocaleDict) -> None:
        """Test comparison conditions."""
        i18n = I18nModern("en", comparison_locales)
        assert i18n.get("age_group", values={"age": 15}) == "Minor"
        assert i18n.get("age_group", values={"age": 25}) == "Adult"

    def test_memoization(self, memoization_locales: LocaleDict) -> None:
        """Test that memoization works."""
        i18n = I18nModern("en", memoization_locales)

        # First call
        result1 = i18n.get("greeting", values={"name": "World"})
        # Second call should be cached
        result2 = i18n.get("greeting", values={"name": "World"})

        assert result1 == result2 == "Hello, World!"

    def test_load_from_value(self) -> None:
        """Test loading from value."""
        i18n = I18nModern("en")
        i18n.load_from_value({"welcome": "Welcome!"}, "en")

        assert i18n.get("welcome") == "Welcome!"

    def test_default_locale(self) -> None:
        """Test default locale property."""
        i18n = I18nModern("en")
        assert i18n.default_locale == "en"

        i18n.default_locale = "es"
        assert i18n.default_locale == "es"

    def test_missing_key_returns_key(self, basic_locales: LocaleDict) -> None:
        """Test that missing keys return the key itself."""
        i18n = I18nModern("en", basic_locales)
        assert i18n.get("missing.key") == "missing.key"

    def test_empty_values_dict(self, basic_locales: LocaleDict) -> None:
        """Test translation with empty values dict."""
        i18n = I18nModern("en", basic_locales)
        assert i18n.get("greeting", values={}) == "Hello, [name]!"

    @pytest.mark.parametrize(
        "count,expected",
        [
            (0, "No items"),
            (1, "One item"),
            (2, "2 items"),
            (10, "10 items"),
            (100, "100 items"),
        ],
    )
    def test_conditional_translations_parametrized(
        self, conditional_locales: LocaleDict, count: int, expected: str
    ) -> None:
        """Test conditional translations with multiple values."""
        i18n = I18nModern("en", conditional_locales)
        assert i18n.get("items", values={"count": count}) == expected

    @pytest.mark.parametrize(
        "age,expected",
        [
            (5, "Minor"),
            (17, "Minor"),
            (18, "Adult"),
            (25, "Adult"),
            (65, "Adult"),
        ],
    )
    def test_comparison_conditions_parametrized(
        self, comparison_locales: LocaleDict, age: int, expected: str
    ) -> None:
        """Test comparison conditions with multiple values."""
        i18n = I18nModern("en", comparison_locales)
        assert i18n.get("age_group", values={"age": age}) == expected


# Additional functional tests outside the class for variety
def test_initialization_without_locales() -> None:
    """Test that I18nModern can be initialized without locales."""
    i18n = I18nModern("en")
    assert i18n.default_locale == "en"


def test_initialization_with_empty_dict() -> None:
    """Test that I18nModern can be initialized with empty dict."""
    i18n = I18nModern("en", {})
    assert i18n.default_locale == "en"


def test_get_nonexistent_key_with_values() -> None:
    """Test getting a nonexistent key with values."""
    i18n = I18nModern("en", {})
    result = i18n.get("nonexistent", values={"name": "test"})
    assert result == "nonexistent"


def test_multiple_locale_setting() -> None:
    """Test that default_locale can be changed multiple times."""
    i18n = I18nModern("en")

    # Change locale multiple times
    i18n.default_locale = "es"
    assert i18n.default_locale == "es"

    i18n.default_locale = "fr"
    assert i18n.default_locale == "fr"

    i18n.default_locale = "de"
    assert i18n.default_locale == "de"


def test_load_from_directory() -> None:
    """Test loading all files from a directory."""
    from pathlib import Path

    # Use the example directory with multiple YAML files
    examples_dir = Path(__file__).parent.parent / "examples" / "locales" / "es_MX"

    if examples_dir.exists():
        i18n = I18nModern("es_MX")
        i18n.load_from_directory(str(examples_dir), locale_identify="es_MX")

        # Check that files were loaded and merged
        # From auth.yml
        assert i18n.get("auth.login", locale="es_MX") == "Iniciar sesión"
        # From common.yml
        assert (
            i18n.get("common.welcome", locale="es_MX")
            == "Bienvenido a nuestra aplicación"
        )
        # From document.yml
        assert i18n.get("document.create", locale="es_MX") == "Crear documento"
        # From roles.yml
        assert i18n.get("roles.admin", locale="es_MX") == "Administrador"
        # From users.yml
        assert i18n.get("users.name", locale="es_MX") == "Nombre"


def test_load_from_directory_with_auto_locale_name() -> None:
    """Test that directory name is used as locale when not specified."""
    from pathlib import Path

    examples_dir = Path(__file__).parent.parent / "examples" / "locales" / "es_MX"

    if examples_dir.exists():
        i18n = I18nModern("es_MX")
        # Don't specify locale_identify, should use directory name "es_MX"
        i18n.load_from_directory(str(examples_dir))

        # Should be able to get translations using the directory name
        assert i18n.get("auth.login", locale="es_MX") == "Iniciar sesión"


def test_load_from_directory_not_found() -> None:
    """Test that loading from nonexistent directory raises FileNotFoundError."""
    i18n = I18nModern("en")

    with pytest.raises(FileNotFoundError):
        i18n.load_from_directory("/nonexistent/path", locale_identify="en")


def test_load_from_directory_not_a_directory() -> None:
    """Test that loading from a file path raises ValueError."""
    from pathlib import Path

    # Use a file that exists
    file_path = Path(__file__).parent.parent / "README.md"

    if file_path.exists():
        i18n = I18nModern("en")

        with pytest.raises(ValueError, match="not a directory"):
            i18n.load_from_directory(str(file_path), locale_identify="en")


def test_load_from_directory_filename_as_namespace() -> None:
    """Test that filename stem is used as namespace when set per call."""
    import tempfile
    from pathlib import Path

    i18n = I18nModern("en")  # instance default is False

    with tempfile.TemporaryDirectory() as tmpdir:
        common_yaml = Path(tmpdir, "common.yaml")
        common_yaml.write_text(
            'hello: "Hola"\n'
            "errors:\n"
            '  unexpected: "Ha ocurrido un error inesperado"\n'
            '  unauthorized: "No autorizado"\n'
            '  forbidden: "Acceso denegado"\n'
            '  not_found: "Recurso no encontrado"\n'
            '  validation_failed: "La validacion ha fallado"\n'
            '  conflict: "Conflicto en la solicitud"\n'
            "messages:\n"
            '  operation_success: "Operacion realizada correctamente"\n'
            '  created: "Recurso creado correctamente"\n'
            '  updated: "Recurso actualizado correctamente"\n'
            '  deleted: "Recurso eliminado correctamente"\n',
            encoding="utf-8",
        )

        # Override at call level
        i18n.load_from_directory(
            tmpdir, locale_identify="en", use_filename_as_namespace=True
        )

        assert i18n.get("common.hello") == "Hola"
        assert i18n.get("common.errors.unexpected") == "Ha ocurrido un error inesperado"
        assert i18n.get("common.errors.unauthorized") == "No autorizado"
        assert i18n.get("common.errors.forbidden") == "Acceso denegado"
        assert i18n.get("common.errors.not_found") == "Recurso no encontrado"
        assert i18n.get("common.errors.validation_failed") == "La validacion ha fallado"
        assert i18n.get("common.errors.conflict") == "Conflicto en la solicitud"
        assert (
            i18n.get("common.messages.operation_success")
            == "Operacion realizada correctamente"
        )
        assert i18n.get("common.messages.created") == "Recurso creado correctamente"
        assert (
            i18n.get("common.messages.updated") == "Recurso actualizado correctamente"
        )
        assert i18n.get("common.messages.deleted") == "Recurso eliminado correctamente"


def test_load_from_directory_filename_as_namespace_instance_default() -> None:
    """Test that instance-level use_filename_as_namespace=True is used by default."""
    import tempfile
    from pathlib import Path

    # Set namespace behaviour at instantiation — no need to pass it per call
    i18n = I18nModern("en", use_filename_as_namespace=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        Path(tmpdir, "common.yaml").write_text(
            'hello: "Hola"\nerrors:\n  unexpected: "Error inesperado"\n',
            encoding="utf-8",
        )

        i18n.load_from_directory(tmpdir, locale_identify="en")  # no override needed

        assert i18n.get("common.hello") == "Hola"
        assert i18n.get("common.errors.unexpected") == "Error inesperado"


def test_load_from_directory_filename_as_namespace_call_override() -> None:
    """Test that a per-call override can disable instance-level namespace."""
    import tempfile
    from pathlib import Path

    # Instance enables namespace by default
    i18n = I18nModern("en", use_filename_as_namespace=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        Path(tmpdir, "common.yaml").write_text(
            'hello: "Hola"\n',
            encoding="utf-8",
        )

        # Explicitly disable namespace for this single call
        i18n.load_from_directory(
            tmpdir, locale_identify="en", use_filename_as_namespace=False
        )

        # Key should be flat (no namespace prefix)
        assert i18n.get("hello") == "Hola"
        # Namespaced key should NOT exist
        assert i18n.get("common.hello") == "common.hello"  # returns key on miss


def test_load_from_directory_filename_as_namespace_property_setter() -> None:
    """Test toggling use_filename_as_namespace via the property setter."""
    import tempfile
    from pathlib import Path

    i18n = I18nModern("en")
    assert i18n.use_filename_as_namespace is False

    i18n.use_filename_as_namespace = True
    assert i18n.use_filename_as_namespace is True

    with tempfile.TemporaryDirectory() as tmpdir:
        Path(tmpdir, "users.yaml").write_text(
            'name: "Nombre"\n',
            encoding="utf-8",
        )

        i18n.load_from_directory(tmpdir, locale_identify="en")

        assert i18n.get("users.name") == "Nombre"


def test_load_from_directory_filename_as_namespace_multiple_files() -> None:
    """Test filename-as-namespace with multiple files in the same directory."""
    import tempfile
    from pathlib import Path

    i18n = I18nModern("en")

    with tempfile.TemporaryDirectory() as tmpdir:
        Path(tmpdir, "auth.yaml").write_text(
            'login: "Log in"\nlogout: "Log out"\n',
            encoding="utf-8",
        )
        Path(tmpdir, "users.yaml").write_text(
            'name: "Name"\nemail: "Email"\n',
            encoding="utf-8",
        )

        i18n.load_from_directory(
            tmpdir, locale_identify="en", use_filename_as_namespace=True
        )

        assert i18n.get("auth.login") == "Log in"
        assert i18n.get("auth.logout") == "Log out"
        assert i18n.get("users.name") == "Name"
        assert i18n.get("users.email") == "Email"


def test_load_from_directory_no_supported_files() -> None:
    """Test that loading from directory with no supported files raises ValueError."""
    import tempfile
    from pathlib import Path

    i18n = I18nModern("en")

    # Create a temporary directory with no supported files
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some non-supported files
        Path(tmpdir, "file.txt").write_text("Some text")
        Path(tmpdir, "file.md").write_text("# Markdown")

        with pytest.raises(ValueError, match="No supported locale files found"):
            i18n.load_from_directory(tmpdir, locale_identify="en")
