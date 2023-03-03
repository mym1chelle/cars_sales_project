from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateOrderStates(StatesGroup):
    select_car_brand = State()
    select_steering_wheel_position = State()
    select_car_color = State()
    add_order_wishes = State()
    
