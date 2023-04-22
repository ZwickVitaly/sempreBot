from aiogram import Bot
from other_api.sempre_google_sheets import SempreSchedule , SempreMenu
from config import sempre_schedule_url


class SempreBot(Bot):
    def __init__(self, token, parse_mode):
        super().__init__(token, parse_mode=parse_mode)
        self.schedule_table = SempreSchedule(sempre_schedule_url)
        self.menu_table = SempreMenu()

    def set_google_table(self, google_table_url):
        self.schedule_table = SempreSchedule(google_table_url)
