from aiogram.dispatcher.filters.state import State, StatesGroup


class SempreFSM(StatesGroup):
    """
    Specific Finite State Machine class. Parent - StatesGroup
    Attributes:
        main_menu (State): main menu state
        menu_choice (State): dish menu choice state
        today_shift (State): today's shift worker choice state
        tomorrow_shift (State): tomorrow's shift worker choice state
        end_state (State): end(stop) state
    """
    main_menu = State()
    day_choice = State()
    menu_choice = State()
    today_shift = State()
    tomorrow_shift = State()
    end_state = State()
