from aiogram import Bot
from other_api.sempre_google_sheets import SempreSchedule, SempreMenu
from config import sempre_schedule_url, sempre_menu_url


class SempreBot(Bot):
    """
    Specific SempreBot class with Google sheets. Parent: Bot

    :param: token (str): takes in telegram bot token.
    :param: parse_mode (str): takes in bot parse mode.

    :arg: schedule_table (SempreSchedule): instance of a SempreSchedule class
    :arg: menu_table (SempreSchedule): instance of a SempreMenu class
    """
    def __init__(self, token: str, parse_mode: str) -> None:
        super().__init__(token, parse_mode=parse_mode)
        self.schedule_sheet = SempreSchedule(sempre_schedule_url)
        self.menu_sheet = SempreMenu(sempre_menu_url)

    def set_google_table(self, google_sheet_url: str) -> None:
        """
        schedule_sheet setter

        :param: google_table_url (str): takes in url of Google table

        :return: None
        """
        self.schedule_sheet = SempreSchedule(google_sheet_url)
