from bs4 import BeautifulSoup
import cloudscraper
from datetime import datetime
import logging
import os
import random
import re
import requests
import sys
import threading
import time

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
    # Urutkan berdasarkan panjang menurun dan ganti seluruh kata saja
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
            # Untuk tanggal parsial seperti 'Des 2025'
            partial = datetime.strptime(date_str, '%b %Y')
            # Asumsikan hari ke-1 untuk penyortiran
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
            'category': None  # Inisialisasi tanpa kategori
        }
    
    except Exception as e:
        logging.error(f"Error memproses entri: {str(e)}")
        return None
    
def user_agent():
    """Menghasilkan User-Agent acak untuk menghindari blokir."""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 YaBrowser/25.12.3.1141 Yowser/2.5 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 YaBrowser/25.12.3.1141 Yowser/2.5 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 18_7_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 YaBrowser/26.3.1.592 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; arm_64; Android 16; SM-G965F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.7632.121 YaBrowser/25.12.8.44 Mobile Safari/537.36'
    ]
    return random.choice(user_agents)

def scrape_nekopoi():
    """Mengambil jadwal hentai dari Nekopoi.care"""
    global loading_active, data_usage, session_data_usage
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://nekopoi.care/',
    }

    try:
        print_status(continuous=True)
        loading_active = True
        animation_thread = threading.Thread(target=loading_animation, args=("🔄 Mengambil jadwal hentai Nekopoi...",))
        animation_thread.daemon = True
        animation_thread.start()

        # Buat scraper khusus untuk Nekopoi saja
        scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
        )

        response = scraper.get(
            "https://nekopoi.care/jadwal-new-hentai/", 
            headers=headers, 
            timeout=60
        )
        
        response.raise_for_status()
        data_usage += len(response.content)
        session_data_usage += len(response.content)

        soup = BeautifulSoup(response.text, 'html.parser')

        nekopoi_data = {}
        spoiler_bodies = soup.find_all('div', class_='spoiler-body')

        for spoiler_body in spoiler_bodies:
            entries = spoiler_body.find_all('div', class_='coming_soon')

            for entry in entries:
                try:
                    title_tag = entry.select_one('h2 a.title')
                    title = title_tag.get_text(strip=True) if title_tag else None
                    if not title: 
                        continue

                    eps_tag = entry.select_one('span.episode')
                    eps_text = eps_tag.get_text(strip=True) if eps_tag else ''
                    eps_match = re.search(r'Episode?\s*(\d+)', eps_text, re.I)
                    eps_num = int(eps_match.group(1)) if eps_match else 1

                    date_tag = entry.select_one('span.release_date')
                    release_date = date_tag.get_text(strip=True) if date_tag else None
                    if not release_date: 
                        continue

                    studio = 'Unknown'
                    studio_tag = entry.select_one('span[style*="b679f2"]')
                    if studio_tag:
                        studio = studio_tag.get_text(strip=True)

                    if release_date not in nekopoi_data:
                        nekopoi_data[release_date] = {}
                    
                    if title not in nekopoi_data[release_date]:
                        nekopoi_data[release_date][title] = {'episodes': [eps_num], 'studio': studio}
                    else:
                        if studio != 'Unknown':
                            nekopoi_data[release_date][title]['studio'] = studio
                        nekopoi_data[release_date][title]['episodes'].append(eps_num)

                except:
                    continue

        # Proses data
        processed_data = {}
        for date, titles in nekopoi_data.items():
            processed_data[date] = []
            for title, data in titles.items():
                eps = sorted(data['episodes'])
                eps_str = f"Episode {eps[0]}" if len(eps) == 1 else f"Episode {eps[0]} - {eps[-1]}"
                processed_data[date].append({
                    'title': title,
                    'episodes': eps_str,
                    'studio': data['studio']
                })

        # Last Update
        last_update = "Unknown"
        update_tag = soup.find(string=re.compile(r'Update Terakhir', re.I))
        if update_tag:
            match = re.search(r'Update Terakhir[:\s]*(\d{1,2}\s+\w+\s+\d{4})', str(update_tag))
            if match:
                last_update = match.group(1)

        loading_active = False
        time.sleep(0.3)
        if 'animation_thread' in locals():
            animation_thread.join()

        logging.info(f"✅ Nekopoi: {sum(len(v) for v in processed_data.values())} jadwal berhasil diambil")
        return processed_data, last_update

    except Exception as e:
        loading_active = False
        if 'animation_thread' in locals():
            animation_thread.join()
        logging.error(f"❌ Error scraping Nekopoi: {str(e)}")
        return {}, "Unknown"

def print_status(scraping_start_time=None, continuous=False):
    """Print scrapping time, data usage, and current time."""
    global start_time, data_usage, session_data_usage, continuous_scraping_start
    if continuous and hasattr(print_status, 'continuous_start'):
        elapsed = time.time() - print_status.continuous_start
    elif scraping_start_time:
        elapsed = time.time() - scraping_start_time
    else:
        elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    time_str = f"{minutes:02d}:{seconds:02d}"
    session_kb = session_data_usage // 1024
    total_kb = data_usage // 1024
    if session_kb >= 1024:
        session_mb = session_kb / 1024
        session_str = f"{session_mb:.2f} MB"
    else:
        session_str = f"{session_kb} KB"
    if total_kb >= 1024:
        total_mb = total_kb / 1024
        total_str = f"{total_mb:.2f} MB"
    else:
        total_str = f"{total_kb} KB"
    print(f"Scrapping time {time_str} Data Usage : {session_str} Total Data Usage : {total_str}")

def scrape_mal_seasonal(url, max_retries=3, use_proxy=False, proxy_list=None):
    """Fungsi scraping utama untuk halaman musiman MyAnimeList dengan retry dan proxy support."""
    global loading_active, data_usage, session_data_usage
    headers = {
        'User-Agent': user_agent(),
        'Accept-Language': 'en-US,en;q=0.9',
    }

    for attempt in range(max_retries):
        try:
            scraping_start_time = time.time()
            if not hasattr(print_status, 'continuous_start'):
                print_status.continuous_start = scraping_start_time
            print_status(scraping_start_time, continuous=True)
            # Mulai animasi loading di thread terpisah
            loading_active = True
            animation_thread = threading.Thread(target=loading_animation, args=("🔄 Mengambil halaman musiman MyAnimeList...",))
            animation_thread.daemon = True
            animation_thread.start()

            time.sleep(random.uniform(3, 7))

            # Setup proxy if enabled
            proxies = None
            if use_proxy and proxy_list:
                proxy = random.choice(proxy_list)
                proxies = {
                    'http': proxy,
                    'https': proxy
                }

            response = requests.get(url, headers=headers, timeout=15, proxies=proxies)
            response.raise_for_status()
            data_usage += len(response.content)
            session_data_usage += len(response.content)

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
                
            hentai_count = 0
            erotica_count = 0
            for date, animes in anime_data.items():
                for anime in animes:
                    genres = anime.get('genres', [])
                    if 'Hentai' in genres:
                        hentai_count += 1
                    if 'Erotica' in genres:
                        erotica_count += 1

            print(f"\n🔍 Ditemukan {hentai_count} entri anime untuk Hentai")
            print(f"\n🔍 Ditemukan {erotica_count} entri anime untuk Erotica\n")

            # Hentikan animasi loading
            loading_active = False
            time.sleep(0.2)  # Berikan waktu thread animasi untuk selesai
            animation_thread.join()

            logging.info(f"\n🔍 Total entri anime ditemukan: {total_entries}\n")

            return anime_data, categories

        except Exception as e:
            # Hentikan animasi loading
            loading_active = False
            time.sleep(0.2)  # Berikan waktu thread animasi untuk selesai
            animation_thread.join()

            if attempt < max_retries - 1:
                logging.warning(f"❌ Attempt {attempt + 1} failed: {str(e)}. Retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logging.error(f"❌ All {max_retries} attempts failed. Last error: {str(e)}")
                return {}, {}

def save_to_file(anime_data, categories, output_path, member_threshold=10000, nekopoi_data=None, nekopoi_last_update="Unknown", filter_year=2025, season_name="Unknown", year="2025"):
    """Menyimpan data anime ke dalam file."""

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

    # Hitung jumlah bulan nekopoi dari data yang di-scrape
    if nekopoi_data:
        unique_months = set()
        for date in nekopoi_data.keys():
            dt = parse_indo_date(date)
            unique_months.add((dt.year, dt.month))
        if unique_months:
            first_ym = min(unique_months)
            last_ym = max(unique_months)
            current = datetime.now()
            current_ym = (current.year, current.month)
            def months_diff(ym1, ym2):
                y1, m1 = ym1
                y2, m2 = ym2
                return (y2 - y1) * 12 + (m2 - m1)
            nekopoi_month = months_diff(first_ym, last_ym) + 1
            month_has_passed = months_diff(first_ym, current_ym)
            # Dapatkan nama bulan terakhir dalam bahasa Indonesia
            last_month_english = datetime(last_ym[0], last_ym[1], 1).strftime('%B')
            last_month = translate_month(last_month_english)  # Menggunakan fungsi translate_month yang ada
            # Tentukan teks jadwal berdasarkan apakah month_has_passed masuk akal
            if month_has_passed >= 0:
                schedule_info = f"(dengan {month_has_passed} bulan telah berlalu, dan bulan terakhir adalah {last_month})"
            else:
                schedule_info = f"(dan bulan terakhir adalah {last_month})"
        else:
            nekopoi_month = 0
            month_has_passed = 0
            last_month = "Tidak diketahui"
            schedule_info = f"(dan bulan terakhir adalah {last_month})"
    else:
        nekopoi_month = 0
        month_has_passed = 0
        last_month = "Tidak diketahui"
        schedule_info = f"(dan bulan terakhir adalah {last_month})"

    # cspell:disable-next-line
    header_template = """{season} 𝙷𝚎𝚗𝚝𝚊𝚒 𝙰𝚗𝚍 𝙽𝚘𝚛𝚖𝚊𝚕 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝
            {year}
𝙼𝚎𝚖𝚋𝚎𝚛 : {member}

Latest Information :
Inget : Anime Hentai yg w ambil ada 2 sumber, yg pastinya syudah jelas mana yg bakal up dluan :v jdi w pisahin list nya biar gk bingung. Ohh iya di list punya ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒 jadwalnya cuma {nekopoi_month} bulan {schedule_info}

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

Tools  : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
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

    # Konversi member threshold ke angka fancy
    fancy_member = ''.join(number_mapping.get(char, char) for char in str(member_threshold))

    # Ganti placeholder di header
    header = header_template.replace("{season}", fancy_season).replace("{year}", fancy_year).replace("{member}", fancy_member).replace("{nekopoi_month}", str(nekopoi_month)).replace("{schedule_info}", schedule_info)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header)

        # Tulis Daftar Hentai Nekopoi terlebih dahulu
        if nekopoi_data:
            f.write("\n" + "=" * 50 + "\n")
            f.write("*𝙷𝚎𝚗𝚝𝚊𝚒 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝 ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒*\n")
            f.write("=" * 50 + "\n")

            # Urutkan tanggal secara kronologis
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
                f.write(f"- *{cat}:*\n")
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

def tampilkan_header():
    """Menampilkan header program"""
    logging.info("="*65)
    logging.info("               MyAnimeList dan NekoPoi SCRAPPER")
    logging.info("                   VERSI 15 - TheKingTermux")
    logging.info("="*65)
    logging.info(" Script ini akan mengambil data anime seasonal dari MyAnimeList")
    logging.info(" Normal maupun Hentai dan akan mengambil data anime Hentai dari")
    logging.info("  NekoPoi dan menyimpannya dalam format yang telah ditentukan.\n")

def main():
    """Fungsi utama."""
    global start_time, data_usage, session_data_usage
    start_time = time.time()
    session_data_usage = 0
    try:
        with open('data_usage.txt', 'r') as f:
            data_usage = int(f.read().strip())
    except FileNotFoundError:
        data_usage = 0

    # Musim yang tersedia
    seasons = {
        1: "Musim Dingin",
        2: "Semi",
        3: "Panas",
        4: "Gugur",
        5: "Ganti tahun yang dipilih"
    }

    # Minta input tahun dengan validasi
    while True:
        tampilkan_header()  # Panggil fungsi header di sini

        year = input("Masukkan tahun (contoh: 2025): \n").strip()
        if not year or not year.isdigit():
            print("⚠️  Warning: Tahun harus berupa angka yang valid dan tidak boleh kosong.\n")
            for i in range(3, 0, -1):
                print(f"Silahkan coba lagi dalam {i}...", end='\r')
                time.sleep(1)
            print()  # Baris baru setelah hitungan mundur
            os.system('cls')
            continue  # Langsung kembali ke awal loop, header akan ditampilkan lagi
        year_int = int(year)
        if year_int < 1917:
            print("⚠️  Warning: Tahun harus 1917 atau lebih baru.")
            for i in range(3, 0, -1):
                print(f"Silahkan coba lagi dalam {i}...", end='\r')
                time.sleep(1)
            print()  # Baris baru setelah hitungan mundur
            os.system('cls')
            continue  # Langsung kembali ke awal loop, header akan ditampilkan lagi
        current_year = datetime.now().year
        if year_int > current_year + 1:
            print("⚠️  Warning: Data MAL gak segitu kedepannya tau bro, lu dari masa depan emang?\n")
            for i in range(3, 0, -1):
                print(f"Silahkan coba lagi dalam {i}...", end='\r')
                time.sleep(1)
            print()  # Baris baru setelah hitungan mundur
            os.system('cls')
            continue  # Langsung kembali ke awal loop, header akan ditampilkan lagi

        # Minta input musim dengan validasi
        season_valid = False
        while True:
            print(f"\nTahun yang dipilih: {year}")
            print("\nPilih musim:")
            for key, value in seasons.items():
                print(f"{key}. {value}")

            season_choice = input("Silakan pilih musim (1-5): \n")
            if season_choice == '5':
                print("⚠️  Warning: Kembali ke tahun\n")
                for i in range(3, 0, -1):
                    print(f"Kembali ke pemilihan tahun dalam {i}...", end='\r')
                    time.sleep(1)
                print()
                year = None  # Atur ulang tahun untuk memilih ulang
                os.system('cls')
                break
            elif season_choice.isdigit() and int(season_choice) in [1,2,3,4]:
                season_valid = True
                break
            print("⚠️  Warning: Input tidak valid. Silakan memilih pilihan yang valid (1-5).\n")
            for i in range(3, 0, -1):
                print(f"Silahkan coba lagi dalam {i}...", end='\r')
                time.sleep(1)
            print()
            os.system('cls')
            tampilkan_header()
            # Lanjut ke awal loop, akan tampilkan tahun dan opsi musim lagi

        if season_valid:
            break

    # Minta ambang batas anggota
    member_threshold_input = input("\nMasukkan ambang batas anggota (kosongkan untuk default 10000 atau 10K, contoh: 5 untuk 5000): \n").strip()
    if not member_threshold_input:
        member_threshold = 10000
    else:
        member_threshold_input = member_threshold_input.upper().replace(',', '').strip()
        if 'K' in member_threshold_input:
            member_threshold = int(float(member_threshold_input.replace('K', '')) * 1000)
        elif 'M' in member_threshold_input:
            member_threshold = int(float(member_threshold_input.replace('M', '')) * 1000000)
        else:
            # Asumsikan K jika tidak ada sufiks
            member_threshold = int(float(member_threshold_input) * 1000)

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

    # Hitung nama default
    selected_season_english = season_url_map.get(selected_season, selected_season).capitalize()
    default_name = f"{selected_season_english}{year}.txt"
    if member_threshold != 10000:
        threshold_str = f"{member_threshold // 1000}K" if member_threshold % 1000 == 0 else str(member_threshold)
        default_name = default_name.replace('.txt', f'Member{threshold_str}.txt')

    custom_name = input(f"\nMasukkan nama file output (kosongkan untuk default '{default_name}'): \n").strip()

    # Konstruksi URL berdasarkan input pengguna
    url = f"https://myanimelist.net/anime/season/{year}/{url_season}"

    # Sekarang scrape data menggunakan URL yang dibuat secara dinamis
    anime_data, categories = scrape_mal_seasonal(url)

    # Scrape data Nekopoi (lanjutkan waktu dari MAL scraping)
    nekopoi_data, nekopoi_last_update = scrape_nekopoi()

    # Simpan ke file
    if not custom_name:
        selected_season_english = season_url_map.get(selected_season, selected_season).capitalize()
        custom_name = f"{selected_season_english}{year}.txt"
        if member_threshold != 10000:
            threshold_str = f"{member_threshold // 1000}K" if member_threshold % 1000 == 0 else str(member_threshold)
            custom_name = custom_name.replace('.txt', f'Member{threshold_str}.txt')
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
    print_status()
    with open('data_usage.txt', 'w') as f:
        f.write(str(data_usage))

if __name__ == "__main__":
    main()