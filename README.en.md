👉 **[Versi Bahasa Indonesia](./README.md)** 👉 **[Confused about security issues and don't trust this script? Please read here for more information](https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper/wiki/Security-Concern%3F-Please-read-this!)** 

# 🎬 MyAnimeList & Nekopoi Scrapper

[![Python](https://img.shields.io/badge/Python-3.13.3-blue?logo=python)](https://www.python.org/)
![GitHub Release](https://img.shields.io/github/v/release/TheKingTermux/myanimelist-nekopoi-scrapper)
[![Made with ❤️](https://img.shields.io/badge/Created%20with-%E2%9D%A4-red)]()

> Automated scraper to collect data from MyAnimeList & Nekopoi, built in Python + Requests + BeautifulSoup.
>
> Wrapped in a `.bat` installer so it's easy for anyone to run 🚀
>
> Use `gui_scraper.py` for more features!.

## ✨ Features
- 🔍 Fetch seasonal anime data (Normal, Erotica, Hentai) from **MyAnimeList**
- 🔞 Fetch hentai metadata from **NekoPoi**
- 🖥️ Desktop Interface: Graphical interface with Tkinter for ease of use
- 🌍 Multi-Language GUI Support: Supports 9 languages ​​(Indonesian, English, Japanese, Spanish, Mandarin, Korean, French, German, Portuguese)
- 🔍 Search & Filter: Search by title, genre, studio, number of members
- 📊 Multi-Format Export: Save results in TXT, JSON, CSV, or PDF formats
- 🔄 Retry & Proxy Support: Error handling with auto-retries and proxy support
- ⚡ Auto-setup: If Python is not installed, the script will download, install, and then automatically uninstall the downloaded Python installation file
- 📦 Auto-install all required libraries (`requirements.txt`)
- 🔁 Interactive menu to run the scraper or install requirements

## 📂 Project Structure
```
├── LICENSE # License
├── MyAnimeList_and_Nekopoi_Scrapper.py         # Main script (Indonesian version)
├── MyAnimeList_and_Nekopoi_Scrapper_English.py # Main script (English version)
├── gui_scraper.py                              # Desktop GUI with Tkinter (multi-language support)
├── localization.py                             # Code for multi-language support
├── requirements.txt                            # Dependencies
├── Start.bat                                   # Batch file (installer + runner)
├── AnimeList/                                  # Output folder Scraping
├── data_usage.txt                              # Data usage tracking
├── README.md and README.en.md                  # Project documentation
└── CHANGELOG.md                                # Version changelog
```

## 🛠️ How to Use

### 1️⃣ Clone the Repository or Download .zip
```
git clone https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper.git
cd myanimelist-nekopoi-scrapper
```

### ⬇️ [Download Latest Release (.zip) Github](https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper/releases/latest)
### ⬇️ [Download Latest Release (.zip) Backup](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2FTheKingTermux%2Fmyanimelist-nekopoi-scrapper)

### 2️⃣ Run the Batch File
Simply double-click `Start.bat` and the tools will run automatically. 

### 3️⃣ Menu Options

1 → Run Scraper

> If Python is not already installed, it will be automatically installed and installed the requirements → then the scraper will run.

2 → Run Desktop GUI

> Graphical interface for ease of use without the command line

3 → Install Requirements Manually

4 → Exit

## 🎨 Using Desktop GUI

```bash
python gui_scraper.py
```

### GUI Features:
- Support for 9 languages ​​(Indonesian, English, Japanese, Spanish, (Chinese, Korean, French, German, Portuguese)
- Input form for year, season, member threshold
- Separate Scraping Options: Checkbox to select MAL only, Nekopoi only, or both
- Export format options (TXT/JSON/CSV/PDF)
- Scrape button with progress bar
- Preview scraping results
- Real-time search and filtering
- Save results to a file

## 📦 Requirements

### System
- Windows 10/11 (supports .bat)
- Linux/MacOS (manual setup)
- Internet (to install Python/libraries)

### Software
- Python 3.8+ (auto-install if not already installed)
- Dependencies: `pip install -r requirements.txt` (use Start.bat for easier access)

### Hardware
- RAM: Minimum 2GB
- Storage: 500MB free space
- CPU: Dual-core 2.0GHz+

## 📋 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version change details.

## ⚠️ Disclaimer

- This script is for educational and personal use only.
- Scraping may violate the target site's Terms of Service.
- Use wisely and responsibly.
- Rate limiting and proxy support are provided to avoid blocking.

## 🤝 Contributing

Contributions are welcome! Please:
1. [Fork repository](https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper/fork)
2. Create a new feature branch.
3. Commit changes.
4. Push to branch.
5. Create a Pull Request.

## 🙏 Acknowledgments

- MyAnimeList.net for anime data
- Nekopoi.care for hentai schedules
- BeautifulSoup4 and Requests for web scraping
- Open source community

## 👨‍💻 Author

Created with ❤️ by TheKingTermux-Sama
