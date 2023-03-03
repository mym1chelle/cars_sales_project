from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.models.db_commands.car import (
    count_car_brands,
    select_all_car_brands,
)
from tgbot.models.db_commands.color import (
    count_car_colors,
    select_all_car_colors
)
from tgbot.middlewares.translate import _


orders_menu_callback_data = CallbackData(
    'manage_data',
    'level',
    'filter',
    'brand_id',
    'color_id',
    'user_id'
)


def make_data_menu_callback_dt(
        level,
        filter="",
        brand_id="",
        color_id="",
        user_id=""
):
    return orders_menu_callback_data.new(
        level=level,
        filter=filter,
        brand_id=brand_id,
        color_id=color_id,
        user_id=user_id,
    )


async def all_data_menu_keyboard():
    """
    Displays the names of all tables in the database
    """
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)
    car_brands_count = await count_car_brands()
    color_count = await count_car_colors()
    buttons = [
        InlineKeyboardButton(
            text=_('Car brands ({count})').format(
                count=car_brands_count),
            callback_data=make_data_menu_callback_dt(
                level=CURRENT_LEVEL + 1,
                filter='cars'
            )),
        InlineKeyboardButton(
            text=_('Car colors ({count})').format(
                count=color_count
            ),
            callback_data=make_data_menu_callback_dt(
                level=CURRENT_LEVEL + 1,
                filter='colors'
            ))
    ]
    markup.add(*buttons)
    markup.row(
        InlineKeyboardButton(
            text=_('Exit'),
            callback_data='exit_data_menu'),
    )
    return markup


async def queryset_list(filter):
    """Displays a list of car models,
    car colors depending on the selection in the previous level"""
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=2)
    if filter == 'cars':
        car_brands = await select_all_car_brands()
        for brand in car_brands:
            button_text = brand.name
            callback_data = make_data_menu_callback_dt(
                level=CURRENT_LEVEL + 1,
                filter='cars',
                brand_id=brand.id
            )
            markup.insert(
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=callback_data
                )
            )
    elif filter == 'colors':
        car_colors = await select_all_car_colors()
        for color in car_colors:
            button_text = color.name
            callback_data = make_data_menu_callback_dt(
                level=CURRENT_LEVEL + 1,
                filter='colors',
                color_id=color.id
            )
            markup.insert(
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=callback_data
                )
            )
    markup.row(
        InlineKeyboardButton(
            text=_('Add'),
            callback_data=make_data_menu_callback_dt(
                level=CURRENT_LEVEL + 1,
                filter=filter
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Back'),
            callback_data=make_data_menu_callback_dt(
                level=CURRENT_LEVEL - 1
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Exit'),
            callback_data='exit_data_menu'),
    )
    return markup


async def select_item_menu(filter, brand_id=None, color_id=None):
    """Displays a menu with actions for the selected item"""
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row=1)
    if brand_id:
        buttons = [
            InlineKeyboardButton(
                text=_('Change'),
                callback_data=make_data_menu_callback_dt(
                    level=CURRENT_LEVEL + 1,
                    filter='cars',
                    brand_id=brand_id
                )),
            InlineKeyboardButton(
                text=_('Delete'),
                callback_data=make_data_menu_callback_dt(
                    level=CURRENT_LEVEL + 1,
                    filter='cards',
                    brand_id=brand_id
                ))
        ]
    elif color_id:
        buttons = [
            InlineKeyboardButton(
                text=_('Change'),
                callback_data=make_data_menu_callback_dt(
                    level=CURRENT_LEVEL + 1,
                    filter='colors',
                    color_id=color_id
                )),
            InlineKeyboardButton(
                text=_('Delete'),
                callback_data=make_data_menu_callback_dt(
                    level=CURRENT_LEVEL + 1,
                    filter='colors',
                    color_id=color_id
                ))
        ]
    elif not brand_id and not color_id:
        pass
    markup.add(*buttons)
    markup.row(
        InlineKeyboardButton(
            text=_('Back'),
            callback_data=make_data_menu_callback_dt(
                level=CURRENT_LEVEL - 1,
                filter=filter
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Exit'),
            callback_data='exit_data_menu'),
    )
    return markup


async def after_edit_item_keyboard(filter, brand_id=None, card_id=None):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row=1)
    markup.row(
        InlineKeyboardButton(
            text=_('Back'),
            callback_data=make_data_menu_callback_dt(
                level=CURRENT_LEVEL - 1,
                filter=filter,
                brand_id=brand_id,
                card_id=card_id
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Exit'),
            callback_data='exit_data_menu'),
    )
    return markup
