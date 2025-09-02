# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-

(
    """Validation tests package"""
    """
Validation Tests Package

Tests for ToolValidator classes and GUI enhancement features including:
- Helper function validation (CPU cores, memory detection)
- ToolValidator lifecycle methods (initializeParameters, updateParameters)
- Enhanced dropdown population and system capability display
- Error handling and graceful degradation
- ArcGIS Pro .atbx Script tool compatibility

Each toolbox_0_N subdirectory contains validation tests for that specific phase.
"""
)

import unittest
import os


def run_all_validation_tests(verbosity=2):
    """
    Run all validation tests across all phases.

    Args:
        verbosity (int): Test output verbosity (0=quiet, 1=normal, 2=verbose)

    Returns:
        unittest.TestResult: Test results
    """
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)


def run_validation_phase_tests(phase_num, verbosity=2):
    """
    Run validation tests for a specific phase.

    Args:
        phase_num (int): Phase number (1, 2, etc.)
        verbosity (int): Test output verbosity

    Returns:
        unittest.TestResult: Test results
    """
    loader = unittest.TestLoader()
    base_dir = os.path.dirname(__file__)
    phase_dir = os.path.join(base_dir, f"toolbox_0_{phase_num}")

    if not os.path.exists(phase_dir):
        print(
            f"Warning: Phase {phase_num} validation tests directory not found: {phase_dir}"
        )
        return None

    suite = loader.discover(phase_dir, pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)


def get_available_phases():
    """
    Get list of available validation test phases.

    Returns:
        list: List of available phase numbers
    """
    base_dir = os.path.dirname(__file__)
    phases = []

    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and item.startswith("toolbox_0_"):
            try:
                phase_num = int(item.split("_")[-1])
                phases.append(phase_num)
            except ValueError:
                continue

    return sorted(phases)


# Package metadata
__version__ = "0.1.0"
__focus__ = "ToolValidator and GUI enhancement testing"
