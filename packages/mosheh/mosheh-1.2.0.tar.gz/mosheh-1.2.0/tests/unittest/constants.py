from string import Formatter

from mosheh.constants import (
    ACCEPTABLE_LOWER_CONSTANTS,
    ASSERT_MD_STRUCT,
    ASSIGN_MD_STRUCT,
    BUILTIN_DUNDER_METHODS,
    BUILTIN_FUNCTIONS,
    BUILTIN_MODULES,
    CLASS_DEF_MD_STRUCT,
    DEFAULT_MKDOCS_YML,
    FILE_MARKDOWN,
    FUNCTION_DEF_MD_STRUCT,
    IMPORT_MD_STRUCT,
)


def is_formatable_and_get_fields(s: str) -> tuple[bool, list[str] | None]:
    formatter: Formatter = Formatter()
    fields: list[str] = []

    try:
        for _, field_name, _, _ in formatter.parse(s):
            if field_name is not None:
                fields.append(field_name)
        return True, fields if fields else None
    except ValueError:
        return False, None


def test_BUILTIN_MODULES():
    assert isinstance(BUILTIN_MODULES, list)
    assert all(map(lambda x: isinstance(x, str), BUILTIN_MODULES))


def test_BUILTIN_FUNCTIONS():
    assert isinstance(BUILTIN_FUNCTIONS, list)
    assert all(map(lambda x: isinstance(x, str), BUILTIN_FUNCTIONS))


def test_BUILTIN_DUNDER_METHODS():
    assert isinstance(BUILTIN_DUNDER_METHODS, list)
    assert all(map(lambda x: isinstance(x, str), BUILTIN_DUNDER_METHODS))


def test_ACCEPTABLE_LOWER_CONSTANTS():
    assert isinstance(ACCEPTABLE_LOWER_CONSTANTS, list)
    assert all(map(lambda x: isinstance(x, str), ACCEPTABLE_LOWER_CONSTANTS))


def test_DEFAULT_MKDOCS_YML():
    assert isinstance(DEFAULT_MKDOCS_YML, str)
    assert is_formatable_and_get_fields(DEFAULT_MKDOCS_YML) == (
        True,
        ['proj_name', 'repo_url', 'repo_name', 'edit_uri', 'logo_path', 'logo_path'],
    )


def test_FILE_MARKDOWN():
    assert isinstance(FILE_MARKDOWN, str)
    assert is_formatable_and_get_fields(FILE_MARKDOWN) == (
        True,
        [
            'filename',
            'filepath',
            'filedoc',
            'imports',
            'constants',
            'classes',
            'functions',
            'assertions',
        ],
    )


def test_IMPORT_MD_STRUCT():
    assert isinstance(IMPORT_MD_STRUCT, str)
    assert is_formatable_and_get_fields(IMPORT_MD_STRUCT) == (
        True,
        ['name', '_path', 'category', 'code'],
    )


def test_ASSIGN_MD_STRUCT():
    assert isinstance(ASSIGN_MD_STRUCT, str)
    assert is_formatable_and_get_fields(ASSIGN_MD_STRUCT) == (
        True,
        ['token', '_type', 'value', 'code'],
    )


def test_CLASS_DEF_MD_STRUCT():
    assert isinstance(CLASS_DEF_MD_STRUCT, str)
    assert is_formatable_and_get_fields(CLASS_DEF_MD_STRUCT) == (
        True,
        ['name', 'inherit', 'decorators', 'kwargs', 'code'],
    )


def test_FUNCTION_DEF_MD_STRUCT():
    assert isinstance(FUNCTION_DEF_MD_STRUCT, str)
    assert is_formatable_and_get_fields(FUNCTION_DEF_MD_STRUCT) == (
        True,
        ['name', 'rtype', 'decorators', 'args', 'kwargs', 'code'],
    )


def test_ASSERT_MD_STRUCT():
    assert isinstance(ASSERT_MD_STRUCT, str)
    assert is_formatable_and_get_fields(ASSERT_MD_STRUCT) == (
        True,
        ['test', 'msg', 'code'],
    )
