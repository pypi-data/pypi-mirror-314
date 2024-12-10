tempfile312
===========

Backport of Python 3.12's `tempfile` library for older Python versions. Notably, supports
the `delete_on_close` parameter to `NamedTemporaryFile` to make it useful on Windows.

See official documentation here: https://docs.python.org/3.12/library/tempfile.html.

Major changes from Python 3.8:
- Added *delete\_on\_close* parameter to `NamedTemporaryFile`
- Added *ignore\_cleanup\_errors* and *delete* parameters to `TemporaryDirectory`
- `gettempdir()` always returns a str. Previously it would return any tempdir value regardless of type so long as it was not `None`.
- `SpooledTemporaryFile` fully implements the `io.BufferedIOBase` and `io.TextIOBase` abstract base classes (depending on whether binary or text mode was specified).
- `mkdtemp()` now always returns an absolute path, even if dir is relative.
