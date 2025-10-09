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

def loading_animation(message="🔄 Processing..."):
    """Displays a loading animation with spinner on its own line"""
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
# cspell:disable-next-line
DANGER_GENRES = {"Adult", "Boys Love", "Yaoi", "Crossdressing", "Ecchi", "Girls Love", "Yuri", "Hentai", "Erotica"}

# Regular expressions
EPS_REGEX = re.compile(r'(\d+)(?:\s*eps)?')
DURATION_REGEX = re.compile(r'(\d+)\s*min')

def translate_month(date_str):
    """Translates month names from English to English (identity function for English version)."""
    # cspell:disable-next-line
    month_translation = {
        'January': 'January', 'February': 'February', 'March': 'March',
        'April': 'April', 'May': 'May', 'June': 'June',
        'July': 'July', 'August': 'August', 'September': 'September',
        'October': 'October', 'November': 'November', 'December': 'December',
        'Jan': 'January', 'Feb': 'February', 'Mar': 'March',
        'Apr': 'April', 'May': 'May', 'Jun': 'June',
        'Jul': 'July', 'Aug': 'August', 'Sep': 'September',
        'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
    }
    # Sort by descending length and replace whole words only
    for eng, eng in sorted(month_translation.items(), key=lambda x: len(x[0]), reverse=True):
        date_str = re.sub(r'\b' + re.escape(eng) + r'\b', eng, date_str)
    return date_str

def parse_date_flexible(date_str):
    """Parses date string with flexible format."""
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
    """Converts member count text (like '10K') to integer."""
    members_text = members_text.upper().replace(',', '').strip()
    if 'K' in members_text:
        return int(float(members_text.replace('K', '')) * 1000)
    elif 'M' in members_text:
        return int(float(members_text.replace('M', '')) * 1000000)
    else:
        return int(re.sub(r'[^0-9]', '', members_text))

def get_anime_data(entry):
    """Extracts data from one anime entry."""
    try:
        # Anime title
        title_tag = entry.select_one('div.title > div > h2 > a')
        title = title_tag.get_text(strip=True) if title_tag else 'Unknown'

        # Member count
        members_tag = entry.select_one('div.information > div.information-item.scormem > div > div.scormem-item.member')
        members_text = members_tag.get_text(strip=True) if members_tag else '0'
        members = parse_member_count(members_text)

        # Release date
        date_tag = entry.select_one('div.prodsrc > div.info > span:nth-child(1)')
        date_text = date_tag.get_text(strip=True) if date_tag else 'Unknown'

        # Episodes and duration
        eps_dur_tag = entry.select_one('div.prodsrc > div.info > span:nth-child(2)')
        eps_dur_text = eps_dur_tag.get_text(strip=True) if eps_dur_tag else ''

        # Extract episode count and duration
        eps_count = EPS_REGEX.search(eps_dur_text)
        duration_min = DURATION_REGEX.search(eps_dur_text)
        eps_count = eps_count.group(1) if eps_count else ''
        duration_min = duration_min.group(1) if duration_min else ''

        # Studio
        studio_tag = entry.select_one('div.synopsis.js-synopsis > div > div:nth-child(1) > span.item > a')
        studio = studio_tag.get_text(strip=True) if studio_tag else 'Unknown'

        # Handle invalid studio cases
        if studio in {'?', '0', 'unknown', '', None}:
            studio = 'Unknown'

        # Genres
        genres = []
        genre_container = entry.select_one('div.genres-inner')
        if genre_container:
            genres = [genre.get_text(strip=True) for genre in genre_container.find_all('span')]

        # Themes
        themes = [theme.get_text(strip=True) for theme in entry.select('div.properties > div:nth-child(3) > span.item')]

        # Demographics
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
        logging.error(f"Error processing entry: {str(e)}")
        return None

def scrape_nekopoi():
    """Scrapes hentai schedule from Nekopoi.care"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    global loading_active
    try:
        # Start loading animation in separate thread
        loading_active = True
        animation_thread = threading.Thread(target=loading_animation, args=("🔄 Fetching Nekopoi hentai schedule...",))
        animation_thread.daemon = True
        animation_thread.start()

        time.sleep(random.uniform(3, 7))

        response = requests.get("https://nekopoi.care/jadwal-new-hentai/", headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all spoiler bodies containing hentai entries
        nekopoi_data = {}

        # Get all spoiler-body elements
        spoiler_bodies = soup.find_all('div', class_='spoiler-body')

        for spoiler_body in spoiler_bodies:
            # Find all hentai entries in this spoiler
            entries = spoiler_body.find_all('div', recursive=False)

            for entry in entries:
                try:
                    # Title
                    title_tag = entry.select_one('h2:nth-child(1) > a')
                    title = title_tag.get_text(strip=True) if title_tag else None

                    if not title:
                        continue

                    # Episode
                    eps_tag = entry.select_one('h2:nth-child(1) > span')
                    eps_text = eps_tag.get_text(strip=True) if eps_tag else ''
                    # Extract episode number
                    eps_match = re.search(r'Episode (\d+)', eps_text)
                    eps_num = int(eps_match.group(1)) if eps_match else 1

                    # Release Date
                    date_tag = entry.select_one('h2:nth-child(3) > span.release_date')
                    release_date = date_tag.get_text(strip=True) if date_tag else None

                    if not release_date:
                        continue

                    # Studio/Producer (try several approaches)
                    studio = 'Unknown'

                    # Try specific selector first
                    studio_tag = entry.select_one('h2:nth-child(3) > span:nth-child(1) > span > span')
                    if studio_tag:
                        studio = studio_tag.get_text(strip=True)

                    # If not found, search for "Producer / Label :" pattern
                    if studio == 'Unknown':
                        # Search for text containing "Producer / Label :"
                        producer_text = entry.find(text=lambda text: text and 'Producer / Label :' in text)
                        if producer_text:
                            # Extract studio name after "Producer / Label :"
                            text_parts = producer_text.split('Producer / Label :')
                            if len(text_parts) > 1:
                                studio = text_parts[1].strip()

                    # Group by release date
                    if release_date not in nekopoi_data:
                        nekopoi_data[release_date] = {}

                    if title not in nekopoi_data[release_date]:
                        nekopoi_data[release_date][title] = {'episodes': [eps_num], 'studio': studio}
                    else:
                        # Update studio if found and previously Unknown
                        if studio != 'Unknown' and nekopoi_data[release_date][title]['studio'] == 'Unknown':
                            nekopoi_data[release_date][title]['studio'] = studio
                        nekopoi_data[release_date][title]['episodes'].append(eps_num)

                except Exception as e:
                    logging.warning(f"Error parsing Nekopoi entry: {str(e)}")
                    continue

        # Process data to combine episodes
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

        # Get last update date
        last_update_tag = soup.select_one('#content > div.postsbody > div > div.contentpost > p:nth-child(14) > span > em > strong')
        last_update = "Unknown"
        if last_update_tag:
            last_update_text = last_update_tag.get_text(strip=True)
            # Extract date from format like "[Last Update 18 August 2025]"
            date_match = re.search(r'(\d{1,2}\s+\w+\s+\d{4})', last_update_text)
            if date_match:
                last_update = date_match.group(1)

        # Stop loading animation
        loading_active = False
        time.sleep(0.2)  # Give time for animation thread to finish

        logging.info(f"\n🔍 Found Nekopoi entries for {len(processed_data)} dates")
        return processed_data, last_update

    except Exception as e:
        # Stop loading animation
        loading_active = False
        time.sleep(0.2)  # Give time for animation thread to finish

        logging.error(f"❌ Error scraping Nekopoi: {str(e)}")
        return {}, "Unknown"

def scrape_mal_seasonal(url):
    """Main scraping function for MyAnimeList seasonal page."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    global loading_active
    try:
        # Start loading animation in separate thread
        loading_active = True
        animation_thread = threading.Thread(target=loading_animation, args=("🔄 Fetching MyAnimeList seasonal page...",))
        animation_thread.daemon = True
        animation_thread.start()

        time.sleep(random.uniform(3, 7))

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        if "captcha" in response.url.lower():
            raise Exception("Blocked by CAPTCHA")

        soup = BeautifulSoup(response.text, 'html.parser')
        anime_data = {}

        # Define selectors for each category
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

                    # Format release date
                    try:
                        date_obj = datetime.strptime(data['date'], '%b %d, %Y')
                        formatted_date = date_obj.strftime('%d %B')  # Fixed for Windows compatibility
                        translated_date = translate_month(formatted_date)
                    except ValueError:
                        translated_date = data['date']

                    # Save translated date in data
                    data['translated_date'] = translated_date

                    # Use original date as key for consistent parsing
                    key = data['date']
                    if key not in anime_data:
                        anime_data[key] = []
                    anime_data[key].append(data)

                    categories[cat].append(data)
            else:
                logging.info(f"🔍 No entries found for {cat}")

        # Print category messages
        for msg in log_messages:
            logging.info(msg)

        # Stop loading animation
        loading_active = False
        time.sleep(0.2)  # Give time for animation thread to finish

        logging.info(f"\n🔍 Total anime entries found: {total_entries}\n")

        return anime_data, categories

    except Exception as e:
        # Stop loading animation
        loading_active = False
        time.sleep(0.2)  # Give time for animation thread to finish

        logging.error(f"❌ Error scraping: {str(e)}")
        return {}, {}

def save_to_file(anime_data, categories, output_path, member_threshold=10000, nekopoi_data=None, nekopoi_last_update="Unknown", filter_year=2025, season_name="Unknown", year="2025"):
    """Saves anime data to file."""
    # cspell:disable-next-line
    header_template = """{season} 𝙷𝚎𝚗𝚝𝚊𝚒 𝙰𝚗𝚍 𝙽𝚘𝚛𝚖𝚊𝚕 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝
            {year}

Latest Information :
Remember : The hentai anime we take has 2 sources, which clearly show which will be released first :v so we separate the lists so you don't get confused. Oh yeah, the schedule in the ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒 list is only 2 months

Common Information for Hentai ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞 Anime list :
- Release Date
> Hentai Title
^ Studio
! Hentai Genre (ABSOLUTELY SECRET) Because I don't know the genre :v
+ Number of Episodes (if available)
~ Minutes per Episode (if available)

Common Information for Hentai ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒 Anime list :
- Release Date
> Hentai Title
^ Studio
! Hentai Genre (ABSOLUTELY SECRET) Because I don't know the genre :v
+ Episodes to be released (Meaning which eps will be released on this date in ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒)

Common Information for Normal Anime list :
- Release Date
> Anime Title
! Anime Genre
+ Number of Episodes (if available)
~ Minutes per Episode (if available)

Danger Anime Genre:
Adl : Adult
BL / Yao : Boys Love / Yaoi
Cro : Crossdressing
Ecc : Ecchi
Ero : Erotica
GL / Yur : Girls Love / Yuri
Hen : Hentai

Additional Info :
If at the end of the genre it is separated and behind the genre there is a sign ! (exclamation mark) + bold, it means beware because the genre is already weird / perverted and usually that genre enters "Danger Anime Genre", so try to read and understand well" so if something happens it's not the Admin's fault / the one who shares the recommendation if you still watch that anime with dangerous genre 🙂


Disclaimer :
All Normal Anime list and Some Hentai Anime List are taken from ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞 and Some Hentai Anime List is taken from ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒 not all anime that appears we write :v
Basically we take what we think is interesting :v

Tools  : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
Source : https://chat.whatsapp.com/CYXRhe5hGFcLpNuSpykqst
\n\n"""

    # Convert season name to fancy font
    season_mapping = {
        "Winter": "𝚆𝚒𝚗𝚝𝚎𝚛",
        "Spring": "𝚂𝚙𝚛𝚒𝚗𝚐",
        "Summer": "𝚂𝚞𝚖𝚖𝚎𝚛",
        "Fall": "𝙵𝚊𝚕𝚕"
    }
    fancy_season = season_mapping.get(season_name, season_name)

    # Convert year to fancy numbers
    number_mapping = {
        '0': '𝟶', '1': '𝟷', '2': '𝟸', '3': '𝟹', '4': '𝟺',
        '5': '𝟻', '6': '𝟼', '7': '𝟽', '8': '𝟾', '9': '𝟿'
    }
    fancy_year = ''.join(number_mapping.get(char, char) for char in str(year))

    # Replace placeholders in header
    header = header_template.replace("{season}", fancy_season).replace("{year}", fancy_year)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header)

        # Write Nekopoi Hentai List first
        if nekopoi_data:
            f.write("\n" + "=" * 50 + "\n")
            f.write("*𝙷𝚎𝚗𝚝𝚊𝚒 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝 ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒*\n")
            f.write("=" * 50 + "\n")

            # Sort dates chronologically
            def parse_english_date(date_str):
                """Parses English date format like '27 June 2025' to datetime for sorting"""
                month_map = {
                    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
                }
                parts = date_str.split()
                if len(parts) == 3:
                    day = int(parts[0])
                    month = month_map.get(parts[1], 1)
                    year = int(parts[2])
                    return datetime(year, month, day)
                return datetime.now()  # fallback

            sorted_dates = sorted(nekopoi_data.keys(), key=parse_english_date)

            for date in sorted_dates:
                entries = nekopoi_data[date]
                f.write(f"- *{date}*\n")
                for entry in entries:
                    f.write(f"> {entry['title']}\n")
                    f.write(f"^ {entry['studio']}\n")
                    f.write("! *Hentai Genre (ABSOLUTELY SECRET) Because I don't know the genre :v*\n")
                    f.write(f"+ {entry['episodes']}\n")
                    f.write("\n")  # Add blank line between entries
                f.write("\n")

            # Add note and last update below Nekopoi list
            f.write("NOTE : Schedule may not be complete, please wait for admin update\n")
            f.write(f"Last Update : {nekopoi_last_update}\n\n")

        if not anime_data:
            f.write("\nNo anime meets the criteria\n")
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
                    else:  # Add to normal anime list if it meets requirements
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


            # Write MyAnimeList Hentai List first (after Nekopoi)
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
                        f.write(f"~ {anime['duration']} min / ep\n")
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
                        f.write(f"~ {anime['duration']} min / ep\n")
                    f.write("\n")

            # Write Normal Anime separated by category
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
                            group = f"{dt.day} {dt.strftime('%B')} {dt.year}"
                        except ValueError:
                            try:
                                dt = datetime.strptime(date_str, '%b %Y')
                                group = f"Unknown Release Date {dt.strftime('%B')} {dt.year}"
                            except ValueError:
                                dt = datetime.min
                                group = date_str
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
                                f.write(f"~ {anime['duration']} min / ep\n")
                            f.write("\n")
                else:
                    f.write("_*NONE*_\n\n")

def main():
    """Main function."""
    logging.info("="*65)
    logging.info("               MyAnimeList and NekoPoi SCRAPPER")
    logging.info("                   VERSION 11 - TheKingTermux")
    logging.info("="*65)
    logging.info(" This script will scrape seasonal anime data from MyAnimeList")
    logging.info("  Normal and Hentai and will scrape Hentai anime data from")
    logging.info("       NekoPoi and save it in the specified format.\n")

    # Available seasons
    seasons = {
        1: "Winter",
        2: "Spring",
        3: "Summer",
        4: "Fall"
    }

    # Ask for year input
    year = input("Enter year (example: 2025): \n")

    # Display season options
    print("\nChoose season:")
    for key, value in seasons.items():
        print(f"{key}. {value}")

    # Ask for season input
    season_choice = input("Please choose season (1-4): \n")

    # Validate user input
    while not season_choice.isdigit() or int(season_choice) not in seasons:
        print("Invalid input. Please choose a valid season (1-4).")
        season_choice = input("Please choose season (1-4): \n")

    custom_name = input("\nEnter output file name (leave blank for default 'AnimeList.txt'): \n").strip()

    # Ask for member threshold
    member_threshold_input = input("\nEnter member threshold (default 10000): \n").strip()
    if not member_threshold_input:
        member_threshold = 10000
    else:
        member_threshold = int(member_threshold_input)

    # Get selected season
    selected_season = seasons[int(season_choice)]

    # Map Indonesian season to English for URL
    season_url_map = {
        "Winter": "winter",
        "Spring": "spring",
        "Summer": "summer",
        "Fall": "fall"
    }
    url_season = season_url_map.get(selected_season, selected_season)

    # Construct URL based on user input
    url = f"https://myanimelist.net/anime/season/{year}/{url_season}"

    # Now scrape data using dynamically created URL
    anime_data, categories = scrape_mal_seasonal(url)

    # Scrape NekoPoi data
    nekopoi_data, nekopoi_last_update = scrape_nekopoi()

    # Save to file
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
        logging.info(f"✅  Successfully saved {total} anime to: {output_path}")
        if mal_total > 0:
            logging.info(f"   - MyAnimeList: {mal_total} entries")
        if nekopoi_total > 0:
            logging.info(f"   - Nekopoi    : {nekopoi_total} entries")
    else:
        logging.error("❌ Failed to collect anime data from both sources")

        # Possible reasons for MyAnimeList error
        logging.error("Possible reasons for MyAnimeList:")
        mal_reasons = [
            "MyAnimeList site is down",
            "Blocked by anti-scraping measures",
            "HTML structure has changed",
            "No anime with more than 10,000 members"
        ]
        for reason in mal_reasons:
            logging.error(f"- {reason}")

        # Possible reasons for Nekopoi error
        logging.error("Possible reasons for Nekopoi:")
        nekopoi_reasons = [
            "Nekopoi site is down",
            "Blocked by anti-scraping measures",
            "HTML structure has changed",
            "No hentai scheduled for current period"
        ]
        for reason in nekopoi_reasons:
            logging.error(f"- {reason}")

        logging.error("Suggestion: Check your internet connection and try again later.")
    logging.info("="*50)

if __name__ == "__main__":
    main()
