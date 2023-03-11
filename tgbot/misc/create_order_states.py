from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateOrderStates(StatesGroup):
    add_order_wishes = State()
