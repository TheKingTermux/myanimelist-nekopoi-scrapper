import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime
import time
import random
import logging
import threading
import sys

# Konfigurasi logging agar tidak mengganggu animasi
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Flag global untuk animasi loading
loading_active = False

def loading_animation(message="🔄 Memproses..."):
    """Menampilkan animasi loading dengan spinner pada baris tersendiri"""
    spinner = ['|', '/', '-', '\\']
    i = 0
    while loading_active:
        sys.stdout.write(f'\r{message} {spinner[i % len(spinner)]}')
        sys.stdout.flush()
        time.sleep(0.15)
        i += 1
    sys.stdout.write(f'\r{message} completed ✓\n')
    sys.stdout.flush()

# Genre berbahaya
# cspell:disable-next-line
DANGER_GENRES = {"Adult", "Boys Love", "Yaoi", "Crossdressing", "Ecchi", "Girls Love", "Yuri", "Hentai", "Erotica"}

# Ekspresi reguler
EPS_REGEX = re.compile(r'(\d+)(?:\s*eps)?')
DURATION_REGEX = re.compile(r'(\d+)\s*min')

def translate_month(date_str):
    """Menerjemahkan nama bulan dari Bahasa Inggris ke Bahasa Indonesia."""
    # cspell:disable-next-line
    month_translation = {
        'January': 'Januari', 'February': 'Februari', 'March': 'Maret',
        'April': 'April', 'May': 'Mei', 'June': 'Juni',
        'July': 'Juli', 'August': 'Agustus', 'September': 'September',
        'October': 'Oktober', 'November': 'November', 'December': 'Desember',
        'Jan': 'Januari', 'Feb': 'Februari', 'Mar': 'Maret',
        'Apr': 'April', 'May': 'Mei', 'Jun': 'Juni',
        'Jul': 'Juli', 'Aug': 'Agustus', 'Sep': 'September',
        'Oct': 'Oktober', 'Nov': 'November', 'Dec': 'Desember'
    }
    # Sort by length descending and replace whole words only
    for eng, indo in sorted(month_translation.items(), key=lambda x: len(x[0]), reverse=True):
        date_str = re.sub(r'\b' + re.escape(eng) + r'\b', indo, date_str)
    return date_str

def parse_date_flexible(date_str):
    """Mengurai string tanggal dengan format yang fleksibel."""
    if date_str == 'Unknown':
        return None
    try:
        return datetime.strptime(date_str, '%b %d, %Y')
    except ValueError:
        try:
            # For partial dates like 'Dec 2025'
            partial = datetime.strptime(date_str, '%b %Y')
            # Assume day 1 for sorting
            return partial.replace(day=1)
        except ValueError:
            return None

def parse_member_count(members_text):
    """Mengonversi teks jumlah anggota (seperti '10K') menjadi bilangan bulat."""
    members_text = members_text.upper().replace(',', '').strip()
    if 'K' in members_text:
        return int(float(members_text.replace('K', '')) * 1000)
    elif 'M' in members_text:
        return int(float(members_text.replace('M', '')) * 1000000)
    else:
        return int(re.sub(r'[^0-9]', '', members_text))

def get_anime_data(entry):
    """Mengekstrak data dari satu entri anime."""
    try:
        # Judul anime
        title_tag = entry.select_one('div.title > div > h2 > a')
        title = title_tag.get_text(strip=True) if title_tag else 'Unknown'
        
        # Jumlah anggota
        members_tag = entry.select_one('div.information > div.information-item.scormem > div > div.scormem-item.member')
        members_text = members_tag.get_text(strip=True) if members_tag else '0'
        members = parse_member_count(members_text)

        # Tanggal rilis
        date_tag = entry.select_one('div.prodsrc > div.info > span:nth-child(1)')
        date_text = date_tag.get_text(strip=True) if date_tag else 'Unknown'
        
        # Episode dan durasi
        eps_dur_tag = entry.select_one('div.prodsrc > div.info > span:nth-child(2)')
        eps_dur_text = eps_dur_tag.get_text(strip=True) if eps_dur_tag else ''
        
        # Ekstrak jumlah episode dan durasi
        eps_count = EPS_REGEX.search(eps_dur_text)
        duration_min = DURATION_REGEX.search(eps_dur_text)
        eps_count = eps_count.group(1) if eps_count else ''
        duration_min = duration_min.group(1) if duration_min else ''
        
        # Studio
        studio_tag = entry.select_one('div.synopsis.js-synopsis > div > div:nth-child(1) > span.item > a')
        studio = studio_tag.get_text(strip=True) if studio_tag else 'Unknown'
        
        # Tangani kasus di mana studio tidak valid
        if studio in {'?', '0', 'unknown', '', None}:
            studio = 'Unknown'
        
        # Genre
        genres = []
        genre_container = entry.select_one('div.genres-inner')
        if genre_container:
            genres = [genre.get_text(strip=True) for genre in genre_container.find_all('span')]
        
        # Tema
        themes = [theme.get_text(strip=True) for theme in entry.select('div.properties > div:nth-child(3) > span.item')]
        
        # Demografi
        demographics = [demo.get_text(strip=True) for demo in entry.select('div.properties > div:nth-child(4) > span.item')]
        
        return {
            'title': title,
            'members': members,
            'date': date_text,
            'eps': eps_count,
            'duration': duration_min,
            'studio': studio,
            'genres': genres,
            'themes': themes,
            'demographics': demographics,
            'category': None  # Initialize without a category
        }
    
    except Exception as e:
        logging.error(f"Error memproses entri: {str(e)}")
        return None

def scrape_nekopoi():
    """Mengambil jadwal hentai dari Nekopoi.care"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    global loading_active
    try:
        # Mulai animasi loading di thread terpisah
        loading_active = True
        animation_thread = threading.Thread(target=loading_animation, args=("🔄 Mengambil jadwal hentai Nekopoi...",))
        animation_thread.daemon = True
        animation_thread.start()

        time.sleep(random.uniform(3, 7))

        response = requests.get("https://nekopoi.care/jadwal-new-hentai/", headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Temukan semua badan spoiler yang berisi entri hentai
        nekopoi_data = {}

        # Dapatkan semua elemen spoiler-body
        spoiler_bodies = soup.find_all('div', class_='spoiler-body')

        for spoiler_body in spoiler_bodies:
            # Temukan semua entri hentai di spoiler ini
            entries = spoiler_body.find_all('div', recursive=False)

            for entry in entries:
                try:
                    # Judul
                    title_tag = entry.select_one('h2:nth-child(1) > a')
                    title = title_tag.get_text(strip=True) if title_tag else None

                    if not title:
                        continue

                    # Episode
                    eps_tag = entry.select_one('h2:nth-child(1) > span')
                    eps_text = eps_tag.get_text(strip=True) if eps_tag else ''
                    # Ekstrak nomor episode
                    eps_match = re.search(r'Episode (\d+)', eps_text)
                    eps_num = int(eps_match.group(1)) if eps_match else 1

                    # Tanggal Rilis
                    date_tag = entry.select_one('h2:nth-child(3) > span.release_date')
                    release_date = date_tag.get_text(strip=True) if date_tag else None

                    if not release_date:
                        continue

                    # Studio/Produser (coba beberapa pendekatan)
                    studio = 'Unknown'

                    # Coba selector spesifik terlebih dahulu
                    studio_tag = entry.select_one('h2:nth-child(3) > span:nth-child(1) > span > span')
                    if studio_tag:
                        studio = studio_tag.get_text(strip=True)

                    # Jika tidak ditemukan, coba cari pola "Producer / Label :"
                    if studio == 'Unknown':
                        # Cari teks yang berisi "Producer / Label :"
                        producer_text = entry.find(text=lambda text: text and 'Producer / Label :' in text)
                        if producer_text:
                            # Ekstrak nama studio setelah "Producer / Label :"
                            text_parts = producer_text.split('Producer / Label :')
                            if len(text_parts) > 1:
                                studio = text_parts[1].strip()

                    # Kelompokkan berdasarkan tanggal rilis
                    if release_date not in nekopoi_data:
                        nekopoi_data[release_date] = {}

                    if title not in nekopoi_data[release_date]:
                        nekopoi_data[release_date][title] = {'episodes': [eps_num], 'studio': studio}
                    else:
                        # Perbarui studio jika ditemukan dan sebelumnya Unknown
                        if studio != 'Unknown' and nekopoi_data[release_date][title]['studio'] == 'Unknown':
                            nekopoi_data[release_date][title]['studio'] = studio
                        nekopoi_data[release_date][title]['episodes'].append(eps_num)

                except Exception as e:
                    logging.warning(f"Error parsing entri Nekopoi: {str(e)}")
                    continue

        # Proses data untuk menggabungkan episode
        processed_data = {}
        for date, titles in nekopoi_data.items():
            processed_data[date] = []
            for title, data in titles.items():
                episodes = data['episodes']
                studio = data['studio']
                episodes.sort()
                if len(episodes) == 1:
                    eps_str = f"Episode {episodes[0]}"
                elif len(episodes) == 2:
                    eps_str = f"Episode {episodes[0]} & {episodes[1]}"
                else:
                    eps_str = f"Episode {episodes[0]} - {episodes[-1]}"

                processed_data[date].append({
                    'title': title,
                    'episodes': eps_str,
                    'studio': studio
                })

        # Dapatkan tanggal update terakhir
        last_update_tag = soup.select_one('#content > div.postsbody > div > div.contentpost > p:nth-child(14) > span > em > strong')
        last_update = "Unknown"
        if last_update_tag:
            last_update_text = last_update_tag.get_text(strip=True)
            # Ekstrak tanggal dari format seperti "[Update Terakhir 18 Agustus 2025]"
            date_match = re.search(r'(\d{1,2}\s+\w+\s+\d{4})', last_update_text)
            if date_match:
                last_update = date_match.group(1)

        # Hentikan animasi loading
        loading_active = False
        time.sleep(0.2)  # Berikan waktu thread animasi untuk selesai

        logging.info(f"\n🔍 Ditemukan entri Nekopoi untuk {len(processed_data)} tanggal")
        return processed_data, last_update

    except Exception as e:
        # Hentikan animasi loading
        loading_active = False
        time.sleep(0.2)  # Berikan waktu thread animasi untuk selesai

        logging.error(f"❌ Error scraping Nekopoi: {str(e)}")
        return {}, "Unknown"

def scrape_mal_seasonal(url):
    """Fungsi scraping utama untuk halaman musiman MyAnimeList."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    global loading_active
    try:
        # Mulai animasi loading di thread terpisah
        loading_active = True
        animation_thread = threading.Thread(target=loading_animation, args=("🔄 Mengambil halaman musiman MyAnimeList...",))
        animation_thread.daemon = True
        animation_thread.start()

        time.sleep(random.uniform(3, 7))
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        if "captcha" in response.url.lower():
            raise Exception("Diblokir oleh CAPTCHA")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        anime_data = {}

        # Definisikan selector untuk setiap kategori
        category_selectors = {
            'TV (New)': '#content > div.js-categories-seasonal > div:nth-child(1)',
            'TV (Continuing)': '#content > div.js-categories-seasonal > div:nth-child(3)',
            'ONA': '#content > div.js-categories-seasonal > div.seasonal-anime-list.js-seasonal-anime-list.js-seasonal-anime-list-key-5',
            'OVA': '#content > div.js-categories-seasonal > div.seasonal-anime-list.js-seasonal-anime-list.js-seasonal-anime-list-key-2',
            'Movie': '#content > div.js-categories-seasonal > div.seasonal-anime-list.js-seasonal-anime-list.js-seasonal-anime-list-key-3',
            'Special': '#content > div.js-categories-seasonal > div.seasonal-anime-list.js-seasonal-anime-list.js-seasonal-anime-list-key-4',
            'Unknown': '#content > div.js-categories-seasonal > div.seasonal-anime-list.js-seasonal-anime-list.js-seasonal-anime-list-key-0'
        }

        total_entries = 0
        categories = {cat: [] for cat in category_selectors}
        log_messages = []

        for cat, sel in category_selectors.items():
            container = soup.select_one(sel)
            if container:
                anime_entries = container.find_all('div', class_='js-seasonal-anime') or \
                                container.find_all('div', class_='seasonal-anime')
                log_messages.append(f"\n🔍 Ditemukan {len(anime_entries)} entri anime untuk {cat}")
                total_entries += len(anime_entries)

                for entry in anime_entries:
                    data = get_anime_data(entry)
                    if not data:
                        continue

                    data['category'] = cat

                    # Format tanggal rilis
                    try:
                        date_obj = datetime.strptime(data['date'], '%b %d, %Y')
                        formatted_date = date_obj.strftime('%d %B')  # Diperbaiki untuk kompatibilitas Windows
                        translated_date = translate_month(formatted_date)
                    except ValueError:
                        translated_date = data['date']

                    # Simpan tanggal yang diterjemahkan dalam data
                    data['translated_date'] = translated_date

                    # Gunakan tanggal asli sebagai kunci untuk parsing yang konsisten
                    key = data['date']
                    if key not in anime_data:
                        anime_data[key] = []
                    anime_data[key].append(data)

                    categories[cat].append(data)
            else:
                logging.info(f"🔍 Tidak ada entri yang ditemukan untuk {cat}")

        # Cetak pesan kategori
        for msg in log_messages:
            logging.info(msg)

        # Hentikan animasi loading
        loading_active = False
        time.sleep(0.2)  # Berikan waktu thread animasi untuk selesai

        logging.info(f"\n🔍 Total entri anime ditemukan: {total_entries}\n")

        return anime_data, categories

    except Exception as e:
        # Hentikan animasi loading
        loading_active = False
        time.sleep(0.2)  # Berikan waktu thread animasi untuk selesai

        logging.error(f"❌ Error scraping: {str(e)}")
        return {}, {}

def save_to_file(anime_data, categories, output_path, member_threshold=10000, nekopoi_data=None, nekopoi_last_update="Unknown", filter_year=2025, season_name="Unknown", year="2025"):
    """Menyimpan data anime ke dalam file."""
    # cspell:disable-next-line
    header_template = """{season} 𝙷𝚎𝚗𝚝𝚊𝚒 𝙰𝚗𝚍 𝙽𝚘𝚛𝚖𝚊𝚕 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝
           {year}

Latest Information :
Inget : Anime Hentai yg w ambil ada 2 sumber, yg pastinya syudah jelas mana yg bakal up dluan :v jdi w pisahin list nya biar gk bingung. Ohh iya di list punya ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒 jadwalnya cuma 2 bulan

Common Information for Hentai ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞 Anime list :
- Tanggal Rilis
> Judul Hentai
^ Studio
! Genre Hentai (ABSOLUTELY SECRET) Soalnya gatau genrenya :v
+ Jumlah Episode (kalo udh ada)
~ Menit per Episode (kalo udh ada)

Common Information for Hentai ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒 Anime list :
- Tanggal Rilis
> Judul Hentai
^ Studio
! Genre Hentai (ABSOLUTELY SECRET) Soalnya gatau genrenya :v
+ Episode yg bakal dirilis (Mksdnya tuh di tanggal ini eps berapa yg bakal dirilis di ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒)

Common Information for Normal Anime list :
- Tanggal Rilis
> Judul Anime
! Genre Anime
+ Jumlah Episode (kalo udh ada)
~ Menit per Episode (kalo udh ada)

Danger Anime Genre:
Adl : Adult
BL / Yao : Boys Love / Yaoi
Cro : Crossdressing
Ecc : Ecchi
Ero : Erotica
GL / Yur : Girls Love / Yuri
Hen : Hentai

Info tambahan :
Kalau di akhiran genre dipisah dan dibelakang genrenya ada tanda ! (tanda seru) + cetak tebal artinya awas ae soalnya genrenya dah aneh / nyeleweng dan biasanya genre itu masuk di "Danger Anime Genre", jdi usahakan dibaca dlu dan dipahami baek" soalnya klo ada apa" bukan salah Admin / yg share rekomendasi klo ente masih tetep nonton tu anime yg ada genre bahaya 🙂

Disclaimer :
Semua Normal Anime list dan Sebagian Hentai Anime List diambil dari ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞 dan Sebagian Hentai Anime Listmya lagi diambil dari ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒 gk smua anime yg muncul w tulis :v
Intinya w ambil yg menurut w menarik ae :v

Source : https://chat.whatsapp.com/CYXRhe5hGFcLpNuSpykqst
\n\n"""

    # Konversi nama musim ke font fancy
    season_mapping = {
        "Musim Dingin": "𝚆𝚒𝚗𝚝𝚎𝚛",
        "Semi": "𝚂𝚙𝚛𝚒𝚗𝚐",
        "Panas": "𝚂𝚞𝚖𝚖𝚎𝚛",
        "Gugur": "𝙵𝚊𝚕𝚕"
    }
    fancy_season = season_mapping.get(season_name, season_name)

    # Konversi tahun ke angka fancy
    number_mapping = {
        '0': '𝟶', '1': '𝟷', '2': '𝟸', '3': '𝟹', '4': '𝟺',
        '5': '𝟻', '6': '𝟼', '7': '𝟽', '8': '𝟾', '9': '𝟿'
    }
    fancy_year = ''.join(number_mapping.get(char, char) for char in str(year))

    # Ganti placeholder di header
    header = header_template.replace("{season}", fancy_season).replace("{year}", fancy_year)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header)

        # Tulis Daftar Hentai Nekopoi terlebih dahulu
        if nekopoi_data:
            f.write("\n" + "=" * 50 + "\n")
            f.write("*𝙷𝚎𝚗𝚝𝚊𝚒 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝 ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒*\n")
            f.write("=" * 50 + "\n")

            # Urutkan tanggal secara kronologis
            def parse_indo_date(date_str):
                """Mengurai format tanggal Indonesia seperti '27 Juni 2025' ke datetime untuk pengurutan"""
                month_map = {
                    'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4, 'Mei': 5, 'Juni': 6,
                    'Juli': 7, 'Agustus': 8, 'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
                }
                parts = date_str.split()
                if len(parts) == 3:
                    day = int(parts[0])
                    month = month_map.get(parts[1], 1)
                    year = int(parts[2])
                    return datetime(year, month, day)
                return datetime.now()  # fallback

            sorted_dates = sorted(nekopoi_data.keys(), key=parse_indo_date)

            for date in sorted_dates:
                entries = nekopoi_data[date]
                f.write(f"- *{date}*\n")
                for entry in entries:
                    f.write(f"> {entry['title']}\n")
                    f.write(f"^ {entry['studio']}\n")
                    f.write("! *Genre Hentai (ABSOLUTELY SECRET) Soalnya gatau genrenya :v*\n")
                    f.write(f"+ {entry['episodes']}\n")
                    f.write("\n")  # Tambahkan baris kosong antara entri
                f.write("\n")

            # Tambahkan catatan dan update terakhir di bawah daftar Nekopoi
            f.write("NOTE : Jadwal mungkin belum lengkap, harap tunggu update dari admin\n")
            f.write(f"Update Terakhir : {nekopoi_last_update}\n\n")

        if not anime_data:
            f.write("\nTidak ada anime yang memenuhi kriteria\n")
        else:
            filtered_anime_data = {
                date: animes for date, animes in anime_data.items()
                if date != 'Unknown' and (parsed := parse_date_flexible(date)) and parsed.year >= filter_year
            }
            sorted_dates = sorted(filtered_anime_data.items(), key=lambda x: parse_date_flexible(x[0]) or datetime.min)

            from collections import defaultdict

            erotica_anime_list = []
            hentai_anime_list = []
            normal_by_category = defaultdict(list)

            for date, animes in sorted_dates:
                for anime in animes:
                    non_danger_genres = anime['genres']

                    # Pastikan non_danger_genres diperlakukan dengan benar
                    if isinstance(non_danger_genres, str):
                        non_danger_genres = non_danger_genres.split(', ')

                    # Pisahkan menjadi genre normal dan berbahaya
                    danger_genres = [g for g in non_danger_genres if g in DANGER_GENRES]
                    safe_genres = [g for g in non_danger_genres if g not in DANGER_GENRES]

                    combined_genre_info = ', '.join(safe_genres)
                    if danger_genres:
                        combined_danger_info = ', '.join([f'*{g}*!' for g in danger_genres])
                        combined_genre_info += f', {combined_danger_info}' if combined_genre_info else combined_danger_info

                    # Kategorikan entri Hentai dan Erotika
                    if 'Hentai' in non_danger_genres or 'Erotica' in non_danger_genres:
                        if 'Erotica' in non_danger_genres:
                            erotica_anime_list.append({
                                'date': anime['translated_date'],
                                'title': anime['title'],
                                'genres': combined_genre_info,
                                'studio': anime['studio'],
                                'eps': anime['eps'],
                                'duration': anime['duration'],
                            })

                        if 'Hentai' in non_danger_genres:
                            hentai_anime_list.append({
                                'date': anime['translated_date'],
                                'title': anime['title'],
                                'genres': combined_genre_info,
                                'studio': anime['studio'],
                                'eps': anime['eps'],
                                'duration': anime['duration'],
                            })
                    else:  # Tambahkan ke daftar anime normal jika memenuhi syarat
                        if anime['members'] >= member_threshold:
                            category = anime.get('category', 'Unknown')
                            normal_by_category[category].append({
                                'date': anime['translated_date'],
                                'original_date': anime['date'],
                                'title': anime['title'],
                                'genres': combined_genre_info,
                                'studio': anime['studio'],
                                'eps': anime['eps'],
                                'duration': anime['duration'],
                                'category': category
                            })


            # Tulis Hentai MyAnimeList terlebih dahulu (setelah Nekopoi)
            if hentai_anime_list:
                f.write("\n" + "=" * 50 + "\n")
                f.write("*𝙷𝚎𝚗𝚝𝚊𝚒 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝 ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞*\n")
                f.write("=" * 50 + "\n")
                for anime in hentai_anime_list:
                    f.write(f"- *{anime['date']}*\n")
                    f.write(f"> {anime['title']}\n")
                    f.write(f"! {anime['genres']}\n")
                    f.write(f"^ {anime['studio']}\n")
                    if anime['eps'] not in {'?', '0', 'unknown', None, ''}:
                        f.write(f"+ {anime['eps']} eps\n")
                    if anime['duration'] not in {'?', '0', 'unknown', None, ''}:
                        f.write(f"~ {anime['duration']} menit / eps\n")
                    f.write("\n")

            # Tulis Anime Erotika
            if erotica_anime_list:
                f.write("\n" + "=" * 50 + "\n")
                f.write("*𝙴𝚛𝚘𝚝𝚒𝚌𝚊 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝 ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞*\n")
                f.write("=" * 50 + "\n")
                for anime in erotica_anime_list:
                    f.write(f"- *{anime['date']}*\n")
                    f.write(f"> {anime['title']}\n")
                    f.write(f"! {anime['genres']}\n")
                    f.write(f"^ {anime['studio']}\n")
                    if anime['eps'] not in {'?', '0', 'unknown', None, ''}:
                        f.write(f"+ {anime['eps']} eps\n")
                    if anime['duration'] not in {'?', '0', 'unknown', None, ''}:
                        f.write(f"~ {anime['duration']} menit / eps\n")
                    f.write("\n")

            # Tulis Anime Normal dipisah berdasarkan kategori
            category_order = ['TV (New)', 'TV (Continuing)', 'ONA', 'OVA', 'Movie', 'Special', 'Unknown']
            f.write("\n" + "=" * 50 + "\n")
            f.write("*𝙽𝚘𝚛𝚖𝚊𝚕 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝*\n")
            f.write("=" * 50 + "\n")
            for cat in category_order:
                f.write(f"\n- *{cat}:*\n")
                if cat in normal_by_category and normal_by_category[cat]:
                    from collections import defaultdict
                    group_dict = defaultdict(list)
                    groups = []
                    for anime in normal_by_category[cat]:
                        date_str = anime['original_date']
                        try:
                            dt = datetime.strptime(date_str, '%b %d, %Y')
                            group = f"{dt.day} {translate_month(dt.strftime('%B'))} {dt.year}"
                        except ValueError:
                            try:
                                dt = datetime.strptime(date_str, '%b %Y')
                                group = f"Tanggal Rilis Tidak Diketahui {translate_month(dt.strftime('%B'))} {dt.year}"
                            except ValueError:
                                dt = datetime.min
                                group = translate_month(date_str)
                        if group not in [g[0] for g in groups]:
                            groups.append((group, dt))
                        group_dict[group].append(anime)

                    groups.sort(key=lambda x: x[1])
                    for group, _ in groups:
                        f.write(f"- *{group}*\n")
                        for anime in group_dict[group]:
                            f.write(f"> {anime['title']}\n")
                            f.write(f"! {anime['genres']}\n")
                            f.write(f"^ {anime['studio']}\n")
                            if anime['eps'] not in {'?', '0', 'unknown', None, ''}:
                                f.write(f"+ {anime['eps']} eps\n")
                            if anime['duration'] not in {'?', '0', 'unknown', None, ''}:
                                f.write(f"~ {anime['duration']} menit / eps\n")
                            f.write("\n")
                else:
                    f.write("_*TIDAK ADA*_\n\n")

def main():
    """Fungsi utama."""
    logging.info("="*65)
    logging.info("               MyAnimeList dan NekoPoi SCRAPPER")
    logging.info("                VERSI 11 BETA - TheKingTermux")
    logging.info("="*65)
    logging.info(" Script ini akan mengambil data anime seasonal dari MyAnimeList")
    logging.info(" Normal maupun Hentai dan akan mengambil data anime Hentai dari")
    logging.info("  NekoPoi dan menyimpannya dalam format yang telah ditentukan.\n")
    
    # Musim yang tersedia
    seasons = {
        1: "Musim Dingin",
        2: "Semi",
        3: "Panas",
        4: "Gugur"
    }

    # Minta input tahun
    year = input("Masukkan tahun (contoh: 2025): \n")

    # Tampilkan opsi musim
    print("\nPilih musim:")
    for key, value in seasons.items():
        print(f"{key}. {value}")

    # Minta input musim
    season_choice = input("Silakan pilih musim (1-4): \n")

    # Validasi input pengguna
    while not season_choice.isdigit() or int(season_choice) not in seasons:
        print("Input tidak valid. Silakan pilih musim yang valid (1-4).")
        season_choice = input("Silakan pilih musim (1-4): \n")

    custom_name = input("\nMasukkan nama file output (kosongkan untuk default 'AnimeList.txt'): \n").strip()

    # Minta ambang batas anggota
    member_threshold_input = input("\nMasukkan ambang batas anggota (default 10000): \n").strip()
    if not member_threshold_input:
        member_threshold = 10000
    else:
        member_threshold = int(member_threshold_input)

    # Dapatkan musim yang dipilih
    selected_season = seasons[int(season_choice)]

    # Petakan musim Indonesia ke bahasa Inggris untuk URL
    season_url_map = {
        "Musim Dingin": "winter",
        "Semi": "spring",
        "Panas": "summer",
        "Gugur": "fall"
    }
    url_season = season_url_map.get(selected_season, selected_season)

    # Konstruksi URL berdasarkan input pengguna
    url = f"https://myanimelist.net/anime/season/{year}/{url_season}"

    # Sekarang scrape data menggunakan URL yang dibuat secara dinamis
    anime_data, categories = scrape_mal_seasonal(url)

    # Scrape data Nekopoi
    nekopoi_data, nekopoi_last_update = scrape_nekopoi()

    # Simpan ke file
    if not custom_name:
        custom_name = "AnimeList.txt"
    else:
        if not custom_name.lower().endswith(".txt"):
            custom_name += ".txt"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "AnimeList")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, custom_name)

    save_to_file(anime_data, categories, output_path, member_threshold, nekopoi_data, nekopoi_last_update, int(year), selected_season, year)
    
    logging.info("="*50)
    if anime_data or nekopoi_data:
        mal_total = sum(len(v) for v in anime_data.values()) if anime_data else 0
        nekopoi_total = sum(len(v) for v in nekopoi_data.values()) if nekopoi_data else 0
        total = mal_total + nekopoi_total
        logging.info(f"✅  Berhasil menyimpan {total} anime ke: {output_path}")
        if mal_total > 0:
            logging.info(f"   - MyAnimeList: {mal_total} entri")
        if nekopoi_total > 0:
            logging.info(f"   - Nekopoi    : {nekopoi_total} entri")
    else:
        logging.error("❌ Gagal mengumpulkan data anime dari kedua sumber")

        # Alasan error MyAnimeList
        logging.error("Alasan mungkin MyAnimeList:")
        mal_reasons = [
            "Situs MyAnimeList sedang down",
            "Diblokir oleh langkah anti-scraping",
            "Struktur HTML telah berubah",
            "Tidak ada anime dengan lebih dari 10.000 anggota"
        ]
        for reason in mal_reasons:
            logging.error(f"- {reason}")

        # Alasan error Nekopoi
        logging.error("Alasan mungkin Nekopoi:")
        nekopoi_reasons = [
            "Situs Nekopoi sedang down",
            "Diblokir oleh langkah anti-scraping",
            "Struktur HTML telah berubah",
            "Tidak ada hentai yang dijadwalkan untuk periode saat ini"
        ]
        for reason in nekopoi_reasons:
            logging.error(f"- {reason}")

        logging.error("Saran: Periksa koneksi internet Anda dan coba lagi nanti.")
    logging.info("="*50)

if __name__ == "__main__":
    main()
