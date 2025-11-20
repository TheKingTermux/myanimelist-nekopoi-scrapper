import json
import os

class Localization:
    def __init__(self, default_lang='id'):
        self.current_lang = default_lang
        self.translations = {}
        self.load_translations()

    def load_translations(self):
        """Load translation files"""
        lang_dir = os.path.join(os.path.dirname(__file__), 'lang')

        # Default Indonesian translations
        self.translations['id'] = {
            'app_title': 'MyAnimeList & Nekopoi Scraper GUI',
            'year_label': 'Tahun:',
            'season_label': 'Musim:',
            'member_threshold_label': 'Ambang Batas Anggota:',
            'output_format_label': 'Format Output:',
            'start_scraping': 'Mulai Scraping',
            'save_results': 'Simpan Hasil',
            'filter_search': 'Filter & Cari',
            'progress_title': 'Progress',
            'results_title': 'Preview Hasil',
            'ready_status': 'Siap untuk scraping...',
            'scraping_mal': 'Scraping MyAnimeList...',
            'scraping_nekopoi': 'Scraping Nekopoi...',
            'scraping_completed': 'Scraping selesai!',
            'error_title': 'Error',
            'success_title': 'Berhasil',
            'warning_title': 'Peringatan',
            'no_data_warning': 'Tidak ada data untuk disimpan. Silakan scrape terlebih dahulu.',
            'save_success': 'Hasil disimpan ke: {path}',
            'scraping_failed': 'Scraping gagal: {error}',
            'invalid_year': 'Masukkan tahun yang valid (1917 atau lebih baru)',
            'invalid_threshold': 'Masukkan ambang batas anggota yang valid',
            'filter_window_title': 'Filter & Cari',
            'search_title_label': 'Cari Judul:',
            'min_members_label': 'Min Anggota:',
            'genre_label': 'Genre:',
            'studio_label': 'Studio:',
            'apply_filter': 'Terapkan Filter',
            'mal_data': 'Data MyAnimeList',
            'nekopoi_data': 'Data Nekopoi',
            'filtered_results': 'Hasil Filter: {mal} MAL, {nekopoi} Nekopoi',
            'seasons': ['winter', 'spring', 'summer', 'fall'],
            'season_names': ['Musim Dingin', 'Semi', 'Panas', 'Gugur'],
            'formats': ['txt', 'json', 'csv', 'pdf'],
            'format_names': ['Teks (TXT)', 'JSON', 'CSV', 'PDF'],
            'scrape_options_label': 'Opsi Scraping:',
            'no_source_selected': 'Silakan pilih setidaknya satu sumber data untuk di-scrape',
            'mal_scrape_failed': 'Scraping MyAnimeList gagal atau tidak mengembalikan data',
            'nekopoi_scrape_failed': 'Scraping Nekopoi gagal atau tidak mengembalikan data',
            'data_usage_label': 'Penggunaan Data:',
            'scrape_mal_option': 'MyAnimeList',
            'scrape_nekopoi_option': 'Nekopoi',
            'scrape_both_option': 'Keduanya',
            'header_template_both': """{season} 𝙷𝚎𝚗𝚝𝚊𝚒 𝙰𝚗𝚍 𝙽𝚘𝚛𝚖𝚊𝚕 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝
            {year}
𝙼𝚎𝚖𝚋𝚎𝚛 : {member}

Latest Information :
Inget : Anime Hentai yg w ambil ada 2 sumber, yg pastinya syudah jelas mana yg bakal up dluan :v jdi w pisahin list nya biar gk bingung. Ohh iya di list punya ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒 jadwalnya cuma {nekopoi_month} bulan (dengan {month_has_passed} bulan telah berlalu, {ahead_text})

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
\n\n""",
            'header_template_mal': """𝙼𝚢𝙰𝚗𝚒𝚖𝚎𝙻𝚒𝚜𝚝 𝙷𝚎𝚗𝚝𝚊𝚒 𝙰𝚗𝚍 𝙽𝚘𝚛𝚖𝚊𝚕 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝
            {year}
𝙼𝚎𝚖𝚋𝚎𝚛 : {member}

Common Information for Hentai ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞 Anime list :
- Tanggal Rilis
> Judul Hentai
^ Studio
! Genre Hentai (ABSOLUTELY SECRET) Soalnya gatau genrenya :v
+ Jumlah Episode (kalo udh ada)
~ Menit per Episode (kalo udh ada)

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
Semua Normal Anime list dan  Hentai Anime List diambil dari ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞

Tools  : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
Source : https://chat.whatsapp.com/CYXRhe5hGFcLpNuSpykqst
\n\n""",
            'header_template_nekopoi': """𝙽𝚎𝚔𝚘𝙿𝚘𝚒 𝙷𝚎𝚗𝚝𝚊𝚒  𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝
            {first_month - last_month} {year}
Latest Information :
Jadwal ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒 cuma {nekopoi_month} bulan (dengan {month_has_passed} bulan telah berlalu, {ahead_text})

Common Information for Hentai ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒 Anime list :
- Tanggal Rilis
> Judul Hentai
^ Studio
! Genre Hentai (ABSOLUTELY SECRET) Soalnya gatau genrenya :v
+ Episode yg bakal dirilis (Mksdnya tuh di tanggal ini eps berapa yg bakal dirilis di ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒)

Tools  : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
Source : https://chat.whatsapp.com/CYXRhe5hGFcLpNuSpykqst
\n\n""",
            'note_text': "NOTE : Jadwal mungkin belum lengkap, harap tunggu update dari admin\n",
            'last_update_text': "Update Terakhir : {nekopoi_last_update}\n\n",
            'no_anime_text': "\nTidak ada anime yang memenuhi kriteria\n",
            'hentai_list_title': "*𝙷𝚎𝚗𝚝𝚊𝚒 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝 ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞*\n",
            'erotica_list_title': "*𝙴𝚛𝚘𝚝𝚒𝚌𝚊 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝 ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞*\n",
            'normal_list_title': "*𝙽𝚘𝚛𝚖𝚊𝚕 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝*\n",
            'none_text': "_*TIDAK ADA*_\n\n",
            'scrape_mal_option': 'MyAnimeList',
            'scrape_nekopoi_option': 'Nekopoi',
            'scrape_both_option': 'Keduanya'
        }

        # English translations
        self.translations['en'] = {
            'app_title': 'MyAnimeList & Nekopoi Scraper GUI',
            'year_label': 'Year:',
            'season_label': 'Season:',
            'member_threshold_label': 'Member Threshold:',
            'output_format_label': 'Output Format:',
            'start_scraping': 'Start Scraping',
            'save_results': 'Save Results',
            'filter_search': 'Filter & Search',
            'progress_title': 'Progress',
            'results_title': 'Results Preview',
            'ready_status': 'Ready to scrape...',
            'scraping_mal': 'Scraping MyAnimeList...',
            'scraping_nekopoi': 'Scraping Nekopoi...',
            'scraping_completed': 'Scraping completed!',
            'error_title': 'Error',
            'success_title': 'Success',
            'warning_title': 'Warning',
            'no_data_warning': 'No data to save. Please scrape first.',
            'save_success': 'Results saved to: {path}',
            'scraping_failed': 'Scraping failed: {error}',
            'invalid_year': 'Please enter a valid year (1917 or later)',
            'invalid_threshold': 'Please enter a valid member threshold',
            'filter_window_title': 'Filter & Search',
            'search_title_label': 'Search Title:',
            'min_members_label': 'Min Members:',
            'genre_label': 'Genre:',
            'studio_label': 'Studio:',
            'apply_filter': 'Apply Filter',
            'mal_data': 'MyAnimeList Data',
            'nekopoi_data': 'Nekopoi Data',
            'filtered_results': 'Filtered Results: {mal} MAL, {nekopoi} Nekopoi',
            'seasons': ['winter', 'spring', 'summer', 'fall'],
            'season_names': ['Winter', 'Spring', 'Summer', 'Fall'],
            'formats': ['txt', 'json', 'csv', 'pdf'],
            'format_names': ['Text (TXT)', 'JSON', 'CSV', 'PDF'],
            'scrape_options_label': 'Scrape Options:',
            'no_source_selected': 'Please select at least one data source to scrape',
            'mal_scrape_failed': 'MyAnimeList scraping failed or returned no data',
            'nekopoi_scrape_failed': 'Nekopoi scraping failed or returned no data',
            'data_usage_label': 'Data Usage:',
            'header_template_both': """{season} 𝙷𝚎𝚗𝚝𝚊𝚒 𝙰𝚗𝚍 𝙽𝚘𝚛𝚖𝚊𝚕 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝
            {year}
  Member : {member}

  Latest Information :
  Note : The hentai anime I take comes from 2 sources, which clearly show which one will be released first :v so I separate the list so you don't get confused. Oh yeah, the schedule in the ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒 list is only {nekopoi_month} months (with {month_has_passed} months have passed, {ahead_text})

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
  + Episodes to be released (Meaning which episode will be released on this date in ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒)

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
  If at the end of the genre it is separated and behind the genre there is a sign ! (exclamation mark) + bold, it means beware because the genre is already weird / perverted and usually that genre enters "Danger Anime Genre", so try to read first and understand well" so that if there is something wrong it's not the fault of the Admin / recommender if you still watch that dangerous genre anime 🙂

  Disclaimer :
  All Normal Anime list and Some Hentai Anime List are taken from ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞 and Some Hentai Anime List is taken from ©𝙺𝚞𝚌𝚒𝚗𝚐𝙿𝚎𝚍𝚞𝚕𝚒 not all anime that appears I write :v
  Basically I take what I think is interesting :v

  Tools  : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'header_template_mal': """𝙼𝚢𝙰𝚗𝚒𝚖𝚎𝙻𝚒𝚜𝚝 𝙷𝚎𝚗𝚝𝚊𝚒 𝙰𝚗𝚍 𝙽𝚘𝚛𝚖𝚊𝚕 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝
            {year}
  Member : {member}

  Common Information for Hentai ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞 Anime list :
  - Release Date
  > Hentai Title
  ^ Studio
  ! Hentai Genre (ABSOLUTELY SECRET) Because I don't know the genre :v
  + Number of Episodes (if available)
  ~ Minutes per Episode (if available)

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
  If at the end of the genre it is separated and behind the genre there is a sign ! (exclamation mark) + bold, it means beware because the genre is already weird / perverted and usually that genre enters "Danger Anime Genre", so try to read first and understand well" so that if there is something wrong it's not the fault of the Admin / recommender if you still watch that dangerous genre anime 🙂

  Disclaimer :
  All Normal Anime list and Hentai Anime List are taken from ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞

  Tools  : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'header_template_nekopoi': """𝙽𝚎𝚔𝚘𝙿𝚘𝚒 𝙷𝚎𝚗𝚝𝚊𝚒  𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝
            {first_month - last_month} {year}
Latest Information :
Schedule ©KucingPeduli is only {nekopoi_month} months (with {month_has_passed} months have passed, {ahead_text})

Common Information for Hentai ©KucingPeduli Anime list :
- Release Date
> Hentai Title
^ Studio
! Hentai Genre (ABSOLUTELY SECRET) Because I don't know the genre :v
+ Episodes to be released (Meaning which episode will be released on this date in ©KucingPeduli)

Tools  : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'note_text': "NOTE : Schedule may not be complete, please wait for admin update\n",
            'last_update_text': "Last Update : {nekopoi_last_update}\n\n",
            'no_anime_text': "\nNo anime meets the criteria\n",
            'hentai_list_title': "*𝙷𝚎𝚗𝚝𝚊𝚒 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝 ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞*\n",
            'erotica_list_title': "*𝙴𝚛𝚘𝚝𝚒𝚌𝚊 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝 ©𝙻𝚒𝚜𝚝𝙰𝚗𝚒𝚖𝚎𝙺𝚞*\n",
            'normal_list_title': "*𝙽𝚘𝚛𝚖𝚊𝚕 𝙰𝚗𝚒𝚖𝚎 𝙻𝚒𝚜𝚝*\n",
            'none_text': "_*NONE*_\n\n",
            'scrape_mal_option': 'MyAnimeList',
            'scrape_nekopoi_option': 'Nekopoi',
            'scrape_both_option': 'Les deux'
        }

        # Japanese translations
        self.translations['ja'] = {
            'app_title': 'MyAnimeList & Nekopoi Scraper GUI',
            'year_label': '年:',
            'season_label': '季節:',
            'member_threshold_label': 'メンバーしきい値:',
            'output_format_label': '出力形式:',
            'start_scraping': 'スクレイピング開始',
            'save_results': '結果を保存',
            'filter_search': 'フィルター & 検索',
            'progress_title': '進捗',
            'results_title': '結果プレビュー',
            'ready_status': 'スクレイピングの準備完了...',
            'scraping_mal': 'MyAnimeListをスクレイピング中...',
            'scraping_nekopoi': 'Nekopoiをスクレイピング中...',
            'scraping_completed': 'スクレイピング完了！',
            'error_title': 'エラー',
            'success_title': '成功',
            'warning_title': '警告',
            'no_data_warning': '保存するデータがありません。まずスクレイピングしてください。',
            'save_success': '結果を保存しました: {path}',
            'scraping_failed': 'スクレイピング失敗: {error}',
            'invalid_year': '有効な年を入力してください（1917年以降）',
            'invalid_threshold': '有効なメンバーのしきい値を入力してください',
            'filter_window_title': 'フィルター & 検索',
            'search_title_label': 'タイトル検索:',
            'min_members_label': '最小メンバー数:',
            'genre_label': 'ジャンル:',
            'studio_label': 'スタジオ:',
            'apply_filter': 'フィルター適用',
            'mal_data': 'MyAnimeListデータ',
            'nekopoi_data': 'Nekopoiデータ',
            'filtered_results': 'フィルター結果: {mal} MAL, {nekopoi} Nekopoi',
            'seasons': ['winter', 'spring', 'summer', 'fall'],
            'season_names': ['冬', '春', '夏', '秋'],
            'formats': ['txt', 'json', 'csv', 'pdf'],
            'format_names': ['テキスト (TXT)', 'JSON', 'CSV', 'PDF'],
            'scrape_options_label': 'スクレイプオプション:',
            'no_source_selected': '少なくとも1つのデータソースを選択してください',
            'mal_scrape_failed': 'MyAnimeListスクレイピングが失敗したかデータを返しませんでした',
            'nekopoi_scrape_failed': 'Nekopoiスクレイピングが失敗したかデータを返しませんでした',
            'data_usage_label': 'データ使用量:',
            'scrape_mal_option': 'MyAnimeList',
            'scrape_nekopoi_option': 'Nekopoi',
            'scrape_both_option': '両方',
            'header_template_both': """{season} ヘンタイとノーマルアニメリスト
            {year}
メンバー : {member}

最新情報 :
注意 : 私が取るヘンタイアニメは2つのソースから来ており、どちらが先にリリースされるかを明確に示しています :v だから混乱しないようにリストを分けます。ああ、そうだ、©KucingPeduli リストのスケジュールは {nekopoi_month} ヶ月だけ ( {month_has_passed} ヶ月が経過, {ahead_text})

ヘンタイ ©ListAnimeKu アニメリストの共通情報 :
- リリース日
> ヘンタイタイトル
^ スタジオ
! ヘンタイジャンル (絶対秘密) ジャンルがわからないから :v
+ エピソード数 (利用可能な場合)
~ エピソードごとの分 (利用可能な場合)

ヘンタイ ©KucingPeduli アニメリストの共通情報 :
- リリース日
> ヘンタイタイトル
^ スタジオ
! ヘンタイジャンル (絶対秘密) ジャンルがわからないから :v
+ リリースされるエピソード (この日に ©KucingPeduli でリリースされるエピソードの意味)

ノーマルアニメリストの共通情報 :
- リリース日
> アニメタイトル
! アニメジャンル
+ エピソード数 (利用可能な場合)
~ エピソードごとの分 (利用可能な場合)

危険アニメジャンル:
Adl : アダルト
BL / Yao : ボーイズラブ / ヤオイ
Cro : クロスドレッシング
Ecc : エッチ
Ero : エロティカ
GL / Yur : ガールズラブ / ユリ
Hen : ヘンタイ

追加情報 :
ジャンルの終わりが分離されていて、ジャンルの後ろに ! (感嘆符) + 太字がある場合、それは注意を意味します。なぜならジャンルはすでに奇妙 / 変態的で、通常 "Danger Anime Genre" に入るからです、だからまず読んでよく理解してください" 何か問題があればそれが危険なジャンルアニメを見続ける場合の管理者 / 推薦者の責任ではありません 🙂

免責事項 :
すべてのノーマルアニメリストと一部のヘンタイアニメリストは ©ListAnimeKu から取り、一部のヘンタイアニメリストは ©KucingPeduli から取ります すべての表示されるアニメを書くわけではありません :v
基本的に私が面白いと思うものを取ります :v

ツール : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'header_template_mal': """𝙼𝚢𝙰𝚗𝚒𝚖𝚎𝙻𝚒𝚜𝚝 ヘンタイとノーマルアニメリスト
{year}
メンバー : {member}

ヘンタイ ©ListAnimeKu アニメリストの共通情報 :
- リリース日
> ヘンタイタイトル
^ スタジオ
! ヘンタイジャンル (絶対秘密) ジャンルがわからないから :v
+ エピソード数 (利用可能な場合)
~ エピソードごとの分 (利用可能な場合)

ノーマルアニメリストの共通情報 :
- リリース日
> アニメタイトル
! アニメジャンル
+ エピソード数 (利用可能な場合)
~ エピソードごとの分 (利用可能な場合)

危険アニメジャンル:
Adl : アダルト
BL / Yao : ボーイズラブ / ヤオイ
Cro : クロスドレッシング
Ecc : エッチ
Ero : エロティカ
GL / Yur : ガールズラブ / ユリ
Hen : ヘンタイ

追加情報 :
ジャンルの終わりが分離されていて、ジャンルの後ろに ! (感嘆符) + 太字がある場合、それは注意を意味します。なぜならジャンルはすでに奇妙 / 変態的で、通常 "Danger Anime Genre" に入るからです、だからまず読んでよく理解してください" 何か問題があればそれが危険なジャンルアニメを見続ける場合の管理者 / 推薦者の責任ではありません 🙂

免責事項 :
すべてのノーマルアニメリストと ヘンタイアニメリストは ©ListAnimeKuから

ツール : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'header_template_nekopoi': """𝙽𝚎𝚔𝚘𝙿𝚘𝚒 ヘンタイ アニメリスト
{first_month - last_month} {year}
最新情報 :
©KucingPeduli のスケジュールは {nekopoi_month} ヶ月だけ ( {month_has_passed} ヶ月が経過, {ahead_text})

ヘンタイ ©KucingPeduli アニメリストの共通情報 :
- リリース日
> ヘンタイタイトル
^ スタジオ
! ヘンタイジャンル (絶対秘密) ジャンルがわからないから :v
+ リリースされるエピソード (この日に ©KucingPeduli でリリースされるエピソードの意味)

ツール : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'note_text': "注意 : スケジュールが完全でない可能性があります、管理者の更新をお待ちください\n",
            'last_update_text': "最終更新 : {nekopoi_last_update}\n\n",
            'no_anime_text': "\n基準を満たすアニメはありません\n",
            'hentai_list_title': "*ヘンタイアニメリスト ©ListAnimeKu*\n",
            'erotica_list_title': "*エロティカアニメリスト ©ListAnimeKu*\n",
            'normal_list_title': "*ノーマルアニメリスト*\n",
            'none_text': "_*なし*_\n\n"
        }

        # Spanish translations
        self.translations['es'] = {
            'app_title': 'MyAnimeList & Nekopoi Scraper GUI',
            'year_label': 'Año:',
            'season_label': 'Temporada:',
            'member_threshold_label': 'Umbral de Miembros:',
            'output_format_label': 'Formato de Salida:',
            'start_scraping': 'Iniciar Scraping',
            'save_results': 'Guardar Resultados',
            'filter_search': 'Filtrar & Buscar',
            'progress_title': 'Progreso',
            'results_title': 'Vista Previa de Resultados',
            'ready_status': 'Listo para scrapear...',
            'scraping_mal': 'Scrapeando MyAnimeList...',
            'scraping_nekopoi': 'Scrapeando Nekopoi...',
            'scraping_completed': '¡Scraping completado!',
            'error_title': 'Error',
            'success_title': 'Éxito',
            'warning_title': 'Advertencia',
            'no_data_warning': 'No hay datos para guardar. Por favor, scrape primero.',
            'save_success': 'Resultados guardados en: {path}',
            'scraping_failed': 'Scraping falló: {error}',
            'invalid_year': 'Por favor ingrese un año válido (1917 o posterior)',
            'invalid_threshold': 'Por favor ingrese un umbral de miembros válido',
            'filter_window_title': 'Filtrar & Buscar',
            'search_title_label': 'Buscar Título:',
            'min_members_label': 'Mín. Miembros:',
            'genre_label': 'Género:',
            'studio_label': 'Estudio:',
            'apply_filter': 'Aplicar Filtro',
            'mal_data': 'Datos de MyAnimeList',
            'nekopoi_data': 'Datos de Nekopoi',
            'filtered_results': 'Resultados Filtrados: {mal} MAL, {nekopoi} Nekopoi',
            'scrape_options_label': 'Opciones de Scraping:',
            'no_source_selected': 'Por favor seleccione al menos una fuente de datos para scrapear',
            'mal_scrape_failed': 'El scraping de MyAnimeList falló o no devolvió datos',
            'nekopoi_scrape_failed': 'El scraping de Nekopoi falló o no devolvió datos',
            'data_usage_label': 'Uso de Datos:',
            'seasons': ['winter', 'spring', 'summer', 'fall'],
            'season_names': ['Invierno', 'Primavera', 'Verano', 'Otoño'],
            'formats': ['txt', 'json', 'csv', 'pdf'],
            'format_names': ['Texto (TXT)', 'JSON', 'CSV', 'PDF'],
            'scrape_mal_option': 'MyAnimeList',
            'scrape_nekopoi_option': 'Nekopoi',
            'scrape_both_option': 'Ambos',
            'header_template_both': """{season} Lista de Anime Hentai y Normal

{year}
Miembro : {member}

Última Información :
Nota : Los animes hentai que tomo provienen de 2 fuentes, que claramente muestran cuál se lanzará primero :v así que separo la lista para no confundirte. Ah sí, el horario en la lista de ©KucingPeduli es solo {nekopoi_month} meses (con {month_has_passed} meses transcurridos, {ahead_text})

Información Común para la lista de Anime Hentai ©ListAnimeKu :
- Fecha de Lanzamiento
> Título Hentai
^ Estudio
! Género Hentai (ABSOLUTAMENTE SECRETO) Porque no sé el género :v
+ Número de Episodios (si está disponible)
~ Minutos por Episodio (si está disponible)

Información Común para la lista de Anime Hentai ©KucingPeduli :
- Fecha de Lanzamiento
> Título Hentai
^ Estudio
! Género Hentai (ABSOLUTAMENTE SECRETO) Porque no sé el género :v
+ Episodios a lanzarse (Significado cuál episodio se lanzará en esta fecha en ©KucingPeduli)

Información Común para la lista de Anime Normal :
- Fecha de Lanzamiento
> Título Anime
! Género Anime
+ Número de Episodios (si está disponible)
~ Minutos por Episodio (si está disponible)

Género de Anime Peligroso:
Adl : Adulto
BL / Yao : Boys Love / Yaoi
Cro : Crossdressing
Ecc : Ecchi
Ero : Erotica
GL / Yur : Girls Love / Yuri
Hen : Hentai

Información Adicional :
Si al final del género está separado y detrás del género hay un signo ! (signo de exclamación) + negrita, significa cuidado porque el género ya es raro / pervertido y usualmente entra en "Danger Anime Genre", so try to read first and understand well" para que si hay algo mal no sea culpa del Admin / recomendador si sigues viendo ese anime de género peligroso 🙂

Descargo de Responsabilidad :
Todas las listas de Anime Normal y Algunas Listas de Anime Hentai se toman de ©ListAnimeKu y Algunas Listas de Anime Hentai se toman de ©KucingPeduli no escribo todos los animes que aparecen :v
Básicamente tomo lo que pienso que es interesante :v

Herramientas : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'header_template_mal': """𝙼𝚢𝙰𝚗𝚒𝚖𝚎𝙻𝚒𝚜𝚝 Lista de Anime Hentai y Normal
{year}
Miembro : {member}

Información Común para la lista de Anime Hentai ©ListAnimeKu :
- Fecha de Lanzamiento
> Título Hentai
^ Estudio
! Género Hentai (ABSOLUTAMENTE SECRETO) Porque no sé el género :v
+ Número de Episodios (si está disponible)
~ Minutos por Episodio (si está disponible)

Información Común para la lista de Anime Normal :
- Fecha de Lanzamiento
> Título Anime
! Género Anime
+ Número de Episodios (si está disponible)
~ Minutos por Episodio (si está disponible)

Género de Anime Peligroso:
Adl : Adulto
BL / Yao : Boys Love / Yaoi
Cro : Crossdressing
Ecc : Ecchi
Ero : Erotica
GL / Yur : Girls Love / Yuri
Hen : Hentai

Información Adicional :
Si al final del género está separado y detrás del género hay un signo ! (signo de exclamación) + negrita, significa cuidado porque el género ya es raro / pervertido y normalmente entra en "Danger Anime Genre", so try to read first and understand well" para que si hay algo mal no sea culpa del Admin / recomendador si sigues viendo ese anime de género peligroso 🙂

Descargo de Responsabilidad :
Todas las listas de Anime Normal y Hentai Anime List son tomadas de ©ListAnimeKu

Herramientas : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'header_template_nekopoi': """𝙽𝚎𝚔𝚘𝙿𝚘𝚒 Lista de Anime Hentai
{first_month - last_month} {year}
Última Información :
El horario en la lista ©KucingPeduli es solo {nekopoi_month} meses (con {month_has_passed} meses transcurridos, {ahead_text})

Información Común para la lista de Anime Hentai ©KucingPeduli :
- Fecha de Lanzamiento
> Título Hentai
^ Estudio
! Género Hentai (ABSOLUTAMENTE SECRETO) Porque no sé el género :v
+ Episodios a lanzarse (Significado cuál episodio se lanzará en esta fecha en ©KucingPeduli)

Herramientas : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'note_text': "NOTA : El horario puede no estar completo, por favor espera la actualización del admin\n",
            'last_update_text': "Última Actualización : {nekopoi_last_update}\n\n",
            'no_anime_text': "\nNingún anime cumple con los criterios\n",
            'hentai_list_title': "*Lista de Anime Hentai ©ListAnimeKu*\n",
            'erotica_list_title': "*Lista de Anime Erótica ©ListAnimeKu*\n",
            'normal_list_title': "*Lista de Anime Normal*\n",
            'none_text': "_*NINGUNO*_\n\n"
        }

        # Chinese (Simplified) translations
        self.translations['zh'] = {
            'app_title': 'MyAnimeList & Nekopoi 刮取器 GUI',
            'year_label': '年份:',
            'season_label': '季节:',
            'member_threshold_label': '成员阈值:',
            'output_format_label': '输出格式:',
            'start_scraping': '开始刮取',
            'save_results': '保存结果',
            'filter_search': '筛选 & 搜索',
            'progress_title': '进度',
            'results_title': '结果预览',
            'ready_status': '准备刮取...',
            'scraping_mal': '正在刮取 MyAnimeList...',
            'scraping_nekopoi': '正在刮取 Nekopoi...',
            'scraping_completed': '刮取完成！',
            'error_title': '错误',
            'success_title': '成功',
            'warning_title': '警告',
            'no_data_warning': '没有数据可保存。请先刮取。',
            'save_success': '结果已保存到: {path}',
            'scraping_failed': '刮取失败: {error}',
            'invalid_year': '请输入有效年份（1917年或之后）',
            'invalid_threshold': '请输入有效的成员阈值',
            'filter_window_title': '筛选 & 搜索',
            'search_title_label': '搜索标题:',
            'min_members_label': '最小成员数:',
            'genre_label': '类型:',
            'studio_label': '工作室:',
            'apply_filter': '应用筛选',
            'mal_data': 'MyAnimeList 数据',
            'nekopoi_data': 'Nekopoi 数据',
            'filtered_results': '筛选结果: {mal} MAL, {nekopoi} Nekopoi',
            'seasons': ['winter', 'spring', 'summer', 'fall'],
            'season_names': ['冬季', '春季', '夏季', '秋季'],
            'formats': ['txt', 'json', 'csv', 'pdf'],
            'format_names': ['文本 (TXT)', 'JSON', 'CSV', 'PDF'],
            'scrape_options_label': '刮取选项:',
            'no_source_selected': '请至少选择一个数据源进行刮取',
            'mal_scrape_failed': 'MyAnimeList 刮取失败或未返回数据',
            'nekopoi_scrape_failed': 'Nekopoi 刮取失败或未返回数据',
            'data_usage_label': '数据使用量:',
            'scrape_mal_option': 'MyAnimeList',
            'scrape_nekopoi_option': 'Nekopoi',
            'scrape_both_option': '两者',
            'header_template_both': """{season} 变态和正常动漫列表

{year}
成员 : {member}

最新信息 :
注意 : 我拿的变态动漫来自2个来源，它们清楚地显示哪个会先发布 :v 所以我分开列表以免你困惑。哦对了，©KucingPeduli 列表的日程只有 {nekopoi_month} 个月 (已过去 {month_has_passed} 个月, {ahead_text})

变态动漫 ©ListAnimeKu 动漫列表的常见信息 :
- 发布日期
> 变态标题
^ 工作室
! 变态类型 (绝对秘密) 因为我不知道类型 :v
+ 集数 (如果可用)
~ 每集分钟 (如果可用)

变态动漫 ©KucingPeduli 动漫列表的常见信息 :
- 发布日期
> 变态标题
^ 工作室
! 变态类型 (绝对秘密) 因为我不知道类型 :v
+ 要发布的集数 (意思是这一天在 ©KucingPeduli 要发布的集数)

正常动漫列表的常见信息 :
- 发布日期
> 动漫标题
! 动漫类型
+ 集数 (如果可用)
~ 每集分钟 (如果可用)

危险动漫类型:
Adl : 成人
BL / Yao : Boys Love / Yaoi
Cro : Crossdressing
Ecc : Ecchi
Ero : Erotica
GL / Yur : Girls Love / Yuri
Hen : Hentai

附加信息 :
如果类型末尾分开并且类型后面有 ! (感叹号) + 粗体，表示小心因为类型已经奇怪 / 变态，通常进入 "Danger Anime Genre"，所以尽量先读并理解好" 以免如果有问题不是管理员 / 推荐者的错如果你继续看那个危险类型动漫 🙂

免责声明 :
所有正常动漫列表和一些变态动漫列表取自 ©ListAnimeKu 一些变态动漫列表取自 ©KucingPeduli 我不写所有出现的动漫 :v
基本上我拿我觉得有趣的 :v

工具 : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'header_template_mal': """𝙼𝚢𝙰𝚗𝚒𝚖𝚎𝙻𝚒𝚜𝚝 变态和正常动漫列表
{year}
成员 : {member}

变态动漫 ©ListAnimeKu 动漫列表的常见信息 :
- 发布日期
> 变态标题
^ 工作室
! 变态类型 (绝对秘密) 因为我不知道类型 :v
+ 集数 (如果可用)
~ 每集分钟 (如果可用)

正常动漫列表的常见信息 :
- 发布日期
> 动漫标题
! 动漫类型
+ 集数 (如果可用)
~ 每集分钟 (如果可用)

危险动漫类型:
Adl : 成人
BL / Yao : Boys Love / Yaoi
Cro : Crossdressing
Ecc : Ecchi
Ero : Erotica
GL / Yur : Girls Love / Yuri
Hen : Hentai

附加信息 :
如果类型末尾分开并且类型后面有 ! (感叹号) + 粗体，表示小心因为类型已经奇怪 / 变态，通常进入 "Danger Anime Genre"，所以尽量先读并理解好" 以免如果有问题不是管理员 / 推荐者的错如果你继续看那个危险类型动漫 🙂

免责声明 :
所有正常动漫列表和变态动漫列表取自 ©ListAnimeKu

工具 : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'header_template_nekopoi': """𝙽𝚎𝚔𝚘𝙿𝚘𝚒 变态动漫列表
{first_month - last_month} {year}
最新信息 :
©KucingPeduli 列表的日程只有 {nekopoi_month} 个月 (已过去 {month_has_passed} 个月, {ahead_text})

变态动漫 ©KucingPeduli 动漫列表的常见信息 :
- 发布日期
> 变态标题
^ 工作室
! 变态类型 (绝对秘密) 因为我不知道类型 :v
+ 要发布的集数 (意思是这一天在 ©KucingPeduli 要发布的集数)

工具 : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'note_text': "注意 : 日程可能不完整，请等待管理员更新\n",
            'last_update_text': "最后更新 : {nekopoi_last_update}\n\n",
            'no_anime_text': "\n没有动漫符合标准\n",
            'hentai_list_title': "*变态动漫列表 ©ListAnimeKu*\n",
            'erotica_list_title': "*色情动漫列表 ©ListAnimeKu*\n",
            'normal_list_title': "*正常动漫列表*\n",
            'none_text': "_*无*_\n\n"
        }

        # Korean translations
        self.translations['ko'] = {
            'app_title': 'MyAnimeList & Nekopoi 스크래퍼 GUI',
            'year_label': '년:',
            'season_label': '계절:',
            'member_threshold_label': '회원 임계값:',
            'output_format_label': '출력 형식:',
            'start_scraping': '스크래핑 시작',
            'save_results': '결과 저장',
            'filter_search': '필터 & 검색',
            'progress_title': '진행',
            'results_title': '결과 미리보기',
            'ready_status': '스크래핑 준비 완료...',
            'scraping_mal': 'MyAnimeList 스크래핑 중...',
            'scraping_nekopoi': 'Nekopoi 스크래핑 중...',
            'scraping_completed': '스크래핑 완료!',
            'error_title': '오류',
            'success_title': '성공',
            'warning_title': '경고',
            'no_data_warning': '저장할 데이터가 없습니다. 먼저 스크래핑하세요.',
            'save_success': '결과가 다음 위치에 저장됨: {path}',
            'scraping_failed': '스크래핑 실패: {error}',
            'invalid_year': '유효한 년도를 입력하세요 (1917년 이후)',
            'invalid_threshold': '유효한 회원 임계값을 입력하세요',
            'filter_window_title': '필터 & 검색',
            'search_title_label': '제목 검색:',
            'min_members_label': '최소 회원 수:',
            'genre_label': '장르:',
            'studio_label': '스튜디오:',
            'apply_filter': '필터 적용',
            'mal_data': 'MyAnimeList 데이터',
            'nekopoi_data': 'Nekopoi 데이터',
            'filtered_results': '필터링된 결과: {mal} MAL, {nekopoi} Nekopoi',
            'seasons': ['winter', 'spring', 'summer', 'fall'],
            'season_names': ['겨울', '봄', '여름', '가을'],
            'formats': ['txt', 'json', 'csv', 'pdf'],
            'format_names': ['텍스트 (TXT)', 'JSON', 'CSV', 'PDF'],
            'scrape_options_label': '스크래핑 옵션:',
            'no_source_selected': '스크래핑할 데이터 소스를 하나 이상 선택하세요',
            'mal_scrape_failed': 'MyAnimeList 스크래핑이 실패했거나 데이터를 반환하지 않았습니다',
            'nekopoi_scrape_failed': 'Nekopoi 스크래핑이 실패했거나 데이터를 반환하지 않았습니다',
            'data_usage_label': '데이터 사용량:',
            'scrape_mal_option': 'MyAnimeList',
            'scrape_nekopoi_option': 'Nekopoi',
            'scrape_both_option': '둘 다',
            'header_template_both': """{season} 헨타이와 일반 애니메이션 목록

{year}
회원 : {member}

최신 정보 :
참고 : 내가 가져오는 헨타이 애니메이션은 2개의 소스에서 나오며, 어느 것이 먼저 출시될지 명확히 보여줍니다 :v 그래서 혼동되지 않도록 목록을 분리합니다. 아 맞아, ©KucingPeduli 목록의 일정은 {nekopoi_month}개월만 ( {month_has_passed}개월이 지났음, {ahead_text})

헨타이 ©ListAnimeKu 애니메이션 목록의 공통 정보 :
- 출시 날짜
> 헨타이 제목
^ 스튜디오
! 헨타이 장르 (절대 비밀) 장르를 모르기 때문에 :v
+ 에피소드 수 (가능한 경우)
~ 에피소드당 분 (가능한 경우)

헨타이 ©KucingPeduli 애니메이션 목록의 공통 정보 :
- 출시 날짜
> 헨타이 제목
^ 스튜디오
! 헨타이 장르 (절대 비밀) 장르를 모르기 때문에 :v
+ 출시될 에피소드 (이 날짜에 ©KucingPeduli에서 출시될 에피소드 의미)

일반 애니메이션 목록의 공통 정보 :
- 출시 날짜
> 애니메이션 제목
! 애니메이션 장르
+ 에피소드 수 (가능한 경우)
~ 에피소드당 분 (가능한 경우)

위험 애니메이션 장르:
Adl : 성인
BL / Yao : Boys Love / Yaoi
Cro : Crossdressing
Ecc : Ecchi
Ero : Erotica
GL / Yur : Girls Love / Yuri
Hen : Hentai

추가 정보 :
장르 끝이 분리되고 장르 뒤에 ! (느낌표) + 굵은 글씨가 있으면, 장르가 이미 이상 / 변태적이고 일반적으로 "Danger Anime Genre"에 들어가기 때문에 조심하라는 의미입니다, 그래서 먼저 읽고 잘 이해하세요" 만약 문제가 있으면 관리자 / 추천자의 잘못이 아닙니다 만약 당신이 그 위험 장르 애니메이션을 계속 본다면 🙂

면책 조항 :
모든 일반 애니메이션 목록과 일부 헨타이 애니메이션 목록은 ©ListAnimeKu에서 가져오고 일부 헨타이 애니메이션 목록은 ©KucingPeduli에서 가져옵니다 모든 나타나는 애니메이션을 쓰는 것이 아닙니다 :v
기본적으로 내가 흥미롭다고 생각하는 것을 가져옵니다 :v

도구 : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'header_template_mal': """𝙼𝚢𝙰𝚗𝚒𝚖𝚎𝙻𝚒𝚜𝚝 헨타이와 일반 애니메이션 목록
{year}
회원 : {member}

헨타이 ©ListAnimeKu 애니메이션 목록의 공통 정보 :
- 출시 날짜
> 헨타이 제목
^ 스튜디오
! 헨타이 장르 (절대 비밀) 장르를 모르기 때문에 :v
+ 에피소드 수 (가능한 경우)
~ 에피소드당 분 (가능한 경우)

일반 애니메이션 목록의 공통 정보 :
- 출시 날짜
> 애니메이션 제목
! 애니메이션 장르
+ 에피소드 수 (가능한 경우)
~ 에피소드당 분 (가능한 경우)

위험 애니메이션 장르:
Adl : 성인
BL / Yao : Boys Love / Yaoi
Cro : Crossdressing
Ecc : Ecchi
Ero : Erotica
GL / Yur : Girls Love / Yuri
Hen : Hentai

추가 정보 :
장르 끝이 분리되고 장르 뒤에 ! (느낌표) + 굵은 글씨가 있으면, 장르가 이미 이상 / 변태적이고 일반적으로 "Danger Anime Genre"에 들어가기 때문에 조심하라는 의미입니다, 그래서 먼저 읽고 잘 이해하세요" 만약 문제가 있으면 관리자 / 추천자의 잘못이 아닙니다 만약 당신이 그 위험 장르 애니메이션을 계속 본다면 🙂

면책 조항 :
모든 일반 애니메이션 목록과 헨타이 애니메이션 목록은 ©ListAnimeKu에서 가져옵니다

도구 : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'header_template_nekopoi': """𝙽𝚎𝚔𝚘𝙿𝚘𝚒 헨타이 애니메이션 목록
{first_month - last_month} {year}
최신 정보 :
©KucingPeduli 목록의 일정은 {nekopoi_month}개월만 ( {month_has_passed}개월이 지났음, {ahead_text})

헨타이 ©KucingPeduli 애니메이션 목록의 공통 정보 :
- 출시 날짜
> 헨타이 제목
^ 스튜디오
! 헨타이 장르 (절대 비밀) 장르를 모르기 때문에 :v
+ 출시될 에피소드 (이 날짜에 ©KucingPeduli에서 출시될 에피소드 의미)

도구 : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'note_text': "참고 : 일정이 완전하지 않을 수 있습니다, 관리자 업데이트를 기다려주세요\n",
            'last_update_text': "마지막 업데이트 : {nekopoi_last_update}\n\n",
            'no_anime_text': "\n기준에 맞는 애니메이션이 없습니다\n",
            'hentai_list_title': "*헨타이 애니메이션 목록 ©ListAnimeKu*\n",
            'erotica_list_title': "*에로티카 애니메이션 목록 ©ListAnimeKu*\n",
            'normal_list_title': "*일반 애니메이션 목록*\n",
            'none_text': "_*없음*_\n\n"
        }

        # French translations
        self.translations['fr'] = {
            'app_title': 'MyAnimeList & Nekopoi Scraper GUI',
            'year_label': 'Année:',
            'season_label': 'Saison:',
            'member_threshold_label': 'Seuil de Membres:',
            'output_format_label': 'Format de Sortie:',
            'start_scraping': 'Démarrer le Scraping',
            'save_results': 'Sauvegarder les Résultats',
            'filter_search': 'Filtrer & Rechercher',
            'progress_title': 'Progrès',
            'results_title': 'Aperçu des Résultats',
            'ready_status': 'Prêt à scraper...',
            'scraping_mal': 'Scraping MyAnimeList...',
            'scraping_nekopoi': 'Scraping Nekopoi...',
            'scraping_completed': 'Scraping terminé!',
            'error_title': 'Erreur',
            'success_title': 'Succès',
            'warning_title': 'Avertissement',
            'no_data_warning': 'Aucune donnée à sauvegarder. Veuillez d\'abord scraper.',
            'save_success': 'Résultats sauvegardés dans: {path}',
            'scraping_failed': 'Échec du scraping: {error}',
            'invalid_year': 'Veuillez saisir une année valide (1917 ou ultérieure)',
            'invalid_threshold': 'Veuillez saisir un seuil de membres valide',
            'filter_window_title': 'Filtrer & Rechercher',
            'search_title_label': 'Rechercher Titre:',
            'min_members_label': 'Min. Membres:',
            'genre_label': 'Genre:',
            'studio_label': 'Studio:',
            'apply_filter': 'Appliquer le Filtre',
            'mal_data': 'Données MyAnimeList',
            'nekopoi_data': 'Données Nekopoi',
            'filtered_results': 'Résultats Filtrés: {mal} MAL, {nekopoi} Nekopoi',
            'seasons': ['winter', 'spring', 'summer', 'fall'],
            'season_names': ['Hiver', 'Printemps', 'Été', 'Automne'],
            'formats': ['txt', 'json', 'csv', 'pdf'],
            'format_names': ['Texte (TXT)', 'JSON', 'CSV', 'PDF'],
            'scrape_options_label': 'Options de Scraping:',
            'no_source_selected': 'Veuillez sélectionner au moins une source de données à scraper',
            'mal_scrape_failed': 'Le scraping MyAnimeList a échoué ou n\'a pas retourné de données',
            'nekopoi_scrape_failed': 'Le scraping Nekopoi a échoué ou n\'a pas retourné de données',
            'data_usage_label': 'Utilisation des Données:',
            'header_template_both': """{season} Liste d'Anime Hentai et Normal
            {year}
 Membre : {member}

 Dernières Informations :
 Note : Les animes hentai que je prends viennent de 2 sources, qui montrent clairement lequel sera publié en premier :v alors je sépare la liste pour ne pas te confondre. Ah oui, le calendrier dans la liste ©KucingPeduli est seulement {nekopoi_month} mois (avec {month_has_passed} mois passés, {ahead_text})

 Informations Communes pour la liste d'Anime Hentai ©ListAnimeKu :
 - Date de Sortie
 > Titre Hentai
 ^ Studio
 ! Genre Hentai (ABSOLUMENT SECRET) Parce que je ne connais pas le genre :v
 + Nombre d'Épisodes (si disponible)
 ~ Minutes par Épisode (si disponible)

 Informations Communes pour la liste d'Anime Hentai ©KucingPeduli :
 - Date de Sortie
 > Titre Hentai
 ^ Studio
 ! Genre Hentai (ABSOLUMENT SECRET) Parce que je ne connais pas le genre :v
 + Épisodes à sortir (Signifiant quel épisode sera sorti à cette date dans ©KucingPeduli)

 Informations Communes pour la liste d'Anime Normal :
 - Date de Sortie
 > Titre Anime
 ! Genre Anime
 + Nombre d'Épisodes (si disponible)
 ~ Minutes par Épisode (si disponible)

 Genre d'Anime Dangereux:
 Adl : Adulte
 BL / Yao : Boys Love / Yaoi
 Cro : Crossdressing
 Ecc : Ecchi
 Ero : Erotica
 GL / Yur : Girls Love / Yuri
 Hen : Hentai

 Info Additionnelle :
 Si à la fin du genre il est séparé et derrière le genre il y a un signe ! (point d'exclamation) + gras, cela signifie attention parce que le genre est déjà bizarre / pervers et entre généralement dans "Danger Anime Genre", alors essayez de lire d'abord et de bien comprendre" pour que si il y a quelque chose de mal ce ne soit pas la faute de l'Admin / recommandeur si vous continuez à regarder cet anime de genre dangereux 🙂

 Avis de Non-Responsabilité :
 Toutes les listes d'Anime Normal et Certaines Listes d'Anime Hentai sont prises de ©ListAnimeKu et Certaines Listes d'Anime Hentai sont prises de ©KucingPeduli je n'écris pas tous les animes qui apparaissent :v
 Fondamentalement je prends ce que je pense être intéressant :v

 Outils : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
 \n\n""",
             'header_template_mal': """𝙼𝚢𝙰𝚗𝚒𝚖𝚎𝙻𝚒𝚜𝚝 Liste d'Anime Hentai et Normal
 {year}
 Membre : {member}
 
 Informations Communes pour la liste d'Anime Hentai ©ListAnimeKu :
 - Date de Sortie
 > Titre Hentai
 ^ Studio
 ! Genre Hentai (ABSOLUMENT SECRET) Parce que je ne connais pas le genre :v
 + Nombre d'Épisodes (si disponible)
 ~ Minutes par Épisode (si disponible)
 
 Informations Communes pour la liste d'Anime Normal :
 - Date de Sortie
 > Titre Anime
 ! Genre Anime
 + Nombre d'Épisodes (si disponible)
 ~ Minutes par Épisode (si disponible)
 
 Genre d'Anime Dangereux:
 Adl : Adulte
 BL / Yao : Boys Love / Yaoi
 Cro : Crossdressing
 Ecc : Ecchi
 Ero : Erotica
 GL / Yur : Girls Love / Yuri
 Hen : Hentai
 
 Info Additionnelle :
 Si à la fin du genre il est séparé et derrière le genre il y a un signe ! (point d'exclamation) + gras, cela signifie attention parce que le genre est déjà bizarre / pervers et entre généralement dans "Danger Anime Genre", alors essayez de lire d'abord et de bien comprendre" pour que si il y a quelque chose de mal ce ne soit pas la faute de l'Admin / recommandeur si vous continuez à regarder cet anime de genre dangereux 🙂
 
 Avis de Non-Responsabilité :
 Toutes les listes d'Anime Normal et Hentai Anime List sont prises de ©ListAnimeKu
 
 Outils : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
 \n\n""",
             'header_template_nekopoi': """𝙽𝚎𝚔𝚘𝙿𝚘𝚒 Liste d'Anime Hentai
 {first_month - last_month} {year}
 Dernières Informations :
 Le calendrier dans la liste ©KucingPeduli est seulement {nekopoi_month} mois (avec {month_has_passed} mois passés, {ahead_text})
 
 Informations Communes pour la liste d'Anime Hentai ©KucingPeduli :
 - Date de Sortie
 > Titre Hentai
 ^ Studio
 ! Genre Hentai (ABSOLUMENT SECRET) Parce que je ne connais pas le genre :v
 + Épisodes à sortir (Signifiant quel épisode sera sorti à cette date dans ©KucingPeduli)
 
 Outils : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
 \n\n""",
             'note_text': "NOTE : Le calendrier peut ne pas être complet, veuillez attendre la mise à jour de l'admin\n",
            'last_update_text': "Dernière mise à jour : {nekopoi_last_update}\n\n",
            'no_anime_text': "\nAucun anime ne répond aux critères\n",
            'hentai_list_title': "*Liste d'Anime Hentai ©ListAnimeKu*\n",
            'erotica_list_title': "*Liste d'Anime Érotica ©ListAnimeKu*\n",
            'normal_list_title': "*Liste d'Anime Normal*\n",
            'none_text': "_*AUCUN*_\n\n"
        }

        # German translations
        self.translations['de'] = {
            'app_title': 'MyAnimeList & Nekopoi Scraper GUI',
            'year_label': 'Jahr:',
            'season_label': 'Jahreszeit:',
            'member_threshold_label': 'Mitglieder-Schwellenwert:',
            'output_format_label': 'Ausgabeformat:',
            'start_scraping': 'Scraping Starten',
            'save_results': 'Ergebnisse Speichern',
            'filter_search': 'Filtern & Suchen',
            'progress_title': 'Fortschritt',
            'results_title': 'Ergebnisvorschau',
            'ready_status': 'Bereit zum Scrapen...',
            'scraping_mal': 'MyAnimeList wird gescrapt...',
            'scraping_nekopoi': 'Nekopoi wird gescrapt...',
            'scraping_completed': 'Scraping abgeschlossen!',
            'error_title': 'Fehler',
            'success_title': 'Erfolg',
            'warning_title': 'Warnung',
            'no_data_warning': 'Keine Daten zum Speichern. Bitte zuerst scrapen.',
            'save_success': 'Ergebnisse gespeichert in: {path}',
            'scraping_failed': 'Scraping fehlgeschlagen: {error}',
            'invalid_year': 'Bitte geben Sie ein gültiges Jahr ein (1917 oder später)',
            'invalid_threshold': 'Bitte geben Sie einen gültigen Mitglieder-Schwellenwert ein',
            'filter_window_title': 'Filtern & Suchen',
            'search_title_label': 'Titel suchen:',
            'min_members_label': 'Min. Mitglieder:',
            'genre_label': 'Genre:',
            'studio_label': 'Studio:',
            'apply_filter': 'Filter anwenden',
            'mal_data': 'MyAnimeList Daten',
            'nekopoi_data': 'Nekopoi Daten',
            'filtered_results': 'Gefilterte Ergebnisse: {mal} MAL, {nekopoi} Nekopoi',
            'seasons': ['winter', 'spring', 'summer', 'fall'],
            'season_names': ['Winter', 'Frühling', 'Sommer', 'Herbst'],
            'formats': ['txt', 'json', 'csv', 'pdf'],
            'format_names': ['Text (TXT)', 'JSON', 'CSV', 'PDF'],
            'scrape_options_label': 'Scraping-Optionen:',
            'no_source_selected': 'Bitte wählen Sie mindestens eine Datenquelle zum Scrapen aus',
            'mal_scrape_failed': 'MyAnimeList-Scraping ist fehlgeschlagen oder hat keine Daten zurückgegeben',
            'nekopoi_scrape_failed': 'Nekopoi-Scraping ist fehlgeschlagen oder hat keine Daten zurückgegeben',
            'data_usage_label': 'Datenverbrauch:',
            'scrape_mal_option': 'MyAnimeList',
            'scrape_nekopoi_option': 'Nekopoi',
            'scrape_both_option': 'Beide',
            'header_template_both': """{season} Hentai und normale Anime-Liste

{year}
Mitglied : {member}

Neueste Informationen :
Hinweis : Die Hentai-Anime, die ich nehme, kommen aus 2 Quellen, die klar zeigen, welcher zuerst veröffentlicht wird :v also trenne ich die Liste, damit du nicht verwirrt wirst. Ach ja, der Zeitplan in der ©KucingPeduli-Liste ist nur {nekopoi_month} Monate (mit {month_has_passed} Monaten vergangen, {ahead_text})

Gemeinsame Informationen für Hentai ©ListAnimeKu Anime-Liste :
- Veröffentlichungsdatum
> Hentai-Titel
^ Studio
! Hentai-Genre (ABSOLUT GEHEIM) Weil ich das Genre nicht kenne :v
+ Anzahl der Episoden (falls verfügbar)
~ Minuten pro Episode (falls verfügbar)

Gemeinsame Informationen für Hentai ©KucingPeduli Anime-Liste :
- Veröffentlichungsdatum
> Hentai-Titel
^ Studio
! Hentai-Genre (ABSOLUT GEHEIM) Weil ich das Genre nicht kenne :v
+ Zu veröffentlichende Episoden (Bedeutung welche Episode an diesem Datum in ©KucingPeduli veröffentlicht wird)

Gemeinsame Informationen für normale Anime-Liste :
- Veröffentlichungsdatum
> Anime-Titel
! Anime-Genre
+ Anzahl der Episoden (falls verfügbar)
~ Minuten pro Episode (falls verfügbar)

Gefährliches Anime-Genre:
Adl : Erwachsen
BL / Yao : Boys Love / Yaoi
Cro : Crossdressing
Ecc : Ecchi
Ero : Erotica
GL / Yur : Girls Love / Yuri
Hen : Hentai

Zusätzliche Info :
Wenn am Ende des Genres getrennt ist und hinter dem Genre ein ! (Ausrufezeichen) + fett steht, bedeutet das Vorsicht, weil das Genre bereits seltsam / pervers ist und normalerweise in "Danger Anime Genre" eingeht, also versuche zuerst zu lesen und gut zu verstehen" damit wenn etwas falsch ist nicht die Schuld des Admins / Empfehlers ist wenn du weiterhin diesen gefährlichen Genre-Anime ansiehst 🙂

Haftungsausschluss :
Alle normalen Anime-Listen und einige Hentai-Anime-Listen werden von ©ListAnimeKu genommen und einige Hentai-Anime-Listen werden von ©KucingPeduli genommen nicht alle anzeigenden Anime schreibe ich :v
Grundsätzlich nehme ich was ich interessant finde :v

Tools : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'header_template_mal': """𝙼𝚢𝙰𝚗𝚒𝚖𝚎𝙻𝚒𝚜𝚝 Hentai und normale Anime-Liste
{year}
Mitglied : {member}

Gemeinsame Informationen für Hentai ©ListAnimeKu Anime-Liste :
- Veröffentlichungsdatum
> Hentai-Titel
^ Studio
! Hentai-Genre (ABSOLUT GEHEIM) Weil ich das Genre nicht kenne :v
+ Anzahl der Episoden (falls verfügbar)
~ Minuten pro Episode (falls verfügbar)

Gemeinsame Informationen für normale Anime-Liste :
- Veröffentlichungsdatum
> Anime-Titel
! Anime-Genre
+ Anzahl der Episoden (falls verfügbar)
~ Minuten pro Episode (falls verfügbar)

Gefährliches Anime-Genre:
Adl : Erwachsen
BL / Yao : Boys Love / Yaoi
Cro : Crossdressing
Ecc : Ecchi
Ero : Erotica
GL / Yur : Girls Love / Yuri
Hen : Hentai

Zusätzliche Info :
Wenn am Ende des Genres getrennt ist und hinter dem Genre ein ! (Ausrufezeichen) + fett steht, bedeutet das Vorsicht, weil das Genre bereits seltsam / pervers ist und normalerweise in "Danger Anime Genre" eingeht, also versuche zuerst zu lesen und gut zu verstehen" damit wenn etwas falsch ist nicht die Schuld des Admins / Empfehlers ist wenn du weiterhin diesen gefährlichen Genre-Anime ansiehst 🙂

Haftungsausschluss :
Alle normalen Anime-Listen und Hentai Anime List sind genommen von ©ListAnimeKu

Tools : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'header_template_nekopoi': """𝙽𝚎𝚔𝚘𝙿𝚘𝚒 Hentai Anime-Liste
{first_month - last_month} {year}
Neueste Informationen :
Der Zeitplan in der ©KucingPeduli-Liste ist nur {nekopoi_month} Monate (mit {month_has_passed} Monaten vergangen, {ahead_text})

Gemeinsame Informationen für Hentai ©KucingPeduli Anime-Liste :
- Veröffentlichungsdatum
> Hentai-Titel
^ Studio
! Hentai-Genre (ABSOLUT GEHEIM) Weil ich das Genre nicht kenne :v
+ Zu veröffentlichende Episoden (Bedeutung welche Episode an diesem Datum in ©KucingPeduli veröffentlicht wird)

Tools : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'note_text': "HINWEIS : Der Zeitplan ist möglicherweise nicht vollständig, bitte warte auf Admin-Update\n",
            'last_update_text': "Letzte Aktualisierung : {nekopoi_last_update}\n\n",
            'no_anime_text': "\nKein Anime erfüllt die Kriterien\n",
            'hentai_list_title': "*Hentai-Anime-Liste ©ListAnimeKu*\n",
            'erotica_list_title': "*Erotica-Anime-Liste ©ListAnimeKu*\n",
            'normal_list_title': "*Normale Anime-Liste*\n",
            'none_text': "_*KEINE*_\n\n"
        }

        # Portuguese translations
        self.translations['pt'] = {
            'app_title': 'MyAnimeList & Nekopoi Scraper GUI',
            'year_label': 'Ano:',
            'season_label': 'Temporada:',
            'member_threshold_label': 'Limite de Membros:',
            'output_format_label': 'Formato de Saída:',
            'start_scraping': 'Iniciar Scraping',
            'save_results': 'Salvar Resultados',
            'filter_search': 'Filtrar & Buscar',
            'progress_title': 'Progresso',
            'results_title': 'Pré-visualização de Resultados',
            'ready_status': 'Pronto para scrapear...',
            'scraping_mal': 'Scrapeando MyAnimeList...',
            'scraping_nekopoi': 'Scrapeando Nekopoi...',
            'scraping_completed': 'Scraping concluído!',
            'error_title': 'Erro',
            'success_title': 'Sucesso',
            'warning_title': 'Aviso',
            'no_data_warning': 'Nenhum dado para salvar. Por favor, scrape primeiro.',
            'save_success': 'Resultados salvos em: {path}',
            'scraping_failed': 'Scraping falhou: {error}',
            'invalid_year': 'Por favor insira um ano válido (1917 ou posterior)',
            'invalid_threshold': 'Por favor insira um limite de membros válido',
            'filter_window_title': 'Filtrar & Buscar',
            'search_title_label': 'Buscar Título:',
            'min_members_label': 'Mín. Membros:',
            'genre_label': 'Gênero:',
            'studio_label': 'Estúdio:',
            'apply_filter': 'Aplicar Filtro',
            'mal_data': 'Dados do MyAnimeList',
            'nekopoi_data': 'Dados do Nekopoi',
            'filtered_results': 'Resultados Filtrados: {mal} MAL, {nekopoi} Nekopoi',
            'seasons': ['winter', 'spring', 'summer', 'fall'],
            'season_names': ['Inverno', 'Primavera', 'Verão', 'Outono'],
            'formats': ['txt', 'json', 'csv', 'pdf'],
            'format_names': ['Texto (TXT)', 'JSON', 'CSV', 'PDF'],
            'scrape_options_label': 'Opções de Scraping:',
            'no_source_selected': 'Por favor selecione pelo menos uma fonte de dados para scrapear',
            'mal_scrape_failed': 'O scraping do MyAnimeList falhou ou não retornou dados',
            'nekopoi_scrape_failed': 'O scraping do Nekopoi falhou ou não retornou dados',
            'data_usage_label': 'Uso de Dados:',
            'scrape_mal_option': 'MyAnimeList',
            'scrape_nekopoi_option': 'Nekopoi',
            'scrape_both_option': 'Ambos',
            'header_template_both': """{season} Lista de Anime Hentai e Normal

{year}
Membro : {member}

Últimas Informações :
Nota : Os animes hentai que eu pego vêm de 2 fontes, que claramente mostram qual será lançado primeiro :v então eu separo a lista para não te confundir. Ah sim, o cronograma na lista ©KucingPeduli é apenas {nekopoi_month} meses (com {month_has_passed} meses passados, {ahead_text})

Informações Comuns para a lista de Anime Hentai ©ListAnimeKu :
- Data de Lançamento
> Título Hentai
^ Estúdio
! Gênero Hentai (ABSOLUTAMENTE SECRETO) Porque eu não sei o gênero :v
+ Número de Episódios (se disponível)
~ Minutos por Episódio (se disponível)

Informações Comuns para a lista de Anime Hentai ©KucingPeduli :
- Data de Lançamento
> Título Hentai
^ Estúdio
! Gênero Hentai (ABSOLUTAMENTE SECRETO) Porque eu não sei o gênero :v
+ Episódios a serem lançados (Significado qual episódio será lançado nesta data em ©KucingPeduli)

Informações Comuns para a lista de Anime Normal :
- Data de Lançamento
> Título Anime
! Gênero Anime
+ Número de Episódios (se disponível)
~ Minutos por Episódio (se disponível)

Gênero de Anime Perigoso:
Adl : Adulto
BL / Yao : Boys Love / Yaoi
Cro : Crossdressing
Ecc : Ecchi
Ero : Erotica
GL / Yur : Girls Love / Yuri
Hen : Hentai

Informação Adicional :
Se no final do gênero estiver separado e atrás do gênero houver um sinal ! (ponto de exclamação) + negrito, significa cuidado porque o gênero já é estranho / pervertido e normalmente entra em "Danger Anime Genre", então tente ler primeiro e entender bem" para que se houver algo errado não seja culpa do Admin / recomendador se você continuar assistindo aquele anime de gênero perigoso 🙂

Isenção de Responsabilidade :
Todas as listas de Anime Normal e Algumas Listas de Anime Hentai são tiradas de ©ListAnimeKu e Algumas Listas de Anime Hentai são tiradas de ©KucingPeduli não escrevo todos os animes que aparecem :v
Básicamente eu pego o que acho interessante :v

Ferramentas : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'header_template_mal': """𝙼𝚢𝙰𝚗𝚒𝚖𝚎𝙻𝚒𝚜𝚝 Lista de Anime Hentai e Normal
{year}
Membro : {member}

Informações Comuns para a lista de Anime Hentai ©ListAnimeKu :
- Data de Lançamento
> Título Hentai
^ Estúdio
! Gênero Hentai (ABSOLUTAMENTE SECRETO) Porque eu não sei o gênero :v
+ Número de Episódios (se disponível)
~ Minutos por Episódio (se disponível)

Informações Comuns para a lista de Anime Normal :
- Data de Lançamento
> Título Anime
! Gênero Anime
+ Número de Episódios (se disponível)
~ Minutos por Episódio (se disponível)

Gênero de Anime Perigoso:
Adl : Adulto
BL / Yao : Boys Love / Yaoi
Cro : Crossdressing
Ecc : Ecchi
Ero : Erotica
GL / Yur : Girls Love / Yuri
Hen : Hentai

Informação Adicional :
Se no final do gênero estiver separado e atrás do gênero houver um sinal ! (ponto de exclamação) + negrito, significa cuidado porque o gênero já é estranho / pervertido e normalmente entra em "Danger Anime Genre", então tente ler primeiro e entender bem" para que se houver algo errado não seja culpa do Admin / recomendador se você continuar assistindo aquele anime de gênero perigoso 🙂

Isenção de Responsabilidade :
Todas as listas de Anime Normal e Hentai Anime List são tiradas de ©ListAnimeKu

Ferramentas : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'header_template_nekopoi': """𝙽𝚎𝚔𝚘𝙿𝚘𝚒 Lista de Anime Hentai
{first_month - last_month} {year}
Últimas Informações :
O cronograma na lista ©KucingPeduli é apenas {nekopoi_month} meses (com {month_has_passed} meses passados, {ahead_text})

Informações Comuns para a lista de Anime Hentai ©KucingPeduli :
- Data de Lançamento
> Título Hentai
^ Estúdio
! Gênero Hentai (ABSOLUTAMENTE SECRETO) Porque eu não sei o gênero :v
+ Episódios a serem lançados (Significado qual episódio será lançado nesta data em ©KucingPeduli)

Ferramentas : https://github.com/TheKingTermux/myanimelist-nekopoi-scrapper
\n\n""",
            'note_text': "NOTA : O cronograma pode não estar completo, por favor aguarde a atualização do admin\n",
            'last_update_text': "Última Atualização : {nekopoi_last_update}\n\n",
            'no_anime_text': "\nNenhum anime atende aos critérios\n",
            'hentai_list_title': "*Lista de Anime Hentai ©ListAnimeKu*\n",
            'erotica_list_title': "*Lista de Anime Erótica ©ListAnimeKu*\n",
            'normal_list_title': "*Lista de Anime Normal*\n",
            'none_text': "_*NENHUM*_\n\n"
        }

    def set_language(self, lang):
        """Set current language"""
        if lang in self.translations:
            self.current_lang = lang
            return True
        return False

    def get(self, key, **kwargs):
        """Get translated text"""
        if self.current_lang in self.translations and key in self.translations[self.current_lang]:
            text = self.translations[self.current_lang][key]
            if kwargs:
                text = text.format(**kwargs)
            return text
        return key  # Return key if translation not found

    def get_available_languages(self):
        """Get list of available languages"""
        return list(self.translations.keys())

    def get_language_name(self, lang_code):
        """Get human-readable language name"""
        names = {
            'id': 'Bahasa Indonesia',
            'en': 'English',
            'ja': '日本語 (Japanese)',
            'es': 'Español (Spanish)',
            'zh': '中文 (Chinese)',
            'ko': '한국어 (Korean)',
            'fr': 'Français (French)',
            'de': 'Deutsch (German)',
            'pt': 'Português (Portuguese)'
        }
        return names.get(lang_code, lang_code)

# Global instance
i18n = Localization()
            
