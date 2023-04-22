from aiogram import Dispatcher
from config import TOKEN
from bots.sempre_bot import SempreBot
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = SempreBot(TOKEN, parse_mode='HTML')
dispatcher = Dispatcher(bot, storage=storage)
