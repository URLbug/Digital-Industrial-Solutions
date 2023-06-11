from aiogram.fsm.state import State, StatesGroup


class Order(StatesGroup):
    one = State()
    two = State()
