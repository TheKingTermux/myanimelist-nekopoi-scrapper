import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import json
import csv
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import logging
import random

# Import existing functions from the main script
from MyAnimeList_and_Nekopoi_Scrapper import (
    scrape_mal_seasonal, scrape_nekopoi, save_to_file, translate_month,
    parse_date_flexible, parse_member_count, get_anime_data, loading_animation,
    print_status, tampilkan_header, DANGER_GENRES, EPS_REGEX, DURATION_REGEX
)

# Import localization
from localization import i18n

# Import localization
from localization import i18n

class AnimeScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(i18n.get('app_title'))
        self.root.geometry("800x700")
        self.current_lang = 'id'  # Default language

        # Variables
        self.year_var = tk.StringVar(value=str(datetime.now().year))
        self.season_var = tk.StringVar(value="fall")
        self.member_threshold_var = tk.StringVar(value="10000")
        self.output_format_var = tk.StringVar(value="txt")
        self.scraped_data = {}
        self.nekopoi_data = {}
        self.nekopoi_last_update = "Unknown"
        self.categories = {}

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Language selector
        lang_frame = ttk.Frame(self.root, padding="5")
        lang_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        ttk.Label(lang_frame, text="Language / Bahasa:").grid(row=0, column=0, sticky=tk.W)
        self.lang_var = tk.StringVar(value=self.current_lang)
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var,
                                 values=[f"{lang} - {i18n.get_language_name(lang)}" for lang in i18n.get_available_languages()],
                                 state="readonly", width=15)
        lang_combo.grid(row=0, column=1, sticky=tk.W)
        lang_combo.bind('<<ComboboxSelected>>', self.change_language)

        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Input section
        input_frame = ttk.LabelFrame(main_frame, text=i18n.get('input_parameters', default="Input Parameters"), padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        # Year
        ttk.Label(input_frame, text=i18n.get('year_label')).grid(row=0, column=0, sticky=tk.W, pady=2)
        year_entry = ttk.Entry(input_frame, textvariable=self.year_var, width=10)
        year_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        # Season
        ttk.Label(input_frame, text=i18n.get('season_label')).grid(row=1, column=0, sticky=tk.W, pady=2)
        season_combo = ttk.Combobox(input_frame, textvariable=self.season_var,
                                   values=i18n.get('season_names'), state="readonly", width=10)
        season_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2)

        # Member Threshold
        ttk.Label(input_frame, text=i18n.get('member_threshold_label')).grid(row=2, column=0, sticky=tk.W, pady=2)
        threshold_entry = ttk.Entry(input_frame, textvariable=self.member_threshold_var, width=10)
        threshold_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2)

        # Output Format
        ttk.Label(input_frame, text=i18n.get('output_format_label')).grid(row=3, column=0, sticky=tk.W, pady=2)
        format_combo = ttk.Combobox(input_frame, textvariable=self.output_format_var,
                                   values=i18n.get('format_names'), state="readonly", width=10)
        format_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2)

        # Scrape Options
        ttk.Label(input_frame, text=i18n.get('scrape_options_label', default="Scrape Options:")).grid(row=4, column=0, sticky=tk.W, pady=2)
        self.scrape_option_var = tk.StringVar(value=i18n.get('scrape_both_option') if self.current_lang == 'id' else i18n.get('scrape_mal_option'))
        self.scrape_combo = ttk.Combobox(input_frame, textvariable=self.scrape_option_var,
                                        values=[i18n.get('scrape_mal_option'), i18n.get('scrape_nekopoi_option'), i18n.get('scrape_both_option')],
                                        state="readonly", width=10)
        self.scrape_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        self.scrape_button = ttk.Button(button_frame, text=i18n.get('start_scraping'), command=self.start_scraping)
        self.scrape_button.grid(row=0, column=0, padx=(0, 5))

        self.save_button = ttk.Button(button_frame, text=i18n.get('save_results'), command=self.save_results, state=tk.DISABLED)
        self.save_button.grid(row=0, column=1, padx=(0, 5))

        self.filter_button = ttk.Button(button_frame, text=i18n.get('filter_search'), command=self.open_filter_window, state=tk.DISABLED)
        self.filter_button.grid(row=0, column=2)

        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text=i18n.get('progress_title'), padding="10")
        progress_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        self.progress_var = tk.StringVar(value=i18n.get('ready_status'))
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))

        # Data usage display
        self.data_usage_var = tk.StringVar(value=i18n.get('data_usage_label', default="Data Usage: 0 KB"))
        self.data_usage_label = ttk.Label(progress_frame, textvariable=self.data_usage_var)
        self.data_usage_label.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 0))

        # Results section
        results_frame = ttk.LabelFrame(main_frame, text=i18n.get('results_title'), padding="10")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, height=15)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)

    def start_scraping(self):
        # Validate inputs
        try:
            year = int(self.year_var.get())
            if year < 1917 or year > datetime.now().year + 1:
                raise ValueError("Invalid year")
        except ValueError:
            messagebox.showerror(i18n.get('error_title'), i18n.get('invalid_year'))
            return

        try:
            threshold = int(self.member_threshold_var.get())
            if threshold < 0:
                raise ValueError("Invalid threshold")
        except ValueError:
            messagebox.showerror(i18n.get('error_title'), i18n.get('invalid_threshold'))
            return

        # Disable buttons and start progress
        self.scrape_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.progress_var.set(i18n.get('scraping_mal'))

        # Run scraping in separate thread
        threading.Thread(target=self.scrape_data, daemon=True).start()

    def scrape_data(self):
        try:
            year = int(self.year_var.get())
            season = self.season_var.get()
            threshold = int(self.member_threshold_var.get())
            option = self.scrape_option_var.get()
            scrape_mal = option == i18n.get('scrape_mal_option') or option == i18n.get('scrape_both_option')
            scrape_nekopoi = option == i18n.get('scrape_nekopoi_option') or option == i18n.get('scrape_both_option')

            anime_data = {}
            nekopoi_data = {}
            nekopoi_last_update = "Unknown"
            categories = {}

            # Scrape MAL if selected
            if scrape_mal:
                # Construct URL
                url = f"https://myanimelist.net/anime/season/{year}/{season}"

                # Scrape MAL
                self.progress_var.set(i18n.get('scraping_mal'))
                anime_data, categories = scrape_mal_seasonal(url)

            # Scrape Nekopoi if selected
            if scrape_nekopoi:
                self.progress_var.set(i18n.get('scraping_nekopoi'))
                nekopoi_data, nekopoi_last_update = scrape_nekopoi()

            # Validate that at least one source was selected
            if not scrape_mal and not scrape_nekopoi:
                raise Exception(i18n.get('no_source_selected', default="Please select at least one data source to scrape"))

            # Store data
            self.scraped_data = anime_data
            self.nekopoi_data = nekopoi_data
            self.nekopoi_last_update = nekopoi_last_update
            self.categories = categories

            # Update GUI with data usage
            self.root.after(0, self.update_data_usage)
            self.root.after(0, self.update_results_preview)

            self.progress_var.set(i18n.get('scraping_completed'))
            self.root.after(0, lambda: self.scrape_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.save_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.filter_button.config(state=tk.NORMAL))

        except Exception as e:
            self.progress_var.set(f"{i18n.get('error_title')}: {str(e)}")
            self.root.after(0, lambda: self.scrape_button.config(state=tk.NORMAL))
            messagebox.showerror(i18n.get('error_title'), i18n.get('scraping_failed', error=str(e)))

        finally:
            self.root.after(0, self.progress_bar.stop)

    def update_results_preview(self):
        self.results_text.delete(1.0, tk.END)

        mal_count = sum(len(v) for v in self.scraped_data.values()) if self.scraped_data else 0
        nekopoi_count = sum(len(v) for v in self.nekopoi_data.values()) if self.nekopoi_data else 0

        preview = f"MyAnimeList: {mal_count} entries\nNekopoi: {nekopoi_count} entries\n\n"

        # Show sample entries
        if self.scraped_data:
            preview += "Sample MAL entries:\n"
            for date, animes in list(self.scraped_data.items())[:3]:
                for anime in animes[:2]:
                    preview += f"- {anime['title']} ({date})\n"
                break

        if self.nekopoi_data:
            preview += "\nSample Nekopoi entries:\n"
            for date, entries in list(self.nekopoi_data.items())[:2]:
                for entry in entries[:2]:
                    preview += f"- {entry['title']} ({date})\n"

        self.results_text.insert(tk.END, preview)

    def update_data_usage(self):
        """Update the data usage display"""
        try:
            # Read current data usage from file
            data_usage_file = os.path.join(os.path.dirname(__file__), 'data_usage.txt')
            if os.path.exists(data_usage_file):
                with open(data_usage_file, 'r') as f:
                    total_bytes = int(f.read().strip())
            else:
                total_bytes = 0

            # Calculate session usage (this would need to be tracked separately in GUI)
            # For now, just show total usage
            total_kb = total_bytes // 1024
            if total_kb >= 1024:
                total_mb = total_kb / 1024
                usage_str = f"{total_mb:.2f} MB"
            else:
                usage_str = f"{total_kb} KB"

            self.data_usage_var.set(f"{i18n.get('data_usage_label', default='Data Usage:')} {usage_str}")

        except Exception as e:
            self.data_usage_var.set(f"{i18n.get('data_usage_label', default='Data Usage:')} Unknown")

    def save_results(self):
        if not self.scraped_data and not self.nekopoi_data:
            messagebox.showwarning(i18n.get('warning_title'), i18n.get('no_data_warning'))
            return

        # Check if user selected sources but no data was scraped
        option = self.scrape_option_var.get()
        scrape_mal = option == i18n.get('scrape_mal_option') or option == i18n.get('scrape_both_option')
        scrape_nekopoi = option == i18n.get('scrape_nekopoi_option') or option == i18n.get('scrape_both_option')

        if scrape_mal and not self.scraped_data:
            messagebox.showwarning(i18n.get('warning_title'), i18n.get('mal_scrape_failed', default="MyAnimeList scraping failed or returned no data"))
            return

        if scrape_nekopoi and not self.nekopoi_data:
            messagebox.showwarning(i18n.get('warning_title'), i18n.get('nekopoi_scrape_failed', default="Nekopoi scraping failed or returned no data"))
            return

        # Get output path
        format_ext = self.output_format_var.get()
        season_english = self.season_var.get().capitalize()
        year_str = self.year_var.get()
        threshold = int(self.member_threshold_var.get())
        default_name = f"{season_english}{year_str}.{format_ext}"
        if threshold != 10000:
            threshold_str = f"{threshold // 1000}K" if threshold % 1000 == 0 else str(threshold)
            default_name = default_name.replace(f".{format_ext}", f"Member{threshold_str}.{format_ext}")

        # Default to AnimeList folder like main script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, "AnimeList")
        os.makedirs(output_dir, exist_ok=True)

        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{format_ext}",
            filetypes=[(f"{format_ext.upper()} files", f"*.{format_ext}"), ("All files", "*.*")],
            initialfile=default_name,
            initialdir=output_dir
        )

        if not file_path:
            return

        try:
            threshold = int(self.member_threshold_var.get())
            year = int(self.year_var.get())
            season_name = {"winter": "Musim Dingin", "spring": "Semi", "summer": "Panas", "fall": "Gugur"}.get(self.season_var.get(), self.season_var.get())

            # Determine header template based on scrape option
            option = self.scrape_option_var.get()
            if option == i18n.get('scrape_both_option'):
                template_key = 'header_template_both'
            elif option == i18n.get('scrape_mal_option'):
                template_key = 'header_template_mal'
            elif option == i18n.get('scrape_nekopoi_option'):
                template_key = 'header_template_nekopoi'
            else:
                template_key = 'header_template_both'  # default
            header_template = i18n.get(template_key)

            # Only pass Nekopoi data if it was scraped
            scrape_mal = option == i18n.get('scrape_mal_option') or option == i18n.get('scrape_both_option')
            scrape_nekopoi = option == i18n.get('scrape_nekopoi_option') or option == i18n.get('scrape_both_option')
            nekopoi_data = self.nekopoi_data if scrape_nekopoi else {}
            nekopoi_last_update = self.nekopoi_last_update if scrape_nekopoi else "Unknown"

            if format_ext == "txt":
                save_to_file(self.scraped_data, self.categories, file_path, threshold,
                            nekopoi_data, nekopoi_last_update, year, season_name, str(year), header_template)
            elif format_ext == "json":
                self.save_as_json(file_path)
            elif format_ext == "csv":
                self.save_as_csv(file_path)
            elif format_ext == "pdf":
                self.save_as_pdf(file_path)

            messagebox.showinfo(i18n.get('success_title'), i18n.get('save_success', path=file_path))

        except Exception as e:
            messagebox.showerror(i18n.get('error_title'), i18n.get('scraping_failed', error=str(e)))

    def save_as_json(self, file_path):
        data = {
            "mal_data": self.scraped_data,
            "nekopoi_data": self.nekopoi_data,
            "nekopoi_last_update": self.nekopoi_last_update,
            "categories": self.categories
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_as_csv(self, file_path):
        rows = []
        # MAL data
        for date, animes in self.scraped_data.items():
            for anime in animes:
                rows.append({
                    "source": "MAL",
                    "date": date,
                    "title": anime.get("title", ""),
                    "members": anime.get("members", 0),
                    "eps": anime.get("eps", ""),
                    "duration": anime.get("duration", ""),
                    "studio": anime.get("studio", ""),
                    "genres": ", ".join(anime.get("genres", [])),
                    "themes": ", ".join(anime.get("themes", [])),
                    "demographics": ", ".join(anime.get("demographics", [])),
                    "category": anime.get("category", "")
                })

        # Nekopoi data
        for date, entries in self.nekopoi_data.items():
            for entry in entries:
                rows.append({
                    "source": "Nekopoi",
                    "date": date,
                    "title": entry.get("title", ""),
                    "episodes": entry.get("episodes", ""),
                    "studio": entry.get("studio", ""),
                    "members": "",
                    "eps": "",
                    "duration": "",
                    "genres": "",
                    "themes": "",
                    "demographics": "",
                    "category": ""
                })

        if rows:
            df = pd.DataFrame(rows)
            df.to_csv(file_path, index=False, encoding='utf-8')

    def save_as_pdf(self, file_path):
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        y_position = height - 50
        c.setFont("Helvetica", 12)

        # Title
        c.drawString(50, y_position, f"Anime Scraper Results - {self.season_var.get().capitalize()} {self.year_var.get()}")
        y_position -= 30

        # MAL data
        if self.scraped_data:
            c.drawString(50, y_position, "MyAnimeList Data:")
            y_position -= 20
            for date, animes in list(self.scraped_data.items())[:10]:  # Limit to avoid overflow
                for anime in animes[:5]:
                    if y_position < 50:
                        c.showPage()
                        y_position = height - 50
                    c.drawString(50, y_position, f"- {anime['title']} ({date})")
                    y_position -= 15

        # Nekopoi data
        if self.nekopoi_data:
            if y_position < 100:
                c.showPage()
                y_position = height - 50
            c.drawString(50, y_position, "Nekopoi Data:")
            y_position -= 20
            for date, entries in list(self.nekopoi_data.items())[:5]:
                for entry in entries[:3]:
                    if y_position < 50:
                        c.showPage()
                        y_position = height - 50
                    c.drawString(50, y_position, f"- {entry['title']} ({date})")
                    y_position -= 15

        c.save()


    def open_filter_window(self):
        if not self.scraped_data and not self.nekopoi_data:
            messagebox.showwarning(i18n.get('warning_title'), i18n.get('no_data_warning'))
            return

        filter_window = tk.Toplevel(self.root)
        filter_window.title(i18n.get('filter_window_title'))
        filter_window.geometry("600x500")

        # Filter controls
        control_frame = ttk.Frame(filter_window, padding="10")
        control_frame.pack(fill=tk.X)

        ttk.Label(control_frame, text=i18n.get('search_title_label')).grid(row=0, column=0, sticky=tk.W)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(control_frame, textvariable=search_var, width=20)
        search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        ttk.Label(control_frame, text=i18n.get('min_members_label')).grid(row=1, column=0, sticky=tk.W)
        min_members_var = tk.StringVar()
        min_members_entry = ttk.Entry(control_frame, textvariable=min_members_var, width=10)
        min_members_entry.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(control_frame, text=i18n.get('genre_label')).grid(row=2, column=0, sticky=tk.W)
        genre_var = tk.StringVar()
        genre_combo = ttk.Combobox(control_frame, textvariable=genre_var, width=15)
        # Collect all unique genres
        all_genres = set()
        for animes in self.scraped_data.values():
            for anime in animes:
                all_genres.update(anime.get("genres", []))
        genre_combo['values'] = sorted(list(all_genres))
        genre_combo.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(control_frame, text=i18n.get('studio_label')).grid(row=3, column=0, sticky=tk.W)
        studio_var = tk.StringVar()
        studio_combo = ttk.Combobox(control_frame, textvariable=studio_var, width=15)
        # Collect all unique studios
        all_studios = set()
        for animes in self.scraped_data.values():
            for anime in animes:
                studio = anime.get("studio", "")
                if studio:
                    all_studios.add(studio)
        for entries in self.nekopoi_data.values():
            for entry in entries:
                studio = entry.get("studio", "")
                if studio:
                    all_studios.add(studio)
        studio_combo['values'] = sorted(list(all_studios))
        studio_combo.grid(row=3, column=1, sticky=tk.W)

        # Results
        results_frame = ttk.Frame(filter_window)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD)
        results_text.pack(fill=tk.BOTH, expand=True)

        def apply_filter():
            results_text.delete(1.0, tk.END)

            search_term = search_var.get().lower()
            min_members = int(min_members_var.get()) if min_members_var.get().isdigit() else 0
            selected_genre = genre_var.get()
            selected_studio = studio_var.get()

            filtered_mal = []
            filtered_nekopoi = []

            # Filter MAL data
            for date, animes in self.scraped_data.items():
                for anime in animes:
                    if (search_term in anime.get("title", "").lower() and
                        anime.get("members", 0) >= min_members and
                        (not selected_genre or selected_genre in anime.get("genres", [])) and
                        (not selected_studio or selected_studio == anime.get("studio", ""))):
                        filtered_mal.append((date, anime))

            # Filter Nekopoi data
            for date, entries in self.nekopoi_data.items():
                for entry in entries:
                    if (search_term in entry.get("title", "").lower() and
                        (not selected_studio or selected_studio == entry.get("studio", ""))):
                        filtered_nekopoi.append((date, entry))

            # Display results
            results_text.insert(tk.END, i18n.get('filtered_results', mal=len(filtered_mal), nekopoi=len(filtered_nekopoi)) + "\n\n")

            if filtered_mal:
                results_text.insert(tk.END, i18n.get('mal_data') + ":\n")
                for date, anime in filtered_mal[:20]:  # Limit display
                    results_text.insert(tk.END, f"- {anime['title']} ({date}) - {anime.get('members', 0)} members\n")

            if filtered_nekopoi:
                results_text.insert(tk.END, "\n" + i18n.get('nekopoi_data') + ":\n")
                for date, entry in filtered_nekopoi[:20]:
                    results_text.insert(tk.END, f"- {entry['title']} ({date})\n")

        filter_button = ttk.Button(control_frame, text=i18n.get('apply_filter'), command=apply_filter)
        filter_button.grid(row=4, column=0, columnspan=2, pady=10)

        control_frame.columnconfigure(1, weight=1)

    def change_language(self, event=None):
        """Change the application language"""
        selected = self.lang_var.get()
        if selected:
            lang_code = selected.split(' - ')[0]
            if i18n.set_language(lang_code):
                self.current_lang = lang_code
                # Update scrape options
                self.scrape_combo['values'] = [i18n.get('scrape_mal_option'), i18n.get('scrape_nekopoi_option'), i18n.get('scrape_both_option')]
                self.scrape_option_var.set(i18n.get('scrape_both_option') if lang_code == 'id' else i18n.get('scrape_mal_option'))
                self.refresh_ui_texts()

    def refresh_ui_texts(self):
        """Refresh all UI text elements with new language"""
        self.root.title(i18n.get('app_title'))
        # Update all text elements that use i18n
        # Note: This is a simplified refresh - in a full implementation,
        # you'd need to update all labels, buttons, etc. dynamically

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimeScraperGUI(root)
    root.mainloop()
