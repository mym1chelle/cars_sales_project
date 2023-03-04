from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.middlewares.translate import _
from tgbot.filters.seller_filter import SellerFilter
from tgbot.models.db_commands.car import (
    get_car_brand,
    add_car_brand,
    change_car_brand,
    delete_car_brand
)
from tgbot.models.db_commands.color import (
    get_car_color,
    add_car_color,
    change_car_color,
    delete_car_color
)
from tgbot.keyboards.data_management_keyboard import (
    orders_menu_callback_data,
    all_data_menu_keyboard,
    queryset_list_keyboard,
    select_item_menu_keyboard,
    add_edit_delete_keyboard,
    delete_item_callback_data
)
from bot_setting import bot


async def show_data_menu(message: types.Message):
    await main_data_menu(message)


async def main_data_menu(
        message: types.Message | types.CallbackQuery, **kwargs
):
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
    """Lists all car brands or all colors

    Here you can select a specific color or car model,
    or add a new item according to your needs.
    """
    if filter == 'cars':
        text = _('Car brands:')
    elif filter == 'colors':
        text = _('Car colors:')
    markup = await queryset_list_keyboard(filter=filter)
    await call.message.edit_text(
        text=text,
        reply_markup=markup
    )


async def selected_item_menu(
        call: types.CallbackQuery,
        filter, action, brand_id, color_id, state: FSMContext, **kwargs
):
    """Displays a list of actions with the selected element"""
    if filter == 'cars':
        if action == 'add':
            text = _('Enter a new car brand name (no more than 150 characters):')
            async with state.proxy() as data:
                data['filter'] = filter
                data['message_id'] = call.message.message_id
            await state.set_state('add_new_item')
        elif brand_id:
            car_brand = await get_car_brand(brand_id=brand_id)
            text = car_brand.name
    elif filter == 'colors':
        if action == 'add':
            text = _('Enter a new color name (no more than 100 characters):')
            async with state.proxy() as data:
                data['filter'] = filter
                data['message_id'] = call.message.message_id
            await state.set_state('add_new_item')
        elif color_id:
            car_color = await get_car_color(color_id=color_id)
            text = car_color.name
    markup = await select_item_menu_keyboard(
        filter=filter,
        action=action,
        brand_id=brand_id,
        color_id=color_id
    )
    await call.message.edit_text(
        text=text,
        reply_markup=markup
    )


async def add_edit_delete_item(
        call: types.CallbackQuery,
        filter,
        action,
        brand_id,
        color_id,
        state: FSMContext,
        **kwargs):
    """Displays information after changing data
    Buttons are available to change the selected item or delete it
    """
    print(filter)
    print(brand_id)
    print(action)
    if filter == 'cars' and brand_id:
        brand = await get_car_brand(brand_id=brand_id)
        if action == 'change':
            text = _("""
Enter a new car brand name, old name «{name}»
(no more than 150 characters):"""
                     ).format(
                name=brand.name)
            async with state.proxy() as data:
                data['brand_id'] = brand_id
                data['message_id'] = call.message.message_id
            await state.set_state('change_item')
        elif action == 'delete':
            text = _('Are you sure you want to delete «{name}»?:').format(
                name=brand.name)
    elif filter == 'colors' and color_id:
        color = await get_car_color(color_id=color_id)
        if action == 'change':
            text = _("""
Enter a new color name, old name «{name}»
(no more than 150 characters):
""").format(
                name=color.name)
            async with state.proxy() as data:
                data['color_id'] = color_id
                data['message_id'] = call.message.message_id
            await state.set_state('change_item')
        elif action == 'delete':
            text = _('Are you sure you want to delete «{name}»?:').format(
                name=color.name)
    markup = await add_edit_delete_keyboard(
        filter=filter,
        action=action,
        brand_id=brand_id,
        color_id=color_id
    )
    await call.message.edit_text(
        text=text,
        reply_markup=markup
    )


async def navigate(
        call: types.CallbackQuery,
        callback_data: dict,
        state: FSMContext
):
    """Function for navigating through the inline menu"""
    current_level = str(callback_data.get('level'))
    filter = callback_data.get('filter')
    action = callback_data.get('action')
    brand_id = callback_data.get('brand_id')
    color_id = callback_data.get('color_id')

    levels = {
        '0': main_data_menu,
        '1': list_data,
        '2': selected_item_menu,
        '3': add_edit_delete_item
    }
    current_level_func = levels[current_level]

    await current_level_func(
        call=call,
        message=call,
        state=state,
        filter=filter,
        action=action,
        brand_id=brand_id,
        color_id=color_id
    )


async def adding_a_new_item(message: types.Message, state: FSMContext):
    """Handles adding a new car model or a new color"""
    data = await state.get_data()
    filter = data.get('filter')
    message_id = data.get('message_id')
    print(message.text)
    if filter == 'cars':
        if len(message.text) > 150:
            await message.delete()
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=message_id,
                text=_("""
<b>The number of characters is more than 150. Try again.</b>

Enter a new car brand name (no more than 150 characters):
"""),
                reply_markup=await select_item_menu_keyboard(
                    filter=filter,
                    action='add'
                )
            )
        else:
            new_car_brand = await add_car_brand(
                car_brand=message.text
            )
            text = _('The brand of the car «{brand}» has been added').format(
                brand=new_car_brand.name)
            await message.delete()
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=message_id,
                text=text,
                reply_markup=await select_item_menu_keyboard(
                    action='add',
                    filter=filter
                )
            )
            await state.finish()
    elif filter == 'colors':
        if len(message.text) > 100:
            await message.delete()
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=message_id,
                text=_("""
<b>The number of characters is more than 100. Try again.</b>

Enter a new color name (no more than 100 characters):
"""),
                reply_markup=await select_item_menu_keyboard(
                    filter=filter,
                    action='add',
                )
            )
        else:
            new_color = await add_car_color(color_name=message.text)
            text = _('Car color «{color}» has been added').format(
                color=new_color
            )
            await message.delete()
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=message_id,
                text=text,
                reply_markup=await select_item_menu_keyboard(
                    action='add',
                    filter=filter
                )
            )
            await state.finish()


async def change_item(message: types.Message, state: FSMContext):
    data = await state.get_data()
    brand_id = data.get('brand_id')
    color_id = data.get('color_id')
    message_id = data.get('message_id')
    if brand_id:
        if len(message.text) > 150:
            await message.delete()
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=message_id,
                text=_("""
<b>The number of characters is more than 150. Try again.</b>

Enter a new car brand name (no more than 150 characters):
"""),
                reply_markup=await add_edit_delete_keyboard(
                    filter='cars',
                    action='change',
                    brand_id=brand_id,
                )
            )
        else:
            filter = 'cars'
            changed_brand = await change_car_brand(
                new_brand=message.text,
                brand_id=brand_id
            )
            if changed_brand:
                text = _('The car model has been changed to «{brand}»').format(
                    brand=changed_brand
                )
            else:
                text = _('An error occurred while editing car model'),
            markup = await select_item_menu_keyboard(
                    filter=filter,
                    action='change',
                    brand_id=brand_id
                )
            await message.delete()
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=message_id,
                text=text,
                reply_markup=markup
                )
            await state.finish()
    elif color_id:
        if len(message.text) > 100:
            await message.delete()
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=message_id,
                text=_("""
<b>The number of characters is more than 100. Try again.</b>

Enter a new color name (no more than 100 characters):
"""),
                reply_markup=await add_edit_delete_keyboard(
                    filter='cars',
                    action='change',
                    color_id=color_id,
                )
            )
        else:
            filter = 'colors'
            changed_color = await change_car_color(
                new_color=message.text,
                color_id=color_id
            )
            if changed_color:
                text = _('The color has been changed to «{color}»').format(
                    color=changed_color.name
                )
            else:
                text = _('An error occurred while changing the color'),
            markup = await select_item_menu_keyboard(
                    filter=filter,
                    action='change',
                    color_id=color_id
                )
            await message.delete()
            await bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=message_id,
                text=text,
                reply_markup=markup
                )
            await state.finish()


async def confirm_to_delete(
        call: types.CallbackQuery,
        callback_data: dict
        ):
    print(callback_data)
    brand_id = callback_data.get('brand_id')
    print(brand_id)
    color_id = callback_data.get('color_id')
    if brand_id:
        brand = await delete_car_brand(brand_id=brand_id)
        if brand:
            await call.answer(text=_('The car brand has been successfully deleted'))
            markup = await queryset_list_keyboard(filter='cars')
        else:
            text = _('An error occurred while deleting a car brand')
            markup = await select_item_menu_keyboard(
                filter='cars',
                action='delete',
                brand_id=brand_id
            )
            await call.message.edit_text(
                    text=text,
                    reply_markup=markup
                )
        await call.message.edit_text(
                    text=_('Car brands:'),
                    reply_markup=markup
                )
    elif color_id:
        color = await delete_car_color(color_id=color_id)
        if color:
            await call.answer(text=_('Car color has been successfully removed'))
            markup = await queryset_list_keyboard(filter='colors')
        else:
            text = _('An error occurred while deleting a car color')
            markup = await select_item_menu_keyboard(
                filter='colors',
                action='delete',
                color_id=color_id
            )
            await call.message.edit_text(
                    text=text,
                    reply_markup=markup
                )
        await call.message.edit_text(
                    text=_('Car colors:'),
                    reply_markup=markup
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
    dp.register_message_handler(
        adding_a_new_item,
        state='add_new_item'
    )
    dp.register_message_handler(
        change_item,
        state='change_item'
    )
    dp.register_callback_query_handler(
        confirm_to_delete,
        delete_item_callback_data.filter()
    )
