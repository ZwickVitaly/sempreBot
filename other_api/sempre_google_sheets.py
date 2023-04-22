import re
import pygsheets
from random import choice
from datetime import datetime
from config import sempre_menu_url


class SempreSchedule:

    def __init__(self, sempre_schedule_url: str) -> None:
        self.google_sheet_client = pygsheets.authorize(service_file='google_credentials.json')
        self.google_sheet_url = sempre_schedule_url
        self.worker_search_scenarios = {
                                 'хостес': r'.*хостес|оператор|вызывные\b.*',
                                 'официанты': r'.*официант\b.*|.*стаж[её]р\b.*',
                                 'раннеры': r'.*официанта\b.*',
                                 'клининг': r'.*уборщица\b.*',
                                 'грузчики': r'.*котломойщик\b.*',
                                 }
        self.emoji_list = [
                            '\U0001F973', '\U0001F60E', '\U0001F340',
                            '\U0001F354', '\U0001F370', '\U0001F379',
                            '\U0001F378', '\U0001F377',
                            '\U0001F37E', '\U0001F37A'
                          ]

    def search_workers(self, worker, date, search_col=1):
        day_name = 'Сегодня' if date == datetime.now().day else 'Завтра'
        date_shift = 2
        worker = worker.lower()
        date_col = int(date.day)
        sheet = self.google_sheet_client.open_by_url(self.google_sheet_url).sheet1
        shift_dict = {}

        find_cell = sheet.find(
                               self.worker_search_scenarios.get(worker),
                               re.IGNORECASE,
                               matchEntireCell=True,
                               cols=(search_col, search_col)
                               )

        for cell in find_cell:
            time = sheet.get_value((cell.row, date_col + date_shift))
            if worker == 'официанты':
                name = sheet.get_value((cell.row, 2)).split(' ')[0]
                if re.match(r'.*стаж[её]р\b.*', cell.value, re.IGNORECASE):
                    name += '(стажёр)'
            else:
                name = sheet.get_value((cell.row, 2))
            if time and name:
                if shift_dict.get(time):
                    shift_dict[time] += f', {name}'
                else:
                    shift_dict[time] = name

        chosen_emoji = choice(self.emoji_list)
        result = f'{3 * chosen_emoji} {day_name} {date.strftime("%d.%m")} {3 * chosen_emoji}\n' \
                 f'{worker.capitalize()}:\n'

        for key in sorted(filter(lambda x: x[0].isdigit(), shift_dict.keys()),
                          key=lambda x: int(re.findall(r'^(\d{1,2})', x)[0])):
            if ':' in key:
                result += f'{key} {shift_dict[key]}\n'
            else:
                result += f'{key}:00 {shift_dict[key]}\n'

        return result


class SempreMenu:

    def __init__(self) -> None:
        self.google_sheet_client = pygsheets.authorize(service_file='google_credentials.json')
        self.google_sheet_url = sempre_menu_url

    def search_main_menu(self, dish: str, search_col=2, dish_desc_col=3):
        sheet = self.google_sheet_client.open_by_url(self.google_sheet_url).sheet1
        cells = sheet.find(fr'.*{dish}.*', re.IGNORECASE, matchEntireCell=True, cols=(search_col, search_col))
        if cells:
            result = ''
            for cell in cells:
                dish_description = sheet.get_value((cell.row, dish_desc_col))
                result += f'Блюдо: {cell.value}\nОписание:\n{dish_description}\n\n'
        else:
            result = 'Совпадений не найдено.'
        return result
