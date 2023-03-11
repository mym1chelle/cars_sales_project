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
    """
    Creating a chat with the customer.
    After sending the message, it displays a
    keyboard with the "Leave chat" button.
    The message can contain any files.
    """
    data = await state.get_data()
    message_id = data.get('message_id')
    id_customer = data.get('customer_id')
    seller_id = message.from_user.id
    customer = await get_user(id=id_customer)
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
<b>Message from the seller</b>""")

    await bot.send_message(
        text=first_message_in_chat,
        chat_id=customer.user_id
    )
    await message.copy_to(
        chat_id=customer.user_id
    )
    async with state.proxy() as data:
        data['customer_id'] = customer.user_id
    await state.set_state('live_chat')

    #  Set the state to the client for messaging
    state_customer = dp.current_state(
        chat=customer.user_id, user=customer.user_id
    )
    async with state_customer.proxy() as data:
        data['seller_id'] = message.from_user.id
    await state_customer.set_state('live_chat')


async def seller_and_customer_сhat(
        message: types.Message,
        state: FSMContext
):
    """Chat between seller and customer.
    In the chat, you can send messages containing any files.
    After the chat is ended by the seller, the messages are not processed.
    """
    data = await state.get_data()
    seller_id = data.get('seller_id')
    customer_id = data.get('customer_id')
    if customer_id:
        await message.copy_to(chat_id=customer_id)
    elif seller_id:
        await message.copy_to(chat_id=seller_id)


def register_chat_with_customer(dp: Dispatcher):
    dp.register_message_handler(
        create_chat_with_customer,
        state='create_chat',
        content_types=types.ContentTypes.ANY
    )
    dp.register_message_handler(
        seller_and_customer_сhat,
        state='live_chat',
        content_types=types.ContentTypes.ANY
    )
