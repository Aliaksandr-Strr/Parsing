import json
from bs4 import BeautifulSoup
from requests_html import HTMLSession


class Parser:

    def __init__(self):
        self.session = HTMLSession()
        self.url = 'https://www.mebelshara.ru/contacts'
        self.json = 'address.json'
        self.result = []

    def get_html(self):
        result_html = self.session.get(url=self.url)
        soup = BeautifulSoup(result_html.text, 'html.parser')
        items = soup.find_all('div', class_='city-item')
        for item in items:
            city = item.find('h4', {'class': 'js-city-name'}).get_text(strip=True)
            shops = item.find_all('div', {'class': 'shop-list-item'})
            [self.get_content(city, shop) for shop in shops]

    def get_content(self, city, shop):
        self.result.append({
            'address': f"{city}, {shop['data-shop-address']}",
            'latlon': [float(shop['data-shop-latitude']), float(shop['data-shop-longitude'])],
            'name': shop['data-shop-name'],
            'phones': shop['data-shop-phone'],
            'working_hours': [shop['data-shop-mode1'], shop['data-shop-mode2']]
        })

    def write_file(self):
        self.get_html()
        with open(self.json, 'w', encoding='UTF-8') as file:
            json.dump(self.result, file, ensure_ascii=False)


if __name__ == '__main__':
    p = Parser()
    p.write_file()
