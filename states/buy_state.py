from aiogram.fsm.state import State, StatesGroup

class BuyAccountState(StatesGroup):
    searching_country = State()
