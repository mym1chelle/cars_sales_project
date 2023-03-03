from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from tgbot.misc.create_order_states import CreateOrderStates
from tgbot.models.db_commands.order import add_order, get_order
from tgbot.keyboards.create_order_keyboard import (
    select_car_brand_keyboard,
    select_steering_wheel_position_keyboard,
    select_car_color_keyboard,
    get_order_wishes_keyboard
)
from tgbot.keyboards.admin_orders_keyboard import (
        orders_menu_callback_data,
        orders_menu_keyboard,
        order_group_action_menu_keyboard
    )
from tgbot.keyboards.chat_keyboard import chat_callback_data
from tgbot.services.show_order_info import (
    order_info_for_customer,
    order_info_admin_menu_with_status
)
from tgbot.middlewares.translate import _
from bot_setting import bot, dp


async def back_button_in_create_order(
    call: types.CallbackQuery,
    state: FSMContext
):
    await CreateOrderStates.previous()

    get_current_state = await state.get_state()
    print(get_current_state)

    if get_current_state is None:
        return

    elif get_current_state == 'CreateOrderStates:select_car_brand':
        await call.message.edit_text(
            text=_('Choose a car brand:'),
            reply_markup=await select_car_brand_keyboard()
        )

    elif get_current_state == 'CreateOrderStates:select_steering_wheel_position':
        await call.message.edit_text(
            text=_('Choose a steering wheel position:'),
            reply_markup=await select_steering_wheel_position_keyboard()
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


async def back_button_admin_menu_in_state(
        call: types.CallbackQuery,
        callback_data: dict,
        state: FSMContext,
):
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


async def leave_chat_button(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    customer_id = callback_data.get('customer_id')
    seller_id = callback_data.get('seller_id')
    print(seller_id, customer_id)
    state1 = dp.current_state(user=seller_id, chat=seller_id)
    state2 = dp.current_state(user=customer_id, chat=customer_id)
    print(state1, state2)
    await state2.finish()
    await state1.finish()
    await call.message.delete()
    await call.answer(text=_('You have left the chat'))
    alert_message = """
<b>The seller has left the chat</b>

No further messages will be sent.
    """
    await bot.send_message(
        chat_id=customer_id,
        text=alert_message
    )


async def cancel_or_exit(
    call: types.CallbackQuery,
    state: FSMContext
):
    current = await state.get_state()
    print(current)
    if current is None:
        await call.message.delete()
    else:
        await call.message.delete()
        await state.finish()


async def create_order_without_wishes(
    call: types.CallbackQuery,
    state: FSMContext
):
    data = await state.get_data()
    order = await add_order(
        customer_id=data['id_user'],
        steering_wheel_position=data['steering_wheel_position'],
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


def register_back_cancel_order_buttons(dp: Dispatcher):
    dp.register_callback_query_handler(
        back_button_in_create_order,
        text='back_create_order',
        state='*'
    )
    dp.register_callback_query_handler(
        back_button_admin_menu_in_state,
        orders_menu_callback_data.filter(),
        state='send_post'
    )
    dp.register_callback_query_handler(
        back_button_admin_menu_in_state,
        orders_menu_callback_data.filter(),
        state='create_chat'
    )
    dp.register_callback_query_handler(
        cancel_or_exit,
        text='cancel_create_order',
        state='*'
    )
    dp.register_callback_query_handler(
        create_order_without_wishes,
        text='order_without_wishess',
        state=CreateOrderStates.add_order_wishes
    )
    dp.register_callback_query_handler(
        cancel_or_exit,
        text='exit_admin_menu',
        state='*'
    )
    dp.register_callback_query_handler(
        leave_chat_button,
        chat_callback_data.filter(),
        state='live_chat'
    )
