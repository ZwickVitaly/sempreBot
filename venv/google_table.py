import re
import datetime
import pygsheets
from typing import List, Union

class GoogleTable:

    def __init__(self, cred_serv_file: str = '',
                 google_sheet_url: str = '') -> None:
        self.cred_serv_file = cred_serv_file
        self.google_sheet_url = google_sheet_url

    def get_google_sheet_by_url(self,
                             googlesheet_client: pygsheets.client.Client) -> pygsheets.Spreadsheet:
        sheet: pygsheets.Spreadsheet = googlesheet_client.open_by_url(self.google_sheet_url)
        return sheet.sheet1

    def get_googlesheet_client(self):
        return pygsheets.authorize(service_file=self.cred_serv_file)

    def search_workers(self, worker: str,
                               search_col: int = 1,
                               ):
        date_col = int(datetime.datetime.now().day)
        scenarios = {'/host': [r'.*хостес|оператор|вызывные\b.*', 'хостес'],
                     '/waiters': [r'.*официант\b.*', 'официанты'],
                     '/runners': [r'.*официанта\b.*', 'раннеры'],
                     '/cleaning': [r'.*уборщица\b.*', 'клининг'],
                     '/loaders': [r'.*котломойщик\b.*', 'котломойщики']
                     }
        googlesheet_client: pygsheets.client.Client = self.get_googlesheet_client()
        wks: pygsheets.Spreadsheet = self.get_google_sheet_by_url(googlesheet_client)
        workers_dict = {}
        find_cell = wks.find(scenarios[worker][0], re.IGNORECASE, matchEntireCell=True, cols=(search_col, search_col))
        for cell in find_cell:
            time = wks.get_value((cell.row, date_col + 2))
            name = wks.get_value((cell.row, 2))
            if time and name:
                if workers_dict.get(time):
                    workers_dict[time] += f', {name}'
                else:
                    workers_dict[time] = name
        result = f'\N{fire}\N{fire}\N{fire}\nСегодня, {datetime.datetime.now().strftime("%d.%m")} работают {scenarios[worker][1]}:\n'
        for key in sorted(filter(lambda x: x[0].isdigit(), workers_dict.keys()), key=lambda x: int(re.findall(r'^(\d{1,2})', x)[0])):
            if ':' in key:
                result += f'{key} {workers_dict[key]}\n'
            else:
                result += f'{key}:00 {workers_dict[key]}\n'
        return result + f'\N{fire}\N{fire}\N{fire}'