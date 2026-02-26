"""
Scraper for aravot.am news categories.
Stores category-title pairs into a CSV file.
"""


# Imports
from bs4 import BeautifulSoup
import requests
import random
import time
import csv
import os
import re


# -----------------------------
# CONSTANTS
# -----------------------------
HEADER_ROTATION = 100 # Rotate User-Agent every 100 pages to avoid blocks
SESSION_ROTATION = 400 # Refresh requests session every 400 pages to reduce server detection
MAX_EMPTY_PAGES = 3 # Stop scraping category after this many empty pages
CSV_FILE = "data/news.csv"


# Mapping categories to their base URLs
CATEGORY_URLS = {
    "Politics": "https://www.aravot.am/category/news/politics/page/",
    "Rights": "https://www.aravot.am/category/news/rights/page/",
    "Education": "https://www.aravot.am/category/news/education/page/",
    "Sport": "https://www.aravot.am/category/news/sport/page/",
}

# List of User-Agent strings for rotation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh)",
    "Mozilla/5.0 (Android 11)",
    "Mozilla/5.0 (iPhone)"
]


# -----------------------------
# FUNCTIONS
# -----------------------------
def random_header() -> dict:
    """Return a random User-Agent header to avoid blocks."""
    return {"User-Agent": random.choice(user_agents)}

def new_session(headers: dict) -> requests.Session:
    """Create a fresh session with headers applied."""
    session = requests.Session()
    session.headers.update(headers)
    return session

def clean_titles(titles: list[str]) -> list[str]:
    """Clean list of titles, keeping Armenian & English letters and spaces."""
    cleaned = []
    for title in titles:
        title = re.sub(r'[^a-zA-ZԱ-Ֆա-ֆ\s]+', '', title).strip()
        if title:
            cleaned.append(title)
    return cleaned

def extract_titles(soup: BeautifulSoup) -> list[str]:
    """Extract raw titles from the HTML soup."""
    # "cass" is the actual class name used on the site
    container = soup.find("div", attrs={"cass": "category_items"})
    if not container:
        return []
    return [a.get_text(strip=True) for a in container.find_all("a")]


# -----------------------------
# CSV SETUP
# -----------------------------
file_exists = os.path.isfile(CSV_FILE)
csv_file = open(CSV_FILE, "a", newline="", encoding="utf-8")
writer = csv.writer(csv_file)

# Write header only if CSV didn't exist
if not file_exists:
    writer.writerow(['Category', "Title"])
    csv_file.flush()


# -----------------------------
# MAIN SCRAPING LOOP
# -----------------------------
session = requests.Session()
headers = random_header()

try:
    for category, base_url in CATEGORY_URLS.items():
        print(f"\nScraping category: {category}")
        start_page = 2 # Pages start at 2; site has no page 1
        consecutive_empty_pages = 0
        
        while True:
            if consecutive_empty_pages >= MAX_EMPTY_PAGES:
                print(f'End of the category: {category}')
                break

            # Rotate User-Agent periodically
            if start_page % HEADER_ROTATION == 0:
                headers = random_header()
                session.headers.update(headers)

            # Refresh session periodically
            if start_page % SESSION_ROTATION == 0:
                session.close()
                session = new_session(headers)

            url = f"{base_url}{start_page}"

            try:
                response = session.get(url, headers=headers, timeout=15)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f'Request failed for page {start_page}: {e}')
                consecutive_empty_pages += 1
                start_page += 1
                continue

            print(url, "-", response.status_code)

            soup = BeautifulSoup(response.text, "lxml")
            raw_titles = extract_titles(soup)
            titles = clean_titles(raw_titles)

            if response.status_code != 200:
                print(f'Skipping page: {start_page}')
                consecutive_empty_pages += 1
                start_page += 1    
                continue
            else:
                consecutive_empty_pages = 0
                for title in titles:
                    writer.writerow([category, title])
                csv_file.flush()

            start_page += 1
            time.sleep(random.uniform(0.1, 0.3)) # Polite scraping

except KeyboardInterrupt:
    print("\nCtrl+C detected — saving progress safely...")

finally:
    csv_file.close()
    session.close()
    print("CSV closed safely. You can resume anytime.")