import requests
from bs4 import BeautifulSoup

def get_total_records(search_url, headers):
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the total number of records from the specific div class
    count_div = soup.find('div', class_='sorting__count g-e')
    if count_div:
        total_records = extract_number_of_records(count_div.text)
        return total_records
    return 0

def extract_number_of_records(text):
    import re
    match = re.search(r'(\d+,\d+|\d+)', text)
    if match:
        # Remove commas if any and convert to an integer
        return int(match.group(1).replace(',', ''))
    return 0

# Define the search URL and headers
search_url = 'https://www.landsearch.com/properties/charlotte-county-fl/filter/price[max]=10000,price[min]=0'
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9,he;q=0.8',
    'origin': 'https://www.landsearch.com',
    'priority': 'u=1, i',
    'referer': 'https://www.landsearch.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

# Run the test
total_records = get_total_records(search_url, headers)
print(f"Total number of properties: {total_records}")
