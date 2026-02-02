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

## [11.1] - 2025-09-30

### Added
- Script source
- python-publish.yml
- README.en.md

### Changed
- Change Start.bat
- Change README.md
- Change EN Main Script to same as ID Main Script
- Change Phrase

## [12] - 2025-10-13

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

## [13] - 2025-11-21

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

## [14] - 2026-02-02

### Added
- Full multi-language support in `localization.py` for 9 languages: Indonesian (id), English (en), Japanese (ja), Spanish (es), Chinese (zh), Korean (ko), French (fr), German (de), Portuguese (pt)
- Separate header templates: `header_template_both`, `header_template_mal`, `header_template_nekopoi` – dynamically selected based on user scrape option (MAL only, Nekopoi only, or Both)
- Consistent placeholders `{nekopoi_month}` and `{schedule_info}` across all languages and templates for Nekopoi schedule info
- Logging for Hentai and Erotica counts during MAL scraping (e.g., "Found X anime entries for Hentai", "Found Y anime entries for Erotica")
- Logging for total Nekopoi entries in CLI output
- Updated CLI header to "VERSI 14 - TheKingTermux" in both Indonesian and English scripts

### Changed
- Header template in `localization.py` for all languages: Removed old placeholders like `{first_month - last_month}`, `{ahead_text}`, `{month_has_passed}`; replaced with clean `{nekopoi_month} bulan/months/... {schedule_info}`
- Nekopoi schedule text standardized to "jadwalnya cuma {nekopoi_month} bulan {schedule_info}" (id) and equivalents in other languages
- `save_to_file` logic in `gui_functions.py` improved for schedule_info calculation (safer indentation, fallback for no data)
- CLI scripts (`MyAnimeList_and_Nekopoi_Scrapper.py` & English version): Version bumped to 14, log output enhanced with hentai/erotica/nekopoi counts

### Fixed
- Error 'first_month - last_month' when formatting header (caused by legacy placeholders in localization.py)
- Indentation bug in Nekopoi month calculation (month_has_passed & last_month undefined in some cases)
- GUI language switching now fully recreates widgets with new header templates and scrape options
- Removed zombie placeholders from templates to prevent KeyError during .format()

### Removed
- Legacy placeholders `{first_month - last_month}`, `{ahead_text}`, `{month_has_passed}` from all header templates
- Old single-template header approach; now uses 3 dedicated templates for better flexibility

### Technical Notes
- All core scraping functionality remains backward compatible
- GUI now supports dynamic header selection based on scrape mode
- Tested with all 9 languages; no placeholder errors during save
- Recommended for users upgrading from v13: Replace localization.py fully, update gui_functions.py save_to_file logic

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