# Changelog

## Types of changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities

---

## [10] - 2025-09-16

### Added
- Initial release with CLI-based scraping
- Support for MyAnimeList seasonal data
- Nekopoi hentai schedule scraping
- Auto-installer for Python and dependencies
- Indonesian language interface
- English version available

### Changed
- N/A (initial release)

### Fixed
- N/A (initial release)

## [11.1] - 2025-09-16

### Added
- Script source
- python-publish.yml
- README.en.md

### Changed
- Change Start.bat
- Change README.md
- Change EN Main Script to same as ID Main Script
- Change Phrase

## [12] - 2025-09-16

### Added
- Added global data_usage and session_data_usage variables.
- Added `timeout=15` to all `requests.get()` calls
- Added `animation_thread.join()` after stopping animations in both scraping functions
- Added `print_status()`
- Added `"Member : {member}"` line to the output file header
- Added session_data_usage to global declarations in scraping functions
- Added loading/saving of cumulative data usage to/from data_usage.txt for cross-session tracking.

### Changed
- Changed the default output filename
- Change the Member Threshold Logic
- Changed from grouped dates to individual date lines for each anime,

### Fixed
- Moved the member threshold input
- Updated the custom filename prompt to show the calculated default
- Updated the member threshold prompt to include an example and clarify that inputs without suffix

### Remove
- Removed `scrape_aired()` function

## [Unreleased 13] - 2025-11-21

### Added
- Desktop GUI (`gui_scraper.py`): User-friendly graphical interface with Tkinter
  - Input forms for year, season, member threshold
  - Progress bars and real-time status updates
  - Preview of scraped results
  - Search and filtering capabilities
  - Multi-format export (TXT, JSON, CSV, PDF)
  - Separate scraping options (MAL only, Nekopoi only, or both)
  - Multi-language support (9 languages)
- Multi-Language Support (`localization.py`): Complete localization system
  - Support for 9 languages: Indonesian, English, Japanese, Spanish, Chinese, Korean, French, German, Portuguese
  - Dynamic language switching in GUI
  - Extensible translation framework
  - Header templates for MAL, both, and Nekopoi sources in all supported languages
- Multi-Format Export: Support for JSON, CSV, and PDF outputs
- Enhanced Error Handling: Retry logic with exponential backoff
- Proxy Support: Optional proxy configuration for anti-bot measures
- Search & Filtering: Real-time search by title, genre, studio, member count

### Changed
- Enhanced scraping functions with retry and proxy parameters
- Updated dependencies in `requirements.txt`
- Improved documentation with GUI usage examples
- Modified `Start.bat` startup flow: All users (CLI and GUI) now must go through Python check and requirements installation before mode selection

### Technical Improvements
- Modular code structure with separate GUI components
- Better error handling and logging
- Threading support for non-blocking GUI operations
- Data validation and input sanitization

---

## Version Numbering
This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 13.1.0)
- MAJOR: Breaking changes
- MINOR: New features, backward compatible

- PATCH: Bug fixes, backward compatible

## Source
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
