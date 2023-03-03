from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.middlewares.translate import _
from tgbot.filters.seller_filter import SellerFilter
from tgbot.models.db_commands.car import get_car_brand
from tgbot.models.db_commands.color import get_car_color
from tgbot.keyboards.data_management_keyboard import (
    orders_menu_callback_data,
    all_data_menu_keyboard,
    queryset_list,
    select_item_menu,
    after_edit_item_keyboard
)
from bot_setting import bot


async def show_data_menu(message: types.Message):
    await main_data_menu(message)


async def main_data_menu(message: types.Message | types.CallbackQuery, **kwargs):
    """
    Menu with data

    Contains buttons:
    — Car brands (count brands)
    — Car colors (count colors)
    — Exit
    """
    markup = await all_data_menu_keyboard()
    if isinstance(message, types.Message):
        await message.answer(text=_('Menu:'), reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text(text=_('Menu:'), reply_markup=markup)


async def list_data(call: types.CallbackQuery, filter, **kwargs):
    """Lists all car brands or all colors"""
    if filter == 'cars':
        text = _('Car brands:')
    elif filter == 'colors':
        text = _('Car colors:')
    markup = await queryset_list(filter=filter)
    await call.message.edit_text(
        text=text,
        reply_markup=markup
    )


async def selected_item_menu(call: types.CallbackQuery, filter, brand_id, color_id, **kwargs):
    """Displays a list of actions with the selected element"""
    if brand_id:
        car_brand = await get_car_brand(brand_id=brand_id)
        text = str(car_brand.name)
    elif color_id:
        car_color = await get_car_color(color_id=color_id)
        text = str(car_color.name)
    markup = await select_item_menu(
        filter=filter,
        brand_id=brand_id,
        color_id=color_id
    )
    await call.message.edit_text(
        text=text,
        reply_markup=markup
    )


async def after_edit_or_delete(call: types.CallbackQuery, filter, brand_id, card_id, **kwargs):
    """Displays information after changing data"""
    markup = await after_edit_item_keyboard(
        filter=filter,
        brand_id=brand_id,
        card_id=card_id
    )
    await call.message.edit_text(
        text='',
        reply_markup=markup
    )


async def navigate(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """Function for navigating through the inline menu"""
    current_level = str(callback_data.get('level'))
    filter = callback_data.get('filter')
    brand_id = callback_data.get('brand_id')
    color_id = callback_data.get('color_id')

    levels = {
        '0': main_data_menu,
        '1': list_data,
        '2': selected_item_menu,
        '3': after_edit_or_delete
    }
    current_level_func = levels[current_level]

    await current_level_func(
        call=call,
        message=call,
        filter=filter,
        brand_id=brand_id,
        color_id=color_id
    )


def register_data_menu(dp: Dispatcher):
    dp.register_message_handler(
        show_data_menu,
        SellerFilter(),
        commands='data'
    )
    dp.register_callback_query_handler(
        navigate,
        orders_menu_callback_data.filter()
    )
