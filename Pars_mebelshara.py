import json
import requests
from bs4 import BeautifulSoup


class Parser:

    def __init__(self):
        self.host = 'https://www.mebelshara.ru'
        self.url = 'https://www.mebelshara.ru/contacts'
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 OPR/70.0.3728.189'
        }
        self.json = 'address.json'
        self.contacts = []

    def get_html(self):
        try:
            result = requests.get(self.url, headers=self.headers)
            self.get_content(result.text)
        except Exception as ex:
            print(ex)

    def get_content(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        items = soup.find_all('div', class_='city-item')
        for item in items:
            self.contacts.append(
                {
                    'address': f"{item.find('h4', class_='js-city-name').get_text(strip=True)}," \
                               f" {item.find('div', class_='shop-list-item')['data-shop-address']}",
                    'latlon': [f"{item.find('div', class_='shop-list-item')['data-shop-longitude']}," \
                               f" {item.find('div', class_='shop-list-item')['data-shop-latitude']}"],
                    'name': f"{item.find('div', class_='shop-list-item')['data-shop-name']}",
                    'phones': [f"{item.find('div', class_='shop-list-item')['data-shop-phone']}"],
                    'working_hours': [f"{item.find('div', class_='shop-list-item')['data-shop-mode1']}  " \
                                      f"{item.find('div', class_='shop-list-item')['data-shop-mode2']}"],
                })

    def write_file(self):
        self.get_html()
        with open(self.json, 'w', encoding='UTF-8') as file:
            json.dump(self.contacts, file, ensure_ascii=False)


if __name__ == '__main__':
    p = Parser()
    p.write_file()
