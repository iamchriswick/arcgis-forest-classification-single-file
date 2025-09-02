# KISS Task System Documentation

## Overview

The KISS (Keep It Simple Stupid) task system replaces complex parameterized tasks with 3 ultra-simple VS Code tasks that automatically detect source paths from dotted test paths.

## New Tasks

### `tests_single`

- **Purpose**: Run a single test without coverage analysis
- **Input**: Single dotted test path
- **Example**: `single_file_python_script.tests.execution.toolbox_0_1.test_toolbox_0_1_12.TestExecution.test_auto_multithreading_handling`

### `tests_single_coverage`

- **Purpose**: Run a single test with coverage analysis and auto-detected source path
- **Input**: Single dotted test path
- **Magic**: Automatically detects correct source path using `helper_tests.py`
- **Example**: Same as above

### `tests_single_coverage_report`

- **Purpose**: Generate coverage report after running `tests_single_coverage`
- **Input**: None (depends on previous task)
- **Output**: Detailed coverage report with missing lines

## Auto-Detection Algorithm

The `helper_tests.py` script transforms test paths to source paths:

```
Input:  single_file_python_script.tests.execution.toolbox_0_1.test_toolbox_0_1_12.TestExecution.test_method
Output: single_file_python_script/src/execution/toolbox_0_1

Input:  tests.test_classification.test_species_calculator
Output: src
```

### Transformation Rules

1. **Single File Python Script Tests**:
   - Pattern: `single_file_python_script.tests.*`
   - Rule: Replace `.tests.` with `/src/`, remove test file parts, convert dots to slashes
2. **Main Project Tests**:
   - Pattern: `tests.*`
   - Rule: Use `src` as source path
3. **Fallback**:
   - Unknown patterns default to `single_file_python_script/src`

## Usage Examples

### Example 1: Full Test Method Path

```
Task: tests_single_coverage
Input: single_file_python_script.tests.execution.toolbox_0_1.test_toolbox_0_1_12.TestExecution.test_auto_multithreading_handling
Auto-detected source: single_file_python_script/src/execution/toolbox_0_1
```

### Example 2: Test Class Path

```
Task: tests_single_coverage
Input: single_file_python_script.tests.validation.toolbox_0_1.test_validation_toolbox_0_1_12.TestValidation
Auto-detected source: single_file_python_script/src/validation/toolbox_0_1
```

### Example 3: Test Module Path

```
Task: tests_single_coverage
Input: single_file_python_script.tests.execution.toolbox_0_2.test_toolbox_0_2_12
Auto-detected source: single_file_python_script/src/execution/toolbox_0_2
```

### Example 4: Main Project Test

```
Task: tests_single_coverage
Input: tests.test_classification.test_species_calculator
Auto-detected source: src
```

## Workflow Comparison

### OLD Complex System (6+ parameters)

```
Task: tests_toolbox_coverage
Inputs Required:
- source_module: "single_file_python_script/src/execution/toolbox_0_1"
- test_module: "single_file_python_script.tests.execution.toolbox_0_1.test_toolbox_0_1_12"
```

### NEW KISS System (1 parameter)

```
Task: tests_single_coverage
Input: single_file_python_script.tests.execution.toolbox_0_1.test_toolbox_0_1_12
→ Auto-detects source path automatically!
```

## Benefits

1. **Simplicity**: Single input instead of multiple parameters
2. **No Manual Mapping**: Source paths automatically detected
3. **Error Reduction**: No more mismatched source/test pairs
4. **Speed**: Faster task execution with fewer prompts
5. **Flexibility**: Works with any test granularity (module, class, method)

## Helper Script Details

**Location**: `single_file_python_script/tests/scripts/helper_tests.py`

**Key Features**:

- Automatic source path detection
- Comprehensive error handling
- Detailed logging output
- Support for complex dotted paths
- Fallback for unknown patterns

## Migration Guide

Replace these legacy tasks with KISS equivalents:

| Legacy Task                 | KISS Replacement        | Notes                         |
| --------------------------- | ----------------------- | ----------------------------- |
| `tests_toolbox_coverage`    | `tests_single_coverage` | Auto-detects source path      |
| `tests_validation_coverage` | `tests_single_coverage` | Same task works for all       |
| `tests_phase_coverage`      | `tests_single_coverage` | No directory selection needed |

## Implementation Notes

- Tasks use existing conda environment: `arcgispro-py3-3780`
- Maintains compatibility with existing test discovery patterns
- Leverages Python module structure with `__init__.py` files
- Zero configuration changes needed for existing test files
