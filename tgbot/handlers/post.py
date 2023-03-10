from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_setting import bot
from tgbot.middlewares.translate import _
from tgbot.models.db_commands.user import get_all_clients_user_ids
from tgbot.keyboards.admin_orders import group_orders_keyboard


async def sending_post_for_all_clients(
    message: types.Message,
    state=FSMContext
):
    """
    Sending a post to all users. Post can contain any files.
    """
    user_id = message.from_user.id
    all_client_ids = await get_all_clients_user_ids()
    data = await state.get_data()
    message_id = data.get('message_id')
    await bot.delete_message(
        chat_id=user_id,
        message_id=message_id
    )
    if all_client_ids:
        for id in all_client_ids:
            await message.copy_to(
                chat_id=id
            )
        await message.answer(
            text=_('Post published'),
            reply_markup=await group_orders_keyboard(
                user_id=user_id, filter='send_post'
            )
        )
    else:
        await message.answer(
            text=_('Clients not found'),
            reply_markup=await group_orders_keyboard(
                user_id=user_id, filter='send_post'
            )
        )
    await message.delete()
    await state.finish()


def register_sending_post(dp: Dispatcher):
    dp.register_message_handler(
        sending_post_for_all_clients, state='send_post',
        content_types=types.ContentTypes.ANY
    )
