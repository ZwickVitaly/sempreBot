from aiogram import executor
from keyboards.startup_menu import standard_startup_menu
from handlers.ONE_BIG_HANDLERS_FILE import dispatcher

if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True, on_startup=standard_startup_menu)
