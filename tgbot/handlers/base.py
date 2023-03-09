from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.misc.create_order_states import CreateOrderStates
from tgbot.models.db_commands.order import add_order, get_order
from tgbot.models.db_commands.car import get_car_brand
from tgbot.models.db_commands.color import get_car_color
from tgbot.keyboards.order import (
    select_car_brand_keyboard,
    select_car_color_keyboard,
    get_order_wishes_keyboard
)
from tgbot.keyboards.admin_orders import (
    orders_menu_callback_data,
    orders_menu_keyboard,
    order_group_action_menu_keyboard
)
from tgbot.keyboards.chat import chat_callback_data
from tgbot.keyboards.data import (
    data_menu_callback_data,
    queryset_list_keyboard,
    select_item_menu_keyboard
)
from tgbot.services.order_info import (
    order_info_for_customer,
    order_info_admin_menu_with_status
)
from tgbot.middlewares.translate import _
from bot_setting import bot, dp


async def back_button_in_create_order(
    call: types.CallbackQuery,
    state: FSMContext
):
    """
    Back button to navigate through the states when creating an order
    """
    await CreateOrderStates.previous()

    get_current_state = await state.get_state()

    if get_current_state is None:
        return

    elif get_current_state == 'CreateOrderStates:select_car_brand':
        await call.message.edit_text(
            text=_('Choose a car brand:'),
            reply_markup=await select_car_brand_keyboard()
        )
    elif get_current_state == 'CreateOrderStates:select_car_color':
        await call.message.edit_text(
            text=_('Choose car color:'),
            reply_markup=await select_car_color_keyboard()
        )
    elif get_current_state == 'CreateOrderStates:add_order_wishes':
        await call.message.edit_text(
            text=_('Add a comment to the order:'),
            reply_markup=await get_order_wishes_keyboard()
        )


async def back_button_for_states(
        call: types.CallbackQuery,
        callback_data: dict,
        state: FSMContext,
):
    """
    Function to navigate back through states. Used in:

    — admin menu
    — data menu
    """
    get_current_state = await state.get_state()

    if get_current_state is None:
        return
    elif get_current_state == 'send_post':
        await state.finish()
        await call.message.edit_text(
            text=_('Menu:'),
            reply_markup=await orders_menu_keyboard(
                user_id=call.from_user.id
            )
        )
    elif get_current_state == 'create_chat':
        await state.finish()
        order_id = callback_data.get('order_id')
        order = await get_order(order_id=order_id)
        show_order = order_info_admin_menu_with_status(order=order)
        await call.message.edit_text(
            text=show_order,
            reply_markup=await order_group_action_menu_keyboard(
                filter='selected',
                order_id=order_id,
                user_id=call.from_user.id
            )
        )
    elif get_current_state == 'add_new_item':
        await state.finish()
        filter = callback_data.get('filter')
        if filter == 'cars':
            text = _('Car brands:')
        elif filter == 'colors':
            text = _('Car colors:')
        markup = await queryset_list_keyboard(filter=filter)
        await call.message.edit_text(
            text=text,
            reply_markup=markup
        )
    elif get_current_state == 'change_item':
        await state.finish()
        filter = callback_data.get('filter')
        action = callback_data.get('action')
        brand_id = callback_data.get('brand_id')
        color_id = callback_data.get('color_id')
        if brand_id:
            car_brand = await get_car_brand(brand_id=brand_id)
            text = car_brand.name
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


async def leave_chat_button(
        call: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    """Ending a chat from the seller"""
    customer_id = callback_data.get('customer_id')
    seller_id = callback_data.get('seller_id')
    state_seller = dp.current_state(user=seller_id, chat=seller_id)
    state_customer = dp.current_state(user=customer_id, chat=customer_id)
    await state_customer.finish()
    await state_seller.finish()
    await call.message.delete()
    await call.answer(text=_('You have left the chat'))
    alert_message = _("""
<b>The seller has left the chat</b>

No further messages will be sent.""")
    await bot.send_message(
        chat_id=customer_id,
        text=alert_message
    )


async def cancel_or_exit_buttons(
    call: types.CallbackQuery,
    state: FSMContext
):
    """Implementing cancel and exit buttons"""
    current = await state.get_state()
    if current is None:
        await call.message.delete()
    else:
        await call.message.delete()
        await state.finish()


async def create_order_without_wishes(
    call: types.CallbackQuery,
    state: FSMContext
):
    """Creating an order without adding comments to the order"""
    data = await state.get_data()
    order = await add_order(
        customer_id=data['id_user'],
        car_brand_id=data['car_brand_id'],
        color_id=data['car_color_id'],
    )
    show_order = order_info_for_customer(order=order)
    text = _("""
Your order
{order}
has been created""").format(order=show_order)
    await call.message.edit_text(
        text=text
    )
    await state.finish()


def register_cancel_or_exit_buttons(dp: Dispatcher):
    dp.register_callback_query_handler(
        cancel_or_exit_buttons,
        text='cancel_create_order',
        state='*'
    )
    dp.register_callback_query_handler(
        cancel_or_exit_buttons,
        text='cancel_create_order',
        state='*'
    )
    dp.register_callback_query_handler(
        cancel_or_exit_buttons,
        text='exit_admin_menu',
        state='*'
    )
    dp.register_callback_query_handler(
        cancel_or_exit_buttons,
        text='exit_data_menu',
        state='*'
    )
    dp.register_callback_query_handler(
        cancel_or_exit_buttons,
        text='exit_language_menu'
    )


def register_back_button_for_states(dp: Dispatcher):
    dp.register_callback_query_handler(
        back_button_for_states,
        orders_menu_callback_data.filter(),
        state='send_post'
    )
    dp.register_callback_query_handler(
        back_button_for_states,
        orders_menu_callback_data.filter(),
        state='create_chat'
    )
    dp.register_callback_query_handler(
        back_button_for_states,
        data_menu_callback_data.filter(),
        state='add_new_item'
    )
    dp.register_callback_query_handler(
        back_button_for_states,
        data_menu_callback_data.filter(),
        state='change_item'
    )


def register_of_additional_ordeer_buttons(dp: Dispatcher):
    dp.register_callback_query_handler(
        back_button_in_create_order,
        text='back_create_order',
        state='*'
    )
    dp.register_callback_query_handler(
        create_order_without_wishes,
        text='order_without_wishess',
        state=CreateOrderStates.add_order_wishes
    )
    dp.register_callback_query_handler(
        leave_chat_button,
        chat_callback_data.filter(),
        state='live_chat'
    )
