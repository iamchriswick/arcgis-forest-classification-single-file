# -*- coding: utf-8 -*-
"""
Execution Tests Package

Tests for main toolbox functionality including:
- Tool initialization and parameter handling
- Execute method behavior and progress tracking
- System capability detection (CPU, memory)
- Integration with ArcGIS Pro environment
- Multi-threading and performance features

Each toolbox_0_N subdirectory contains tests for that specific phase implementation.
"""

import unittest
import os


def run_all_execution_tests(verbosity=2):
    """
    Run all execution tests across all phases.

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


def run_execution_phase_tests(phase_num, verbosity=2):
    """
    Run execution tests for a specific phase.

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
            f"Warning: Phase {phase_num} execution tests directory not found: {phase_dir}"
        )
        return None

    suite = loader.discover(phase_dir, pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)


def get_available_phases():
    """
    Get list of available execution test phases.

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
__focus__ = "Toolbox execution functionality testing"
