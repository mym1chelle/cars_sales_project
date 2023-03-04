from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.models.db_commands.user import get_language
from tgbot.middlewares.translate import _


change_language_menu_cd = CallbackData(
    'language_menu',
    'language_code'
)


def make_callback_data(
        language_code,
):
    return change_language_menu_cd.new(
        language_code=language_code
    )


def make_language_button(text_button: str, language_code: str):
    button = InlineKeyboardButton(
        text=text_button,
        callback_data=make_callback_data(
            language_code=language_code
        ))
    return button


async def select_language(user_id: int, full_name: str):
    markup = InlineKeyboardMarkup(row_width=1)
    language_code = await get_language(user_id, full_name)
    if language_code == 'ru':
        buttons = [
            make_language_button(text_button='English 🇺🇸', language_code='en'),
            make_language_button(text_button='عربي 🇸🇦', language_code='ar'),
            make_language_button(text_button='עִברִית 🇮🇱', language_code='he')
        ]
        markup.add(*buttons)
    elif language_code == 'en':
        buttons = [
            make_language_button(text_button='Русский 🇷🇺', language_code='ru'),
            make_language_button(text_button='عربي 🇸🇦', language_code='ar'),
            make_language_button(text_button='עִברִית 🇮🇱', language_code='he')
        ]
        markup.add(*buttons)
    elif language_code == 'ar':
        buttons = [
            make_language_button(text_button='English 🇺🇸', language_code='en'),
            make_language_button(text_button='Русский 🇷🇺', language_code='ru'),
            make_language_button(text_button='עִברִית 🇮🇱', language_code='he')
        ]
        markup.add(*buttons)
    elif language_code == 'he':
        buttons = [
            make_language_button(text_button='English 🇺🇸', language_code='en'),
            make_language_button(text_button='عربي 🇸🇦', language_code='ar'),
            make_language_button(text_button='Русский 🇷🇺', language_code='ru')
        ]
        markup.add(*buttons)
    markup.row(
        InlineKeyboardButton(
            text=_('Exit'),
            callback_data='exit_language_menu'),
    )
    return markup
