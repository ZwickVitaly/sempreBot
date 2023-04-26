from abc import ABC
from typing import List, Dict
from pygsheets.client import Client
from pygsheets import authorize, Cell
from random import choice
from datetime import datetime, timedelta
import re


class GoogleSheet(ABC):
    """
    Abstract GoogleSheet class

    :param: sheet_url (str): takes in google sheet url

    :arg: google_sheet_client (Client): contains authorized Client
    :arg: google_sheet_url (str): contains Google sheet url
    """

    def __init__(self, sheet_url: str) -> None:
        self.google_sheet_client: Client = authorize(service_file='google_credentials.json')
        self.google_sheet_url: str = sheet_url


class SempreSchedule(GoogleSheet):
    """
    Schedule sheet class. Parent: GoogleSheet

    Attributes:
        worker_search_scenarios (Dict): contains ('worker': 'search pattern')
        emoji_list List[str]: contains list of emojis

    :param: sempre_schedule_url (str): takes in schedule Google sheet url.

    :arg: google_sheet_client (Client): contains authorized Client
    :arg: google_sheet_url (str): contains Google sheet url
    """
    worker_search_scenarios: Dict = {
        'Хостес': r'.*хостес|оператор|вызывные\b.*',
        'Официанты': fr'.*официант\b.*|.*стаж[её]р\b.*',
        'Раннеры': r'.*официанта\b.*',
        'Клининг': r'.*уборщица\b.*',
        'Грузчики': r'.*котломойщик\b.*',
    }
    emoji_list: List[str] = [
        '\U0001F973', '\U0001F60E', '\U0001F340',
        '\U0001F354', '\U0001F370', '\U0001F379',
        '\U0001F378', '\U0001F377',
        '\U0001F37E', '\U0001F37A'
    ]

    def __init__(self, sempre_schedule_url: str) -> None:
        super().__init__(sheet_url=sempre_schedule_url)

    def search_workers(self,
                       worker: str,
                       date: int,
                       title_col: int = 1,
                       name_col: int = 2,
                       date_shift: int = 2
                       ) -> str:
        """
        Method to read requested data from Google sheets and compile it into requested output format

        :param: worker (str): takes in title of workers
        :param: date (int): takes in requested day number

        :keyword: title_col (int): takes in job titles column
        :keyword: name_col (int): takes in workers names column
        :keyword: date_shift (int): takes in shift of date columns from first column

        :arg: day_name (str): contains name of chosen day
        :arg: sheet (Spreadsheet.sheet1): contains working sheet
        :arg: shift_dict (Dict): dict of (shift hours: list of workers names)
        :arg: found_cells (List[pygsheets.Cell]): contains list of matching cells
        :arg: time (str): contains shift hours
        :arg: name (str): contains worker's name
        :arg: chosen_emoji (str): contains tripled randomly chosen emoji
        :arg: day_month (str): contains date of requested day in requested format

        :return: result: result string
        :rtype: str
        """
        sheet = self.google_sheet_client.open_by_url(self.google_sheet_url).sheet1
        day_name: str = 'Сегодня' if date == datetime.now().day else 'Завтра'
        shift_dict: Dict = {}

        found_cells: List[Cell] = sheet.find(
            self.worker_search_scenarios.get(worker),
            re.IGNORECASE,
            matchEntireCell=True,
            cols=(title_col, title_col)
        )

        for cell in found_cells:
            time: str = sheet.get_value((cell.row, date + date_shift))
            if worker == 'Официанты':
                name: str = sheet.get_value((cell.row, name_col)).strip().split(' ')[0]
                if re.match(r'.*стаж[её]р\b.*', cell.value, re.IGNORECASE):
                    name += '(стажёр)'
            else:
                name: str = sheet.get_value((cell.row, name_col))
            if time and name:
                if shift_dict.get(time):
                    shift_dict[time] += f', {name}'
                else:
                    shift_dict[time]: Dict = name
        chosen_emoji: str = choice(self.emoji_list) * 3
        day_month: str = datetime.now().strftime("%d.%m") if date == datetime.now().day \
            else (datetime.now() + timedelta(days=1)).strftime("%d.%m")
        result: str = f'{chosen_emoji} {day_name} {day_month} {chosen_emoji}\n' \
                      f'{worker}:\n'

        for key in sorted(filter(lambda x: x[0].isdigit(), shift_dict.keys()),
                          key=lambda x: int(re.findall(r'^(\d{1,2})', x)[0])):
            if ':' in key:
                result += f'{key} {shift_dict[key]}\n'
            else:
                result += f'{key}:00 {shift_dict[key]}\n'

        return result


class SempreMenu(GoogleSheet):
    """
    Schedule sheet class. Parent: GoogleSheet

    :param: menu_url (str): takes in menu google sheet url.

    :arg: google_sheet_client (Client): contains authorized Client
    :arg: google_sheet_url (str): contains google sheet url
    """

    def __init__(self, menu_url: str) -> None:
        super().__init__(sheet_url=menu_url)

    def search_main_menu(self, dish: str, search_col=2, dish_desc_col=3) -> str:
        """
        Method to find dish descriptions in a dish menu Google sheet and compile data in requested output format

        :param: dish (str)

        :keyword: search_col (int)
        :keyword: dish_desc_col (int)

        :arg: :arg: found_cells (List[pygsheets.Cell]): contains list of matching cells

        :returns: result: result string
        :rtype: str

        """
        sheet = self.google_sheet_client.open_by_url(self.google_sheet_url).sheet1
        found_cells: List[Cell] = sheet.find(
                                             fr'.*{dish}.*',
                                             re.IGNORECASE,
                                             matchEntireCell=True,
                                             cols=(search_col, search_col)
                                             )

        if found_cells:
            result: str = ''
            for cell in found_cells:
                dish_description = sheet.get_value((cell.row, dish_desc_col))
                result += f'Блюдо: {cell.value}\nОписание:\n{dish_description}\n\n'
        else:
            result: str = 'Совпадений не найдено.'

        return result
