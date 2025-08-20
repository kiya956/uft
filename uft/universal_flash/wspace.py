"""Provide create temp work space and handle leaving"""

import os
import tempfile
from contextlib import contextmanager


@contextmanager
def temp_local_directory():
    """Create a temporary directory and move into it."""

    current_dir = os.getcwd()

    with tempfile.TemporaryDirectory(
        prefix="uft-",
        ignore_cleanup_errors=False,
    ) as temp_dir:
        try:
            os.chdir(temp_dir)
            yield temp_dir
        finally:
            os.chdir(current_dir)

