import requests
from bs4 import BeautifulSoup

class Step2:
    def __init__(self, headers):
        self.headers = headers

    def extract_element_from_url(self, soup, tag, attrs):
        element = soup.find(tag, attrs)
        if element:
            return element.text.strip()
        else:
            return "N/A"

    def process_property_url(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the parcel number
        apn = self.extract_element_from_url(soup, 'li', {'class': 'g-fc $propertyCopy', 'data-label': 'parcel number'})

        # Extract the price
        price = self.extract_element_from_url(soup, 'div', {'class': 'property-price'})

        # Extract the size
        size = self.extract_element_from_url(soup, 'div', {'class': 'property-size'})

        # Extract the agent
        agent = self.extract_element_from_url(soup, 'div', {'class': 'profile-card__name'})

        return {
            'url': url,
            'apn': apn,
            'price': price,
            'size': size,
            'agent': agent
        }
