from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_setting import bot, dp
from tgbot.middlewares.translate import _
from tgbot.models.db_commands.user import get_user
from tgbot.keyboards.chat import leave_chat_with_the_customer_keyboard


async def create_chat_with_customer(
    message: types.Message,
    state: FSMContext
):
    data = await state.get_data()
    message_id = data.get('message_id')
    id_customer = data.get('customer_id')
    seller_id = message.from_user.id
    customer = await get_user(id=id_customer)
    print(seller_id, customer.user_id)
    await bot.edit_message_text(
        chat_id=seller_id,
        message_id=message_id,
        text=_('You started a chat with a client'),
        reply_markup=await leave_chat_with_the_customer_keyboard(
            seller_id=seller_id,
            customer_id=customer.user_id
        )
    )

    first_message_in_chat = _("""
<b>Message from the seller</b>

{message}
""").format(message=message.text)

    await bot.send_message(
        text=first_message_in_chat,
        chat_id=customer.user_id
    )
    
    async with state.proxy() as data:
        data['customer_id'] = customer.user_id
    await state.set_state('live_chat')

    #  Set the state to the client for messaging
    state_customer = dp.current_state(
        chat=customer.user_id, user=customer.user_id
        )
    print(state_customer)
    async with state_customer.proxy() as data:
        data['seller_id'] = message.from_user.id
    await state_customer.set_state('live_chat')
    s = dp.current_state(chat=customer.user_id, user=customer.user_id)
    print(s)


async def seller_and_customer_сhat(
        message: types.Message,
        state: FSMContext
        ):
    print(message.text)
    data = await state.get_data()
    seller_id = data.get('seller_id')
    print(seller_id)
    customer_id = data.get('customer_id')
    print(customer_id)
    if customer_id:
        print('Сообщение от customer')
        await bot.send_message(chat_id=customer_id, text=message.text)
    elif seller_id:
        print('Сообщение от seller')
        await bot.send_message(chat_id=seller_id, text=message.text)


def register_chat_with_customer(dp: Dispatcher):
    dp.register_message_handler(create_chat_with_customer, state='create_chat')
    dp.register_message_handler(seller_and_customer_сhat, state='live_chat')
