from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.models.db_commands.car import (
    select_all_car_brands,
    select_all_car_colors
)
from tgbot.models.db_constants import STEERING_WHEEL_POSITION
from tgbot.middlewares.translate import _


create_order_callback_data = CallbackData(
    'create',
    'car_brand_id',
    'steering_wheel_position',
    'car_color_id'
)


def order_callback_data(
        car_brand_id='-',
        steering_wheel_position='-',
        car_color_id='-'
):
    return create_order_callback_data.new(
        car_brand_id=car_brand_id,
        steering_wheel_position=steering_wheel_position,
        car_color_id=car_color_id
    )


async def select_car_brand_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    car_brands = await select_all_car_brands()
    for brand in car_brands:
        button_text = brand.name
        callback_data = order_callback_data(
            car_brand_id=brand.id
        )
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data
            )
        )
    markup.row(
        InlineKeyboardButton(
            text=_('Cancel'),
            callback_data='cancel_create_order'
        )
    )
    return markup


async def select_steering_wheel_position_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    steering_wheel_position = STEERING_WHEEL_POSITION
    for position in steering_wheel_position:
        button_text = position[1]
        callback_data = order_callback_data(
            steering_wheel_position=position[0]
        )
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data
            )
        )
    markup.row(
        InlineKeyboardButton(
            text=_('Back'),
            callback_data='back_create_order'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Cancel'),
            callback_data='cancel_create_order'
        )
    )
    return markup


async def select_car_color_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    colors = await select_all_car_colors()
    for color in colors:
        button_text = color.name
        callback_data = order_callback_data(
            car_color_id=color.id
        )
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data
            )
        )
    markup.row(
        InlineKeyboardButton(
            text=_('Back'),
            callback_data='back_create_order'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Cancel'),
            callback_data='cancel_create_order'
        )
    )
    return markup


async def get_order_wishes_keyboard():
    markup = InlineKeyboardMarkup(row=1)
    markup.row(
        InlineKeyboardButton(
            text=_('No comment'),
            callback_data='order_without_wishess'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Back'),
            callback_data='back_create_order'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Cancel'),
            callback_data='cancel_create_order'
        )
    )
    return markup
