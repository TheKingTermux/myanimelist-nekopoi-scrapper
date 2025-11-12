👉 **[English Version](./README.en.md)**  👉 **[Bingung masalah keamanan dan kurang percaya dengan Skrip ini? Silahkan baca disini untuk info lebih lanjut](https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper/wiki/Masalah-Keamanan%3F-Silakan-baca-ini!)** 

# 🎬 MyAnimeList & Nekopoi Scrapper

[![Python](https://img.shields.io/badge/Python-3.13.3-blue?logo=python)](https://www.python.org/)
![GitHub Release](https://img.shields.io/github/v/release/TheKingTermux/myanimelist-nekopoi-scrapper)
[![Dibuat dengan ❤️](https://img.shields.io/badge/Dibuat%20dengan-%E2%9D%A4-red)]()

> Scraper otomatis untuk mengumpulkan data dari MyAnimeList & Nekopoi, dibuat dengan Python + Requests + BeautifulSoup.  
> Dibungkus dengan `.bat` installer supaya gampang dijalankan siapa aja 🚀

## ✨ Fitur
- 🔍 Mengambil data anime musiman (Normal, Erotica, Hentai) dari **MyAnimeList**
- 🔞 Mengambil metadata hentai dari **NekoPoi**
- 🖥️ Antarmuka Desktop: Antarmuka grafis dengan Tkinter untuk kemudahan penggunaan
- 🌍 Dukungan Multi-Bahasa pada GUI: Mendukung 9 bahasa (Indonesia, Inggris, Jepang, Spanyol, Mandarin, Korea, Prancis, Jerman, Portugis)
- 🔍 Pencarian & Penyaringan: Cari berdasarkan judul, genre, studio, jumlah anggota
- 📊 Ekspor Multi-Format: Simpan hasil dalam format TXT, JSON, CSV, atau PDF
- 🔄 Dukungan Ulang Coba & Proxy: Penanganan kesalahan dengan ulang coba otomatis dan dukungan proxy
- ⚡ Pengaturan otomatis: Jika Python tidak terinstal, skrip akan mengunduh, menginstal, dan kemudian menghapus otomatis file instalasi Python yang diunduh
- 📦 Instal otomatis semua perpustakaan yang diperlukan (`requirements.txt`)
- 🔁 Menu interaktif untuk menjalankan scraper atau menginstal persyaratan

## 📂 Struktur Project
```
├── LISENSI                                     # Lisensi
├── MyAnimeList_and_Nekopoi_Scrapper.py         # Skrip utama (versi Indonesia)
├── MyAnimeList_and_Nekopoi_Scrapper_English.py # Skrip utama (versi bahasa Inggris)
├── gui_scraper.py                              # GUI Desktop dengan Tkinter (dukungan multi-bahasa)
├── localization.py                             # Kode untuk dukungan multi-bahasa
├── requirements.txt                            # Dependensi
├── Start.bat                                   # Berkas batch (installer + runner)
├── AnimeList/                                  # Folder output hasil scraping
├── data_usage.txt                              # Tracking penggunaan data
├── README.md dan README.en.md                  # Dokumentasi proyek
└── CHANGELOG.md                                # Log perubahan versi
```

## 🛠️ Cara Penggunaan

### 1️⃣ Kloning Repositori atau Unduh .zip
```
git clone https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper.git
cd myanimelist-nekopoi-scrapper
```

### ⬇️ [Unduh Rilis Terbaru (.zip Github)](https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper/releases/latest)
### ⬇️ [Unduh Rilis Terbaru (.zip Backup)](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2FTheKingTermux%2Fmyanimelist-nekopoi-scrapper)


### 2️⃣ Jalankan Batch File
Cukup klik 2x `Start.bat` maka tools akan langsung bekerja secara otomatis 

### 3️⃣ Pilihan di Menu

1 → Jalankan Scraper

> Kalau Python belum ada, otomatis diinstall dulu + install requirements → baru scraper jalan

2 → Jalankan GUI Desktop

> Interface grafis untuk kemudahan penggunaan tanpa command line

3 → Install Requirements manual

4 → Keluar

### 🎨 Menggunakan GUI Desktop

```bash
python gui_scraper.py
```

**Fitur GUI:**
- Dukungan 9 bahasa (Indonesia, English, Japanese, Spanish, Chinese, Korean, French, German, Portuguese)
- Form input untuk tahun, musim, threshold member
- Opsi Scraping Terpisah: Checkbox untuk memilih MAL saja, Nekopoi saja, atau keduanya
- Pilihan format export (TXT/JSON/CSV/PDF)
- Tombol scrape dengan progress bar
- Preview hasil scraping
- Pencarian dan filter real-time
- Simpan hasil ke file


## 📦 Requirements

### Sistem
- Windows 10/11 (support .bat)
- Linux/MacOS (manual setup)
- Internet (untuk install Python / library)

### Software
- Python 3.8+ (auto install kalau belum ada)
- Dependencies: `pip install -r requirements.txt` (gunakan Start.bat untuk mempermudah)

### Hardware
- RAM: Minimal 2GB
- Storage: 500MB free space
- CPU: Dual-core 2.0GHz+

## 📋 Changelog

Lihat [CHANGELOG.md](./CHANGELOG.md) untuk detail perubahan versi.

## ⚠️ Disclaimer

- Script ini untuk tujuan edukasi dan personal use saja
- Scraping dapat melanggar Terms of Service situs target
- Gunakan dengan bijak dan bertanggung jawab
- Rate limiting dan proxy support disediakan untuk menghindari pemblokiran

## 🤝 Contributing

Kontribusi welcome! Silakan:
1. [Fork repository](https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper/fork)
2. Buat branch fitur baru
3. Commit changes
4. Push ke branch
5. Buat Pull Request

## ‍💻 Author

Created with ❤️ by TheKingTermux-Sama

## 🙏 Acknowledgments

- MyAnimeList.net untuk data anime
- Nekopoi.care untuk jadwal hentai
- BeautifulSoup4 dan Requests untuk web scraping
- Komunitas open source
