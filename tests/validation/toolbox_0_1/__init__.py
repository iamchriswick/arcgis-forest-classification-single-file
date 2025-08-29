# -*- coding: utf-8 -*-
"""
Test package for Phase 1 Validation Module

This package contains tests for the validation module of toolbox_0_1_*.py files,
specifically testing the ToolValidator class and helper functions for ArcGIS Pro
.atbx Script tool compatibility.
"""

import unittest

# Package metadata
__version__ = "0.1.12"
__phase__ = "Phase 1"
__focus__ = "Basic ToolValidator and GUI enhancement testing"


def load_tests(loader, tests, pattern):
    """
    Load all test cases from this package.
    This function is automatically called by unittest discovery.
    """
    return loader.discover(start_dir=__path__[0], pattern="test_*.py")


def get_test_suite():
    """
    Get a test suite containing all validation tests for Phase 1.
    Usage: python -c "from tests.validation.toolbox_0_1 import get_test_suite; unittest.TextTestRunner().run(get_test_suite())"
    """
    loader = unittest.TestLoader()
    return loader.discover(start_dir=__path__[0], pattern="test_*.py")
