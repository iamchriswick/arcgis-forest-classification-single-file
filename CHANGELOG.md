# Changelog - Single File Python Script Development

All notable changes to the Forest Classification Tool single file implementation will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2025-08-28

### Added

- Dynamic system capability detection using `psutil` library
- Automatic CPU core detection for thread count options
- Automatic memory detection for RAM allocation options
- System information logging in execute method
- Fallback values for system detection failures

### Changed

- Thread Count parameter now shows 3 dynamic options based on detected CPU cores:
  - Conservative (25% of cores, min 1)
  - Balanced (50% of cores, min 2) - Default
  - Performance (75% of cores, min 3)
- Memory Allocation parameter now shows 3 dynamic options based on available RAM:
  - Conservative (25% of available RAM, min 2 GB)
  - Balanced (50% of available RAM, min 4 GB) - Default
  - Performance (75% of available RAM, min 6 GB)
- Toolbox and tool labels updated to include version number
- Execute method now logs detected system capabilities

### Technical Details

- Added `os` and `psutil` imports for system detection
- Added `get_system_capabilities()` function
- Added `create_dynamic_thread_options()` function
- Added `create_dynamic_memory_options()` function
- Enhanced parameter creation logic with dynamic value assignment

## [0.1.1] - 2025-08-28

### Added

- Initial Phase 1 implementation
- Basic ArcGIS toolbox class structure
- Parameter definition for output layer, thread count, and memory allocation
- Simple execute method with progress messages
- Basic logging to ArcGIS Pro messages
- Comprehensive test suite with 13 tests
- 98% test coverage

### Features

- Output Feature Layer parameter (GPFeatureLayer)
- Thread Count parameter with 4 static options
- Memory Allocation parameter with 4 static options
- Progress tracking and logging
- ArcGIS Pro integration support

### Technical Details

- Single file Python script approach
- ArcGIS Pro toolbox (.py) format
- Compatible with ArcGIS Pro conda environment
- Supports both polygon and point feature layers
