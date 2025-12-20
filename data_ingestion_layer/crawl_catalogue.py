import requests
from bs4 import BeautifulSoup as bs
import json
import time

# --- Configuration ---
BASE_URL = "https://www.shl.com/products/product-catalog/"
PAGINATION_URL_TEMPLATE = BASE_URL + "?start={}&type=1" 
TOTAL_PAGES = 32 
REQUEST_DELAY = 2
DETAIL_DELAY = 1 # Small delay between page requests

TEST_TYPE_MAP = {
    "A": "Ability & Aptitude",
    "B": "Biodata & Situational Judgement",
    "C": "Competencies",
    "D": "Development & 360",
    "E": "Assessment Exercises",
    "K": "Knowledge & Skills",
    "P": "Personality & Behavior",
    "S": "Simulations"
}

# --- New Function: Scrape Individual Product Page ---
def scrape_product_details(session, url):
    """
    Navigates to the product detail page to extract Description and Duration.
    """
    if not url:
        return "N/A", "N/A"
    
    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
        soup = bs(r.content, "html.parser")

        # 1. Extract Description
        # Finds the text immediately following the "Description" header
        desc_header = soup.find('h4', string=lambda t: t and 'Description' in t)
        description = desc_header.find_next('p').get_text(strip=True) if desc_header else "N/A"

        # 2. Extract Duration
        # Finds the text in the "Assessment length" section
        duration_header = soup.find('h4', string=lambda t: t and 'Assessment length' in t)
        duration = duration_header.find_next('p').get_text(strip=True) if duration_header else "N/A"
        
        # Clean up duration string (e.g., "Approximate Completion Time in minutes = 17")
        if "=" in duration:
            duration = duration.split('=')[-1].strip() + " minutes"

        return description, duration

    except Exception as e:
        print(f"Error scraping details at {url}: {e}")
        return "Error", "Error"

# --- Helper Function to Parse a Single Row ---
def parse_test_row(row, test_type_map):
    cols = row.find_all('td', class_='custom__table-heading__general')
    if len(cols) < 3:
        return None

    title_col = row.find('td', class_='custom__table-heading__title')
    link_tag = title_col.find('a')
    test_name = link_tag.get_text(strip=True) if link_tag else title_col.get_text(strip=True)
    
    test_link_relative = link_tag.get('href') if link_tag else ''
    test_link = "https://www.shl.com" + test_link_relative if test_link_relative.startswith('/') else test_link_relative

    remote_testing = 'Yes' if cols[0].find('span', class_='catalogue__circle -yes') else 'No'
    adaptive_irt = 'Yes' if cols[1].find('span', class_='catalogue__circle -yes') else 'No'

    test_type_spans = cols[2].find_all('span', class_='product-catalogue__key')
    test_types_list = [test_type_map.get(span.get_text(strip=True), "Unknown") for span in test_type_spans]
        
    return {
        'Test Solution': test_name,
        'URL': test_link,
        'Remote Testing': remote_testing,
        'Adaptive/IRT': adaptive_irt,
        'Test Type(s)': test_types_list
    }

# --- Main Logic ---
def crawl_all_shl_products():
    all_data = []
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})

    for page in range(1, TOTAL_PAGES + 1):
        start_value = 12 * (page - 1)
        url = BASE_URL if page == 1 else PAGINATION_URL_TEMPLATE.format(start_value)
        
        print(f"\n--- Scraping Page {page} ---")
        try:
            r = session.get(url, timeout=10)
            soup = bs(r.content, "html.parser")
            tables = soup.find_all(class_="custom__table-responsive")
            
            # Select table (Index 1 on Page 1, Index 0 on others)
            target_table = tables[1] if page == 1 and len(tables) > 1 else tables[0]
            data_rows = target_table.find_all('tr', attrs={'data-entity-id': True})

            for row in data_rows:
                basic_info = parse_test_row(row, TEST_TYPE_MAP)
                if basic_info:
                    # Visit the detail page for Description and Duration
                    print(f"  > Fetching details for: {basic_info['Test Solution']}")
                    desc, dur = scrape_product_details(session, basic_info['URL'])
                    
                    basic_info['Description'] = desc
                    basic_info['Duration'] = dur
                    
                    all_data.append(basic_info)
                    time.sleep(DETAIL_DELAY) # Avoid rate limiting

        except Exception as e:
            print(f"Critical error on page {page}: {e}")
            break
            
        time.sleep(REQUEST_DELAY)

    # Save to JSON
    with open("shl_detailed_catalog.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"\nScraping complete. Total records: {len(all_data)}")

if __name__ == "__main__":
    crawl_all_shl_products()