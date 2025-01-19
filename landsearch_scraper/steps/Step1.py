import requests
from bs4 import BeautifulSoup
import math


class Step1:
    def __init__(self, headers):  # constructor
        self.headers = headers

    def get_total_records(self, search_url):
        response = requests.get(search_url, headers=self.headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the total number of records from the specific div class
        count_div = soup.find('div', class_='sorting__count g-e')
        if count_div:
            total_records = self.extract_number_of_records(count_div.text)
            return total_records
        return 0

    def extract_number_of_records(self, text):
        import re
        match = re.search(r'(\d+,\d+|\d+)', text)
        if match:
            # Remove commas if any and convert to an integer
            return int(match.group(1).replace(',', ''))
        return 0

    def get_all_urls_with_page_numbers(self, search_url):
        all_urls_with_page_numbers = []
        total_records = self.get_total_records(search_url)
        total_pages = math.ceil(total_records / 50)

        for page_number in range(1, total_pages + 1):
            if page_number == 1:
                current_url = search_url
            else:
                current_url = f"{search_url}/p{page_number}"

            print(f"Processing page {page_number}: {current_url}")

            response = requests.get(current_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all <a> tags with class 'preview__link' and extract their href attributes
            links = soup.find_all('a', class_='preview__link')
            base_url = "https://www.landsearch.com"
            urls = [(base_url + link.get('href'), page_number) for link in links if link.get('href')]
            all_urls_with_page_numbers.extend(urls)

        return all_urls_with_page_numbers
