# Single-File Development Testing Strategy

This directory contains test files that correspond to each phase of the single-file development approach for the Forest Classification Toolbox.

## Testing Convention

Each development file follows this naming pattern:

```
single_file_python_script/toolbox_0_{phase}_{patch}.py
```

Each test file follows this naming pattern:

```
single_file_python_script/tests/test_toolbox_0_{phase}_{patch}.py
```

## Phase-by-Phase Testing

| Phase | Development File    | Test File                | Test Focus                     |
| ----- | ------------------- | ------------------------ | ------------------------------ |
| 1     | `toolbox_0_1_1.py`  | `test_toolbox_0_1_1.py`  | Basic ArcGIS toolbox structure |
| 2     | `toolbox_0_2_1.py`  | `test_toolbox_0_2_1.py`  | Parameter validation           |
| 3     | `toolbox_0_3_1.py`  | `test_toolbox_0_3_1.py`  | Basic data reading             |
| ...   | ...                 | ...                      | ...                            |
| 13    | `toolbox_0_13_1.py` | `test_toolbox_0_13_1.py` | Complete modular refactoring   |

## Test Execution

Use the existing project test infrastructure:

```powershell
# Run all tests including single-file tests
run_task tests_all

# Run specific single-file test
conda run -n arcgispro-py3-3780 python -m unittest single_file_python_script.tests.test_toolbox_0_1_1 -v
```

## Test Structure

Each test file should:

- Import the corresponding toolbox module
- Test the specific functionality added in that phase
- Use unittest framework consistent with existing project
- Handle ArcPy availability gracefully (skip tests if not available)
- Include placeholder tests that can be expanded as functionality is added

## Benefits

1. **Incremental Validation**: Each phase can be tested independently
2. **Regression Prevention**: Existing functionality is validated as new features are added
3. **Quality Assurance**: Maintains code quality throughout development
4. **Documentation**: Tests serve as examples of how each phase should work
5. **Debugging**: Isolated test failures help identify issues quickly
