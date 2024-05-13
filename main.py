from aiogram import executor
from keyboards.startup_menu import standard_startup_menu
from bot_loader import dispatcher

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True, on_startup=standard_startup_menu)
