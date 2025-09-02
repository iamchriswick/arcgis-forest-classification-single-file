# Changelog - Single File Python Script Development

All notable changes to the Forest Classification Tool single file implementation will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2025-09-02

### Added

- **Comprehensive IMPORT_FIELDS.md validation** system covering all 48 required fields across 14 data categories
- **Workspace-relative path resolution** for all source layer validation
- **Granular progress tracking** with 1% minimum increments (0-10% setup, 10-60% source validation, 60-90% field validation, 90-100% completion)
- **Stop-on-first-error validation approach** with detailed error messages
- **Enhanced field validation functions**:
  - `validate_source_layers()` - checks existence of all 14 source datasets
  - `validate_field_availability()` - validates all 48 fields exist in their respective sources
- **Complete IMPORT_FIELDS dictionary** mapping all required fields to source layers:
  - Age Data (4 fields), Species (1 field), Biomass (6 fields), Volume (6 fields)
  - Height (6 fields), Site Index (1 field), Diameter (6 fields), Basal Area (3 fields)
  - Tree Density (12 fields), Leaf Area Index (3 fields), Crown Coverage (1 field)
  - Elevation (3 fields), Soil Properties (3 fields), Location (2 fields)

### Changed

- **Thread Count parameter** locked to single-threaded processing (value=1) for Phase 2 validation focus
- **Progress tracking** enhanced from basic messages to precise percentage-based validation workflow
- **Error handling** upgraded from generic messages to specific field/source error reporting format: `"{field_name} not found in {source_path}"`
- **Tool description** updated to reflect comprehensive validation capabilities across all data categories

### Technical Details

- Phase 2 implements **mandatory 8-step development workflow**: RESEARCH → SPECIFY → DESIGN → CODE → DOCUMENT → TEST → CLEANUP → ITERATE
- Maintains same 3 parameters from Phase 1 for architectural consistency
- Inherited comprehensive system capabilities logging from Phase 1
- Single-threaded processing ensures reliable validation sequence
- Workspace-relative paths support flexible deployment scenarios

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
