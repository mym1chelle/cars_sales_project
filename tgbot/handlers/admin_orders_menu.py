from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.middlewares.translate import _
from tgbot.filters.seller_filter import SellerFilter
from tgbot.services.show_order_info import (
    order_info_admin_menu_with_status,
    order_info_admin_menu_without_status,
    order_info_string
)
from tgbot.models.db_commands.order import (
    get_order,
    select_or_unselect_order,
    change_order_status
)
from tgbot.keyboards.admin_orders_keyboard import (
    orders_menu_callback_data,
    orders_menu_keyboard,
    group_orders_keyboard,
    order_group_action_menu_keyboard,
    only_one_order_menu_keyboard,
    after_change_status_menu_keyboard
)


async def show_admin_menu(message: types.Message):
    await main_page_menu(message)


async def main_page_menu(
        message: types.Message | types.CallbackQuery, **kwargs
):
    """
    Admin main menu

    Contains buttons:
    — Availible orders (count orders)
    — Selected orders (count orders)
    — Send post
    — Order data (future)
    — Exit
    """
    user_id = message.from_user.id
    markup = await orders_menu_keyboard(user_id=user_id)
    if isinstance(message, types.Message):
        await message.answer(text=_('Menu:'), reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text(text=_('Menu:'), reply_markup=markup)


async def list_orders_menu(
        call: types.CallbackQuery,
        state: FSMContext,
        filter,
        **kwargs):
    """List of all available orders or list of all selected orders.
    Each button is an order"""
    user_id = call.from_user.id
    markup = await group_orders_keyboard(filter=filter, user_id=user_id)
    if filter == 'send_post':
        await call.message.edit_text(text=_('Enter post text:'),
                                     reply_markup=markup)
        async with state.proxy() as data:
            # I save the ID of messages so that I can delete it later
            data['message_id'] = call.message.message_id
        await state.set_state('send_post')
    else:
        await call.message.edit_text(text=_('Menu:'), reply_markup=markup)


async def show_order_menu(
        call: types.CallbackQuery, filter, order_id, **kwargs
):
    """Menu of actions with a specific order.
    Depends on whether the selected order is or not

    Contains buttons:

    if order is selected:
    — Write to customer
    — Unselect
    — Change order status
    — Back
    — Exit

    if order is unselected:
    — Select order
    — Back
    — Exit
    """
    user_id = call.from_user.id
    markup = await order_group_action_menu_keyboard(
        filter=filter, order_id=order_id, user_id=user_id
    )
    order = await get_order(order_id=order_id)
    if filter == 'selected':
        text = order_info_admin_menu_with_status(order=order)
    else:
        text = order_info_admin_menu_without_status(order=order)
    await call.message.edit_text(text=text, reply_markup=markup)


async def some_action_with_order(
        call: types.CallbackQuery,
        state: FSMContext,
        order_id,
        filter,
        customer_id,
        **kwargs):
    """
    Three order manipulations are processed here:
    — Select order
    — Unselect order,
    — Change the status of an order

    At the same level, a message is sent to the customer
    """
    user_id = call.from_user.id
    if filter == 'unselected':
        order = await select_or_unselect_order(
            order_id=order_id, user_id=user_id
        )
        show_order = order_info_string(order)
        text = _('{order} selected').format(order=show_order)
    elif filter == 'selected':
        order = await select_or_unselect_order(
            order_id=order_id
        )
        show_order = order_info_string(order)
        text = _('{order} selection removed').format(order=show_order)
    elif filter == 'change_order_status':
        text = _('Select order status:')
    markup = await only_one_order_menu_keyboard(
        order_id=order_id,
        user_id=user_id,
        filter=filter,
        customer_id=customer_id
    )
    if filter == 'send_message':
        text = _('Enter your message:')
        await call.message.edit_text(text=text, reply_markup=markup)
        async with state.proxy() as data:
            data['customer_id'] = customer_id
            # I save the ID of messages so that I can delete it later
            data['message_id'] = call.message.message_id
        await state.set_state('create_chat')
    else:
        await call.message.edit_text(text=text, reply_markup=markup)


async def select_new_order_status_or_send_message(
        call: types.CallbackQuery,
        filter,
        order_id,
        order_status,
        user_id,
        **kwargs
):
    """Processes the received order status and its update"""

    order = await change_order_status(
        order_id=order_id,
        status=order_status
    )
    print(order)
    markup = await after_change_status_menu_keyboard(
        filter=filter,
        order_id=order_id,
        user_id=user_id
    )
    show_order = order_info_string(order)
    text = _('{order} status has been changed').format(order=show_order)
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
    orders = callback_data.get('orders')
    order_id = callback_data.get('order_id')
    user_id = callback_data.get('user_id')
    filter = callback_data.get('filter')
    customer_id = callback_data.get('customer_id')
    order_status = callback_data.get('order_status')

    levels = {
        '0': main_page_menu,
        '1': list_orders_menu,
        '2': show_order_menu,
        '3': some_action_with_order,
        '4': select_new_order_status_or_send_message,
    }
    current_level_func = levels[current_level]

    await current_level_func(
        call=call,
        message=call,
        state=state,
        orders=orders,
        order_id=order_id,
        user_id=user_id,
        filter=filter,
        customer_id=customer_id,
        order_status=order_status
    )


def register_admin_menu(dp: Dispatcher):
    dp.register_message_handler(
        show_admin_menu, SellerFilter(), commands='admin'
    )
    dp.register_callback_query_handler(
        navigate, orders_menu_callback_data.filter())
