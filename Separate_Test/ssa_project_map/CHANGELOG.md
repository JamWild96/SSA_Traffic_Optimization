# Changelog

## [2.1.0] - 2024-06-11
### Added
- Enhanced Makefile with improved cleaning capabilities
  - `make clean` now properly cleans Python directory files and caches
  - `make deep-clean` removes all generated files and virtual environment 
  - `make distclean` performs complete cleanup including system files (.DS_Store, etc.)
- New Makefile targets for better workflow
  - `make rebuild` for complete rebuild from scratch (including venv setup)
  - `make diagnostics` to help troubleshoot installation issues
  - `make help` to display available commands
- Better error handling in clean/rebuild targets
- Detailed output messages for all maintenance commands

### Fixed
- Virtual environment path references
- Directory structure cleanup
- Test file removal
- Python cache directory cleanup

### Improved
- Documentation in README.md about maintenance commands
- Feedback messages during clean/rebuild operations
- Test script to use the new clean target before testing

## [2.0.0] - 2024-06-10
### Changed
- Complete architectural overhaul
- Moved all data generation responsibility to C program
- Python scripts now only handle visualization

### Added
- C program now generates:
  - Graph and node coordinates
  - Building and traffic jam data
  - Visit frequency data and statistics

### Fixed
- Numerous memory management issues in C code
- CSV parsing and formatting
- CUDA integration issues

## [1.0.0] - 2024-05-22
### Added
- Initial implementation of Sparrow Search Algorithm
- Hybrid C/Python implementation
- Support for custom parameters
- Visualization tooling