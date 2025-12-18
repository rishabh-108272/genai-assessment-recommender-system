import requests
from bs4 import BeautifulSoup as bs
import json
import time

# --- Configuration ---
BASE_URL = "https://www.shl.com/products/product-catalog/"
PAGINATION_URL_TEMPLATE = BASE_URL + "?start={}&type=1" 
TOTAL_PAGES = 32 
START_PAGE = 20  # Set this to the page where it crashed
REQUEST_DELAY = 2  # Increased delay to be gentler on the server
DETAIL_DELAY = 1   
MAX_RETRIES = 3    # Number of times to retry a failed request

TEST_TYPE_MAP = {
    "A": "Ability & Aptitude", "B": "Biodata & Situational Judgement",
    "C": "Competencies", "D": "Development & 360",
    "E": "Assessment Exercises", "K": "Knowledge & Skills",
    "P": "Personality & Behavior", "S": "Simulations"
}

def scrape_product_details(session, url):
    """Fetches details with a retry mechanism and longer timeout."""
    for attempt in range(MAX_RETRIES):
        try:
            # Increased timeout to 30 seconds
            r = session.get(url, timeout=30)
            r.raise_for_status()
            soup = bs(r.content, "html.parser")

            desc_header = soup.find('h4', string=lambda t: t and 'Description' in t)
            description = desc_header.find_next('p').get_text(strip=True) if desc_header else "N/A"

            duration_header = soup.find('h4', string=lambda t: t and 'Assessment length' in t)
            duration = duration_header.find_next('p').get_text(strip=True) if duration_header else "N/A"
            
            if "=" in duration:
                duration = duration.split('=')[-1].strip() + " minutes"

            return description, duration
        except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
            print(f"    ! Attempt {attempt + 1} failed for {url}: {e}")
            time.sleep(2 ** attempt) # Exponential backoff (wait 2s, then 4s...)
    
    return "Timeout/Error", "Timeout/Error"

def parse_test_row(row, test_type_map):
    cols = row.find_all('td', class_='custom__table-heading__general')
    if len(cols) < 3: return None

    title_col = row.find('td', class_='custom__table-heading__title')
    link_tag = title_col.find('a')
    test_name = link_tag.get_text(strip=True) if link_tag else title_col.get_text(strip=True)
    
    test_link_relative = link_tag.get('href') if link_tag else ''
    test_link = "https://www.shl.com" + test_link_relative if test_link_relative.startswith('/') else test_link_relative

    remote_testing = 'Yes' if cols[0].find('span', class_='catalogue__circle -yes') else 'No'
    adaptive_irt = 'Yes' if cols[1].find('span', class_='catalogue__circle -yes') else 'No'
    test_type_spans = cols[2].find_all('span', class_='product-catalogue__key')
    test_types_list = [test_type_map.get(span.get_text(strip=True), "Unknown") for span in test_type_spans]
        
    return {'Test Solution': test_name, 'URL': test_link, 'Remote Testing': remote_testing, 
            'Adaptive/IRT': adaptive_irt, 'Test Type(s)': test_types_list}

def crawl_shl_with_resume():
    # Load existing data to append to it
    try:
        with open("shl_detailed_catalog.json", "r", encoding="utf-8") as f:
            all_data = json.load(f)
            print(f"Loaded {len(all_data)} existing records.")
    except FileNotFoundError:
        all_data = []

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})

    # Start from the page where it left off
    for page in range(START_PAGE, TOTAL_PAGES + 1):
        start_value = 12 * (page - 1)
        url = BASE_URL if page == 1 else PAGINATION_URL_TEMPLATE.format(start_value)
        
        print(f"\n--- Scraping Page {page} (Start Index: {start_value}) ---")
        try:
            r = session.get(url, timeout=30)
            soup = bs(r.content, "html.parser")
            tables = soup.find_all(class_="custom__table-responsive")
            target_table = tables[1] if page == 1 and len(tables) > 1 else tables[0]
            data_rows = target_table.find_all('tr', attrs={'data-entity-id': True})

            for row in data_rows:
                basic_info = parse_test_row(row, TEST_TYPE_MAP)
                if basic_info:
                    print(f"  > Processing: {basic_info['Test Solution']}")
                    desc, dur = scrape_product_details(session, basic_info['URL'])
                    basic_info['Description'] = desc
                    basic_info['Duration'] = dur
                    all_data.append(basic_info)
                    time.sleep(DETAIL_DELAY)

            # Save progress after every page in case of another crash
            with open("shl_detailed_catalog.json", "w", encoding="utf-8") as f:
                json.dump(all_data, f, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"Error on page {page}: {e}. Try running again starting from this page.")
            break
            
        time.sleep(REQUEST_DELAY)

    print(f"\nProcess finished. Total records in file: {len(all_data)}")

if __name__ == "__main__":
    crawl_shl_with_resume()