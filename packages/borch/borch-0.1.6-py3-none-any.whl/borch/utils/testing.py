"""Utilities to help with writing tests."""

import re
import sys
from doctest import testmod
from glob import glob
from importlib import import_module
from unittest import mock

TEST_FILE_RE = re.compile(r"test.*/test_.*py$")
DOCTEST_ALLOWED_MODULES_NOT_FOUND = ["modin", "mxnet"]


def get_python_files(source_dirs: tuple):
    """Get all Python files under directories ``source_dirs``."""
    for source_dir in source_dirs:
        yield from glob(f"{source_dir}/**/*.py", recursive=True)


def get_source_files(source_dirs: tuple):
    """Find Python source code files (i.e. files excluding tests) under
    directories ``source_dirs``.
    """
    for path in get_python_files(source_dirs):
        if not TEST_FILE_RE.search(path):
            yield path


def filepath_to_import_path(path: str) -> str:
    """Convert filepath ``path`` to a corresponding import path."""
    return re.sub(r"\.py$", "", re.sub("/", ".", path))


def _run_doctest(module, doctest_options: int = 0):
    """Run doctest on a module and raise assertion error on failure."""
    result = testmod(module, optionflags=doctest_options)
    assert not result.failed  # noqa: S101


def run_doctests(source_dirs: tuple, doctest_options: int = 0):
    """Doctests yielded as functions from a generator as if they were individual
    tests.
    """
    for path in get_source_files(source_dirs):
        try:
            mod = import_module(filepath_to_import_path(path))
            yield lambda: _run_doctest(mod, doctest_options)
        except ModuleNotFoundError as e:  # pragma: no cover
            if not any(name in str(e) for name in DOCTEST_ALLOWED_MODULES_NOT_FOUND):
                raise


def _execfile(path: str) -> tuple:
    """Execute the contents of a file in an isolated environment and return
    the evaluated globals. The argument `sys_modules` is used as a replacement
    for `sys.modules` during execution.
    """
    with open(path) as f:
        source = f.read()
    _globals = {}
    exec(source, _globals)  # noqa: S102
    return _globals


class ScriptTest:
    """A mixin class for running tests on scripts.

    The first thing that occurs in each subclass is that the script is
    run, and the resultant global variables and stubbed out import calls
    are set as the class attributes `globals` and `imports`, respectively.
    These can then be use to test against.

    If any logic must be performed before running the script, this should
    be defined in an overriden classmethod `before_script`.

    Any logic required following all tests can be included in the
    classmethod `tearDownClass` as usual.

    **NB the script is run once and only once. Care must be taken to avoid
    manipulating the outputs in `cls.{globals,imports}`.**

    The class attribute `mock_imports` determines which modules will be
    stubbed out before the script is executed. These can also be tested
    against. As an axample, if `mock_imports` were set to: `("matplotlib",
    "matplotlib.pyplot")` we could check that `matplotlib.pyplot.show`
    has been called by: `self.imports.pyplot.show.assert_called()` (NB
    the name is still pyplot regardless of the alias it was imported as).
    All method calls can be found in `self.imports.pyplot.method_calls`.

    Notes:
        **This class must be the dominant class!** The methods here must
        come first in the MRO. I.e. a subclass must be defined like:
        `class TestAScript(ScriptTest, TestCase)`.

        **The class attribute `path` must be set as the path to the target
        script.**

        At least one test must exist in the test case for the test to be
        discovered and the script run.
    """

    mock_imports = ()

    @property
    @classmethod
    def path(cls):
        """Path to tutorial script."""
        raise NotImplementedError

    @classmethod
    def before_script(cls):
        """Override with code to execute before the script is run."""

    @classmethod
    def setUpClass(cls):
        """Execute `cls.before_script`, then the script at `cls.path`, storing
        all objects in `cls.globals`.
        """
        for mod in cls.mock_imports:
            sys.modules[mod] = mock.MagicMock() # pragma: no cover
        cls.before_script()
        cls.globals = _execfile(cls.path)
