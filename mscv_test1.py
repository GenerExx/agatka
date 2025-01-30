import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import logging

# Konfiguracja logowania
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Logowanie do konsoli
    ]
)

# URL strony, którą chcesz sprawdzić
URLBase = "https://grojec.esesja.pl"
URL = urljoin(URLBase, "/transmisje_z_obrad_rady")

def fetch_page(url):
    """Pobiera stronę i zwraca kod HTML"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        logging.debug(f"Kodowanie odpowiedzi: {response.encoding}")
        response.encoding = 'utf-8'
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Błąd podczas pobierania strony: {e}")
        return None

def extract_date_from_text(text):
    """Wyodrębnia datę z tekstu i zwraca ją jako obiekt datetime"""
    date_pattern = r"(\d{1,2})\s(stycznia|lutego|marca|kwietnia|maja|czerwca|lipca|sierpnia|września|października|listopada|grudnia)\s(\d{4})"
    month_mapping = {
        "stycznia": 1, "lutego": 2, "marca": 3, "kwietnia": 4, "maja": 5,
        "czerwca": 6, "lipca": 7, "sierpnia": 8, "września": 9,
        "października": 10, "listopada": 11, "grudnia": 12
    }
    
    match = re.search(date_pattern, text)
    if match:
        day, month_name, year = match.groups()
        month = month_mapping[month_name]
        return datetime(int(year), month, int(day))
    return None

def parse_html(html):
    """Parsuje HTML i wyświetla podstawowe informacje"""
    soup = BeautifulSoup(html, 'html.parser')

    # Linki
    logging.info("=== Linki na stronie ===")
    for link in soup.find_all('a', string=re.compile(r'\bSesja\b', re.IGNORECASE)):
        href = link.get('href')
        text = link.get_text(strip=True)
        if href:
            full_url = urljoin(URLBase, href)
            logging.debug(f"Tekst: {text}, URL: {full_url}")

            # Wyodrębnianie daty z tekstu
            date = extract_date_from_text(text)
            if date:
                logging.info(f"  → Wyodrębniona data: {date.strftime('%Y-%m-%d')}")
            else:
                logging.warning("  → Brak daty w tekście")
        else:
            logging.warning(f"Link bez atrybutu href: {link}")

def main():
    logging.info(f"Pobieranie strony {URL}...")
    html = fetch_page(URL)
    if html:
        logging.info("=== Parsowanie treści ===")
        parse_html(html)
    else:
        logging.error("Nie udało się pobrać strony.")

if __name__ == "__main__":
    main()
