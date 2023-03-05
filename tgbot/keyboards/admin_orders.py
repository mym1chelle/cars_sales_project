from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.models.db_commands.order import (
    count_unselected_orders,
    count_selected_orders,
    all_selected_orders,
    all_unselected_orders,
    get_order
)
from tgbot.services.order_info import order_info_string
from tgbot.middlewares.translate import _


orders_menu_callback_data = CallbackData(
    'orders_menu',
    'level',
    'filter',
    'orders',
    'order_id',
    'user_id',
    'customer_id',
    'order_status'
)


def make_menu_callback_data(
        level,
        filter='',
        orders='',
        user_id='',
        order_id='',
        customer_id='',
        order_status=''
):
    return orders_menu_callback_data.new(
        level=level,
        filter=filter,
        user_id=user_id,
        orders=orders,
        order_id=order_id,
        customer_id=customer_id,
        order_status=order_status
    )


async def orders_menu_keyboard(user_id: int):
    """
    Displays two buttons that offer to select all available orders
    or orders selected by the current user

    user_id: CallBackQuery.from_user.id
    """
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)
    count_unselected = await count_unselected_orders()
    count_selected = await count_selected_orders(user_id=user_id)
    buttons = [
        InlineKeyboardButton(
            text=_('Available orders ({count})').format(
                count=count_unselected),
            callback_data=make_menu_callback_data(
                level=CURRENT_LEVEL + 1,
                filter='unselected'
            )),
        InlineKeyboardButton(
            text=_('Selected orders ({count})').format(
                count=count_selected
            ),
            callback_data=make_menu_callback_data(
                level=CURRENT_LEVEL + 1,
                filter='selected'
            )),
        InlineKeyboardButton(text=_('Send post'),
                             callback_data=make_menu_callback_data(
                                 level=CURRENT_LEVEL + 1,
                                 filter='send_post'
        ))
    ]
    markup.add(*buttons)
    markup.row(
        InlineKeyboardButton(
            text=_('Exit'),
            callback_data='exit_admin_menu'),
    )
    return markup


async def group_orders_keyboard(filter: str, user_id: int):
    """
    Displays all available orders or all selected orders,
    depending on what was selected in the previous level

    filter: callback data in the previous level
    user_id: CallBackQuery.from_user.id
    """
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=2)
    if filter == 'unselected':
        orders = await all_unselected_orders()
        for order in orders:
            button_text = _('Order {order}').format(
                order=order_info_string(order)
            )
            callback_data = make_menu_callback_data(
                level=CURRENT_LEVEL + 1,
                order_id=order.id,
                filter=filter
            )
            markup.insert(
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=callback_data
                )
            )
    elif filter == 'selected':
        orders = await all_selected_orders(user_id=user_id)
        for order in orders:
            button_text = _('Order {order}').format(
                order=order_info_string(order)
            )
            callback_data = make_menu_callback_data(
                level=CURRENT_LEVEL + 1,
                order_id=order.id,
                filter=filter
            )
            markup.insert(
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=callback_data
                )
            )
    elif filter == 'send_post':
        # This is necessary so that after sending the post
        # to get the exit button and back
        pass
    markup.row(
        InlineKeyboardButton(
            text=_('Back'),
            callback_data=make_menu_callback_data(
                level=CURRENT_LEVEL - 1,
                user_id=user_id
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Exit'),
            callback_data='exit_admin_menu'),
    )
    return markup


async def order_group_action_menu_keyboard(filter, order_id, user_id):
    """Displays buttons with valid order actions in the group selected
    at the zero level

    filter: callback data in the previous level
    order_id: callback data in the previous level
    user_id: CallBackQuery.from_user.id
    """
    CURRENT_LEVEL = 2
    order = await get_order(order_id=order_id)
    markup = InlineKeyboardMarkup(row_width=1)
    if filter == 'unselected':
        markup.row(
            InlineKeyboardButton(
                text=_('Select order'),
                callback_data=make_menu_callback_data(
                    level=CURRENT_LEVEL + 1,
                    order_id=order.id,
                    filter=filter
                )
            )
        )
        markup.row(
            InlineKeyboardButton(
                text=_('Back'),
                callback_data=make_menu_callback_data(
                    level=CURRENT_LEVEL - 1,
                    user_id=user_id,
                    filter=filter
                )
            )
        )
    elif filter == 'selected':
        buttons = [
            InlineKeyboardButton(
                text=_('Chat with the customer'),
                callback_data=make_menu_callback_data(
                    level=CURRENT_LEVEL + 1,
                    order_id=order.id,
                    customer_id=order.customer_id,
                    filter='send_message'
                )
            ),
            InlineKeyboardButton(
                text=_('Unselect'),
                callback_data=make_menu_callback_data(
                    level=CURRENT_LEVEL + 1,
                    order_id=order.id,
                    filter=filter
                )
            ),
            InlineKeyboardButton(
                text=_('Change order status'),
                callback_data=make_menu_callback_data(
                    level=CURRENT_LEVEL + 1,
                    order_id=order.id,
                    filter='change_order_status'
                )
            )
        ]
        markup.add(*buttons)
        markup.row(
            InlineKeyboardButton(
                text=_('Back'),
                callback_data=make_menu_callback_data(
                    level=CURRENT_LEVEL - 1,
                    user_id=user_id,
                    filter=filter
                )
            )
        )
    markup.row(
        InlineKeyboardButton(
            text=_('Exit'),
            callback_data='exit_admin_menu'),
    )
    return markup


async def only_one_order_menu_keyboard(
        filter,
        order_id,
        user_id,
        customer_id=None
):
    """Displays buttons for changing the order status
    (if the required filter is accepted),
    for all other filters displays back and exit buttons

    filter: callback data in the previous level
    order_id: callback data in the previous level
    user_id: CallBackQuery.message.from_user.id
    """
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row_width=1)
    if filter == 'change_order_status':
        open_status_button = InlineKeyboardButton(
            text=_('open'),
            callback_data=make_menu_callback_data(
                level=CURRENT_LEVEL + 1,
                order_id=order_id,
                order_status='open'
            )
        )
        in_progrss_status_button = InlineKeyboardButton(
            text=_('in progress'),
            callback_data=make_menu_callback_data(
                level=CURRENT_LEVEL + 1,
                order_id=order_id,
                order_status='in_progress'
            )
        )
        close_status_button = InlineKeyboardButton(
            text=_('close'),
            callback_data=make_menu_callback_data(
                level=CURRENT_LEVEL + 1,
                order_id=order_id,
                order_status='close'
            )
        )

        order = await get_order(order_id=order_id)
        if order.order_status == 'open':
            buttons = [
                in_progrss_status_button,
                close_status_button
            ]
        elif order.order_status == 'in_progress':
            buttons = [
                open_status_button,
                close_status_button,
            ]
        elif order.order_status == 'close':
            buttons = [
                open_status_button,
                in_progrss_status_button
            ]
        else:
            buttons = [
                open_status_button,
                in_progrss_status_button,
                close_status_button
            ]
        markup.add(*buttons)
    elif filter == 'unselected' or filter == 'selected':
        # After selecting an order or canceling the selection,
        # you need to return not to the previous level,
        # but two levels higher in the general menu of orders
        markup.row(
            InlineKeyboardButton(
                text=_('Back'),
                callback_data=make_menu_callback_data(
                    level=CURRENT_LEVEL - 2,
                    user_id=user_id,
                    filter=filter,
                    order_id=order_id
                )
            )
        )
    else:
        markup.row(
            InlineKeyboardButton(
                text=_('Back'),
                callback_data=make_menu_callback_data(
                    level=CURRENT_LEVEL - 1,
                    user_id=user_id,
                    filter='selected',
                    order_id=order_id
                )
            )
        )
        markup.row(
            InlineKeyboardButton(
                text=_('Exit'),
                callback_data='exit_admin_menu'),
        )
    return markup


async def after_change_status_menu_keyboard(
        filter,
        order_id,
        user_id
):
    """Displays exit and back buttons after order status change

    order_id: callback data in the previous level
    user_id: CallBackQuery.message.from_user.id
    """
    CURRENT_LEVEL = 4
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text=_('Back'),
            callback_data=make_menu_callback_data(
                level=CURRENT_LEVEL - 2,
                user_id=user_id,
                filter='selected',
                order_id=order_id
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Exit'),
            callback_data='exit_admin_menu'),
    )
    return markup
