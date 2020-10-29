import json
from requests_html import HTMLSession


class Parser:

    def __init__(self):
        self.session = HTMLSession()
        self.url = 'https://apigate.tui.ru/api/office/list?cityId=1&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false'
        self.offices = []
        self.json = 'offices.json'

    def processing_data(self):
        result = self.session.get(url=self.url)
        all_data = result.json()
        for data in all_data['offices']:
            working_hours = []
            workdays_hours = data['hoursOfOperation']['workdays']
            saturday_hours = data['hoursOfOperation']['saturday']
            sunday_hours = data['hoursOfOperation']['sunday']
            working_hours.append(f"Пн-Пт {workdays_hours.get('startStr')} - {workdays_hours.get('endStr')}")
            if not saturday_hours['isDayOff']:
                working_hours.append(f"Сб {saturday_hours.get('startStr')} - {saturday_hours.get('endStr')}")
            if not sunday_hours['isDayOff']:
                working_hours.append(f"Вс {sunday_hours.get('startStr')} - {sunday_hours.get('endStr')}")
            self.offices.append(
                {
                    'address': data['address'],
                    'latlon': [float(data['latitude']), float(data['longitude'])],
                    'name': data['name'],
                    'phones': data['phone'].split(';'),
                    'working_hours': working_hours,

                }
            )

    def write_file(self):
        self.processing_data()
        with open(self.json, 'w', encoding='UTF-8') as file:
            json.dump(self.offices, file, ensure_ascii=False)


if __name__ == '__main__':
    p = Parser()
    p.write_file()
