import winsound
from landsearch_scraper.steps.Step1 import Step1
from landsearch_scraper.steps.Step2 import Step2
from landsearch_scraper.steps.Step3 import Step3
from landsearch_scraper.steps.Step4 import Step4
from datetime import datetime
import re

class ScrapeDataLandsearch:
    def __init__(self, search_url):
        self.search_url = search_url
        self.headers = {
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
        self.step1_instance = Step1(self.headers)
        self.step2_instance = Step2(self.headers)
        self.step3_instance = Step3()
        self.step4_instance = Step4()

    def run(self):
        # Get the total number of records
        total_records = self.step1_instance.get_total_records(self.search_url)
        print(f"Total number of properties: {total_records}")

        # Prompt the user for approval
        approval = input(f"Do you want to proceed with the scraping? (yes/no): ").strip().lower()
        if approval != 'yes':
            print("Scraping process aborted by the user.")
            return

        # Gather URLs into a list along with their page numbers
        urls_with_page_numbers = self.step1_instance.get_all_urls_with_page_numbers(self.search_url)
        all_property_data = []

        # Process each URL using Step2
        for counter, (url, page_number) in enumerate(urls_with_page_numbers, start=1):
            print(f"Processing URL {counter} (Page {page_number}): {url}")
            property_data = self.step2_instance.process_property_url(url)
            all_property_data.append(property_data)

        # Play a sound when scraping is finished
        winsound.PlaySound('tada.wav', winsound.SND_FILENAME)

        # Generate file name based on search URL and current date/time
        url_part = self.format_url_part(self.search_url)
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"Landsearch_Scraper_{url_part}_{current_time}.xlsx"

        # Save all property data to an Excel file using Step3
        self.step3_instance.save_to_excel(all_property_data, file_name)

        # Prompt the user to open the Excel file using Step4
        self.step4_instance.prompt_to_open_file(file_name)

    def format_url_part(self, url):
        # Extract part after 'https://www.landsearch.com/properties'
        url_suffix = url.split("/properties/")[1]
        # Replace non-alphanumeric characters with underscores
        formatted = re.sub(r'\W+', '_', url_suffix)
        return formatted

def is_valid_url(url):
    return url.startswith("https://www.landsearch.com/properties") and url.strip()

if __name__ == "__main__":
    print("Welcome to Landsearch Scraper (v170120251721b13)\n")
    # Prompt the user for the search URL
    search_url = input("Please enter Landsearch search URL: ")

    # Validate the search URL
    if not is_valid_url(search_url):
        print("Invalid URL. Please enter a valid URL that starts with 'https://www.landsearch.com/properties'.")
    else:
        # Instantiate and run the scraping process
        scraper = ScrapeDataLandsearch(search_url)
        scraper.run()
