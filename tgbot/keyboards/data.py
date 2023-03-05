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


data_menu_callback_data = CallbackData(
    'manage_data',
    'level',
    'filter',
    'brand_id',
    'color_id',
    'action'
)

delete_item_callback_data = CallbackData(
    'delete',
    'brand_id',
    'color_id'
)


def make_data_menu_callback_dt(
        level,
        filter="",
        brand_id="",
        color_id="",
        action=""
):
    return data_menu_callback_data.new(
        level=level,
        filter=filter,
        brand_id=brand_id,
        color_id=color_id,
        action=action
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


async def queryset_list_keyboard(filter):
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
        markup.row(
            InlineKeyboardButton(
                text=_('Add'),
                callback_data=make_data_menu_callback_dt(
                    level=CURRENT_LEVEL + 1,
                    filter='cars',
                    action='add'
                )
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
                    filter='colors',
                    action='add'
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


async def select_item_menu_keyboard(filter, action, brand_id='', color_id=''):
    """Displays a menu with actions for the selected item"""
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row=1)
    if action == 'add':
        pass
    if filter == 'cars' and action != 'add':
        buttons = [
            InlineKeyboardButton(
                text=_('Change'),
                callback_data=make_data_menu_callback_dt(
                    level=CURRENT_LEVEL + 1,
                    filter=filter,
                    action='change',
                    brand_id=brand_id
                )),
            InlineKeyboardButton(
                text=_('Delete'),
                callback_data=make_data_menu_callback_dt(
                    level=CURRENT_LEVEL + 1,
                    filter=filter,
                    action='delete',
                    brand_id=brand_id
                ))
        ]
        markup.add(*buttons)
    elif filter == 'colors' and action != 'add':
        buttons = [
            InlineKeyboardButton(
                text=_('Change'),
                callback_data=make_data_menu_callback_dt(
                    level=CURRENT_LEVEL + 1,
                    filter=filter,
                    action='change',
                    color_id=color_id
                )),
            InlineKeyboardButton(
                text=_('Delete'),
                callback_data=make_data_menu_callback_dt(
                    level=CURRENT_LEVEL + 1,
                    filter=filter,
                    action='delete',
                    color_id=color_id
                ))
        ]
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


async def add_edit_delete_keyboard(filter, action, brand_id='', color_id=''):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row=1)
    if action == 'delete':
        markup.row(
            InlineKeyboardButton(
                text=_('Yes, delete'),
                callback_data=delete_item_callback_data.new(
                    brand_id=brand_id,
                    color_id=color_id
                )
            )
        )
    markup.row(
        InlineKeyboardButton(
            text=_('Back'),
            callback_data=make_data_menu_callback_dt(
                level=CURRENT_LEVEL - 1,
                filter=filter,
                brand_id=brand_id,
                color_id=color_id
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Exit'),
            callback_data='exit_data_menu'),
    )
    return markup
