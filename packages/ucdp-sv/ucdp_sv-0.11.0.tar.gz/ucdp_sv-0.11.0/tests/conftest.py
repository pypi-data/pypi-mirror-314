"""Pytest Configuration and Fixtures."""

from pathlib import Path

import ucdp as u
from pytest import fixture


@fixture
def example():
    """Add access to ``example``."""
    example_path = Path(__file__).parent / "testdata" / "example"
    with u.extend_sys_path((example_path,)):
        yield example_path
