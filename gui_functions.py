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

# Configure logging to not interfere with animation
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Global flag for loading animation
loading_active = False

# Global data usage tracking
data_usage = 0
session_data_usage = 0

def loading_animation(message="🔄 Processing..."):
    """Display loading animation with spinner on its own line"""
    spinner = ['|', '/', '-', '\\']
    i = 0
    while loading_active:
        sys.stdout.write(f'\r{message} {spinner[i % len(spinner)]}')
        sys.stdout.flush()
        time.sleep(0.15)
        i += 1
    sys.stdout.write(f'\r{message} completed ✓\n')
    sys.stdout.flush()

# Dangerous genres
DANGER_GENRES = {"Adult", "Boys Love", "Yaoi", "Crossdressing", "Ecchi", "Girls Love", "Yuri", "Hentai", "Erotica"}

# Regular expressions
EPS_REGEX = re.compile(r'(\d+)(?:\s*eps)?')
DURATION_REGEX = re.compile(r'(\d+)\s*min')

def translate_month(date_str):
    """Translates month names from English to Indonesian."""
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
    for eng, indo in sorted(month_translation.items(), key=lambda x: len(x[0]), reverse=True):
        date_str = re.sub(r'\b' + re.escape(eng) + r'\b', indo, date_str)
    return date_str

def parse_date_flexible(date_str):
    """Parse date string with flexible format."""
    if date_str == 'Unknown':
        return None
    try:
        return datetime.strptime(date_str, '%b %d, %Y')
    except ValueError:
        try:
            partial = datetime.strptime(date_str, '%b %Y')
            return partial.replace(day=1)
        except ValueError:
            return None

def parse_member_count(members_text):
    """Convert member count text (like '10K') to integer."""
    members_text = members_text.upper().replace(',', '').strip()
    if 'K' in members_text:
        return int(float(members_text.replace('K', '')) * 1000)
    elif 'M' in members_text:
        return int(float(members_text.replace('M', '')) * 1000000)
    else:
        return int(re.sub(r'[^0-9]', '', members_text))

def get_anime_data(entry):
    """Extract data from one anime entry."""
    try:
        title_tag = entry.select_one('div.title > div > h2 > a')
        title = title_tag.get_text(strip=True) if title_tag else 'Unknown'

        members_tag = entry.select_one('div.information > div.information-item.scormem > div > div.scormem-item.member')
        members_text = members_tag.get_text(strip=True) if members_tag else '0'
        members = parse_member_count(members_text)

        date_tag = entry.select_one('div.prodsrc > div.info > span:nth-child(1)')
        date_text = date_tag.get_text(strip=True) if date_tag else 'Unknown'

        eps_dur_tag = entry.select_one('div.prodsrc > div.info > span:nth-child(2)')
        eps_dur_text = eps_dur_tag.get_text(strip=True) if eps_dur_tag else ''

        eps_count = EPS_REGEX.search(eps_dur_text)
        duration_min = DURATION_REGEX.search(eps_dur_text)
        eps_count = eps_count.group(1) if eps_count else ''
        duration_min = duration_min.group(1) if duration_min else ''

        studio_tag = entry.select_one('div.synopsis.js-synopsis > div > div:nth-child(1) > span.item > a')
        studio = studio_tag.get_text(strip=True) if studio_tag else 'Unknown'

        if studio in {'?', '0', 'unknown', '', None}:
            studio = 'Unknown'

        genres = []
        genre_container = entry.select_one('div.genres-inner')
        if genre_container:
            genres = [genre.get_text(strip=True) for genre in genre_container.find_all('span')]

        themes = [theme.get_text(strip=True) for theme in entry.select('div.properties > div:nth-child(3) > span.item')]

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
            'category': None
        }

    except Exception as e:
        logging.error(f"Error processing entry: {str(e)}")
        return None

def scrape_nekopoi(max_retries=3, use_proxy=False, proxy_list=None):
    """Mengambil jadwal hentai dari Nekopoi.care dengan retry dan proxy support"""
    global loading_active, data_usage, session_data_usage
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    for attempt in range(max_retries):
        try:
            # Menggunakan waktu continuous yang sama dari MAL scraping
            print_status(continuous=True)
            # Mulai animasi loading di thread terpisah
            loading_active = True
            animation_thread = threading.Thread(target=loading_animation, args=("🔄 Mengambil jadwal hentai Nekopoi...",))
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

            response = requests.get("https://nekopoi.care/jadwal-new-hentai/", headers=headers, timeout=15, proxies=proxies)
            response.raise_for_status()
            data_usage += len(response.content)
            session_data_usage += len(response.content)

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
            last_update_tag = soup.select_one('#content > div.postsbody > div > div.contentpost > p > span > em > strong')
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
            animation_thread.join()

            logging.info(f"\n🔍 Ditemukan entri Nekopoi untuk {len(processed_data)} tanggal")
            return processed_data, last_update

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
                return {}, "Unknown"

def scrape_mal_seasonal(url, max_retries=3, use_proxy=False, proxy_list=None):
    """Main scraping function for MyAnimeList seasonal page with retry and proxy support."""
    global loading_active, data_usage, session_data_usage
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    for attempt in range(max_retries):
        animation_thread = None
        try:
            loading_active = True
            animation_thread = threading.Thread(target=loading_animation, args=("🔄 Mengambil halaman musiman MyAnimeList...",))
            animation_thread.daemon = True
            animation_thread.start()

            time.sleep(random.uniform(3, 7))

            proxies = None
            if use_proxy and proxy_list:
                proxy = random.choice(proxy_list)
                proxies = {
                    'http': proxy,
                    'https': proxy
                }

            response = requests.get(url, headers=headers, timeout=15, proxies=proxies)
            response.raise_for_status()

            if "captcha" in response.url.lower():
                raise Exception("Blocked by CAPTCHA")

            soup = BeautifulSoup(response.text, 'html.parser')
            anime_data = {}

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
                    log_messages.append(f"\n🔍 Found {len(anime_entries)} anime entries for {cat}")
                    total_entries += len(anime_entries)

                    for entry in anime_entries:
                        data = get_anime_data(entry)
                        if not data:
                            continue

                        data['category'] = cat

                        try:
                            date_obj = datetime.strptime(data['date'], '%b %d, %Y')
                            formatted_date = date_obj.strftime('%d %B')
                            translated_date = translate_month(formatted_date)
                        except ValueError:
                            translated_date = data['date']

                        data['translated_date'] = translated_date

                        key = data['date']
                        if key not in anime_data:
                            anime_data[key] = []
                        anime_data[key].append(data)

                        categories[cat].append(data)
                else:
                    logging.info(f"🔍 No entries found for {cat}")

            for msg in log_messages:
                logging.info(msg)

            loading_active = False
            time.sleep(0.2)
            if animation_thread:
                animation_thread.join()

            logging.info(f"\n🔍 Total anime entries found: {total_entries}\n")

            return anime_data, categories

        except Exception as e:
            loading_active = False
            time.sleep(0.2)
            if animation_thread:
                animation_thread.join()

            if attempt < max_retries - 1:
                logging.warning(f"❌ Attempt {attempt + 1} failed: {str(e)}. Retrying...")
                time.sleep(2 ** attempt)
            else:
                logging.error(f"❌ All {max_retries} attempts failed. Last error: {str(e)}")
                return {}, {}

def save_to_file(anime_data, categories, output_path, member_threshold=10000, nekopoi_data=None, nekopoi_last_update="Unknown", filter_year=2025, season_name="Unknown", year="2025", header_template=None):
    """Save anime data to file."""

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

    # Hitung info Nekopoi (sama seperti yang kamu kasih)
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
            last_month_english = datetime(last_ym[0], last_ym[1], 1).strftime('%B')
            last_month = translate_month(last_month_english)
        if month_has_passed >= 0:
            schedule_info = f"(dengan {month_has_passed} bulan telah berlalu, dan bulan terakhir adalah {last_month})"
        else:
            schedule_info = f"(dan bulan terakhir adalah {last_month})"
    else:
        nekopoi_month = 0
        schedule_info = "(tidak ada data Nekopoi)"

    # Header template baru (khusus bagian Nekopoi sesuai permintaanmu)
    if header_template is None:
        header_template = """{season} 𝙷𝚎𝚗𝚝𝚊𝚒 𝙰𝚗𝚍 𝙽𝚘𝚛𝚖𝚊𝚕 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝
{year}
𝙼𝚎𝚖𝚋𝚎𝚛 : {member}

Latest Information :
Inget : Anime Hentai yg w ambil ada 2 sumber, yg pastinya syudah jelas mana yg bakal up dluan :v jdi w pisahin list nya biar gk bingung. 
Ohh iya di list punya ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒 jadwalnya cuma {nekopoi_month} bulan {schedule_info}

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

    # Convert season name to fancy font
    season_mapping = {
        "Musim Dingin": "𝚆𝚒𝚗𝚝𝚎𝚛",
        "Semi": "𝚂𝚙𝚛𝚒𝚗𝚐",
        "Panas": "𝚂𝚞𝚖𝚖𝚎𝚛",
        "Gugur": "𝙵𝚊𝚕𝚕"
    }
    fancy_season = season_mapping.get(season_name, season_name)

    # Convert year to fancy numbers
    number_mapping = {
        '0': '𝟶', '1': '𝟷', '2': '𝟸', '3': '𝟹', '4': '𝟺',
        '5': '𝟻', '6': '𝟼', '7': '𝟽', '8': '𝟾', '9': '𝟿'
    }
    fancy_year = ''.join(number_mapping.get(char, char) for char in str(year))

    # Convert member threshold to fancy numbers
    fancy_member = ''.join(number_mapping.get(char, char) for char in str(member_threshold))

# Replace semua placeholder yang ada
    fancy_season = season_mapping.get(season_name, season_name)
    fancy_year = ''.join(number_mapping.get(c, c) for c in str(year))
    fancy_member = ''.join(number_mapping.get(c, c) for c in str(member_threshold))

    header = header_template.format(
        season=fancy_season,
        year=fancy_year,
        member=fancy_member,
        nekopoi_month=nekopoi_month,
        schedule_info=schedule_info
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header)

        # Write Nekopoi Hentai list first
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

                    # Ensure non_danger_genres is handled correctly
                    if isinstance(non_danger_genres, str):
                        non_danger_genres = non_danger_genres.split(', ')

                    # Separate into normal and dangerous genres
                    danger_genres = [g for g in non_danger_genres if g in DANGER_GENRES]
                    safe_genres = [g for g in non_danger_genres if g not in DANGER_GENRES]

                    combined_genre_info = ', '.join(safe_genres)
                    if danger_genres:
                        combined_danger_info = ', '.join([f'*{g}*!' for g in danger_genres])
                        combined_genre_info += f', {combined_danger_info}' if combined_genre_info else combined_danger_info

                    # Categorize Hentai and Erotica entries
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
                    else:  # Add to normal anime list if qualifies
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


            # Write MyAnimeList Hentai first (after Nekopoi)
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

            # Write Erotica Anime
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

            # Write Normal Anime separated by category
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
    """Display program header"""
    logging.info("="*65)
    logging.info("               MyAnimeList dan NekoPoi SCRAPPER")
    logging.info("                   VERSI 14 - TheKingTermux")
    logging.info("="*65)
    logging.info(" Script ini akan mengambil data anime seasonal dari MyAnimeList")
    logging.info(" Normal maupun Hentai dan akan mengambil data anime Hentai dari")
    logging.info("  NekoPoi dan menyimpannya dalam format yang telah ditentukan.\n")

def print_status(scraping_start_time=None, continuous=False):
    """Print scrapping time, data usage, and current time."""
    # Simplified version for GUI
    pass