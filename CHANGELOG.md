# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Desktop GUI** (`gui_scraper.py`): User-friendly graphical interface with Tkinter
  - Input forms for year, season, member threshold
  - Progress bars and real-time status updates
  - Preview of scraped results
  - Search and filtering capabilities
  - Multi-format export (TXT, JSON, CSV, PDF)
  - Separate scraping options (MAL only, Nekopoi only, or both)
  - Multi-language support (9 languages)
- **Multi-Language Support** (`localization.py`): Complete localization system
  - Support for 9 languages: Indonesian, English, Japanese, Spanish, Chinese, Korean, French, German, Portuguese
  - Dynamic language switching in GUI
  - Extensible translation framework
- **Multi-Format Export**: Support for JSON, CSV, and PDF outputs
- **Enhanced Error Handling**: Retry logic with exponential backoff
- **Proxy Support**: Optional proxy configuration for anti-bot measures
- **Search & Filtering**: Real-time search by title, genre, studio, member count

### Changed
- Enhanced scraping functions with retry and proxy parameters
- Updated dependencies in `requirements.txt`
- Improved documentation with GUI and API usage examples

### Technical Improvements
- Modular code structure with separate GUI and API components
- Better error handling and logging
- Threading support for non-blocking GUI operations
- Data validation and input sanitization

## [10] - 2024-11-XX

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

---

## Types of changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities

## Version Numbering
This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 13.1.0)
- MAJOR: Breaking changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible