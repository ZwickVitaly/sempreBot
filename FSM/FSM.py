from aiogram.dispatcher.filters.state import State, StatesGroup


class SempreFSM(StatesGroup):
    main_menu = State()
    menu_choice = State()
    today_shift = State()
    tomorrow_shift = State()
    end_state = State()
