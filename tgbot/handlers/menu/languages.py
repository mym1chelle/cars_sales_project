from aiogram import types, Dispatcher

from tgbot.models.db_commands.user import change_language
from tgbot.keyboards.languages import (
    select_language, change_language_menu_cd
)
from tgbot.middlewares.translate import _


async def start_change_language(message: types.Message):
    await language_menu(message)


async def language_menu(message: types.Message, **kwargs):
    text = _('Choose language:')
    markup = await select_language(
        user_id=message.from_user.id,
        full_name=message.from_user.full_name
    )
    await message.answer(
        text=text,
        reply_markup=markup
    )


async def select_new_language(call: types.CallbackQuery, callback_data: dict):
    language_code = callback_data.get('language_code')
    user = await change_language(
        user_id=call.from_user.id,
        language_code=language_code
    )
    if user:
        await call.message.delete()
        await call.answer(text=_('The language has been changed'))


def registration_language_menu(dp: Dispatcher):
    dp.register_message_handler(start_change_language, commands='language')
    dp.register_callback_query_handler(
        select_new_language, change_language_menu_cd.filter()
    )
