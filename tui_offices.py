import json
import requests
from bs4 import BeautifulSoup


class Parser:

    def __init__(self):
        self.url = 'https://apigate.tui.ru/api/office/list?cityId=1&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false'
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 OPR/70.0.3728.189'
        }
        self.offices = []
        self.json = 'offices.json'

    def get_json(self):
        try:
            result = requests.get(self.url, headers=self.headers)
            return result.json()

        except Exception as ex:
            print(ex)

    def processing_data(self):
        all_data = self.get_json()
        for data in all_data['offices']:
            weekday = f"Пн-Пт {data['hoursOfOperation']['workdays']['startStr']}-" \
                      f"{data['hoursOfOperation']['workdays']['endStr']}"
            if not data['hoursOfOperation']['saturday']['isDayOff']:
                saturday = f"Сб {data['hoursOfOperation']['saturday']['startStr']}-" \
                           f"{data['hoursOfOperation']['saturday']['endStr']}"
            else:
                saturday = 'Сб выходной'
            if not data['hoursOfOperation']['sunday']['isDayOff']:
                sunday = f"Вс {data['hoursOfOperation']['sunday']['startStr']}-" \
                         f"{data['hoursOfOperation']['sunday']['endStr']}"
            else:
                sunday = 'Вс выходной'
            self.offices.append(
                {
                    'address': data['address'],
                    'latlon': [data['latitude'], data['longitude']],
                    'name': data['name'],
                    'phones': [data['phone']],
                    'working_hours': [weekday, saturday, sunday],

                }
            )

    def write_file(self):
        self.processing_data()
        with open(self.json, 'w', encoding='UTF-8') as file:
            json.dump(self.offices, file, ensure_ascii=False)


if __name__ == '__main__':
    p = Parser()
    p.write_file()
