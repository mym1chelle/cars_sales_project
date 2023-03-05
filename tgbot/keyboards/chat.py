from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.middlewares.translate import _


chat_callback_data = CallbackData(
    'chat_menu',
    'seller_id',
    'customer_id'
)


def make_chat_callback_data(
        seller_id,
        customer_id=''
):
    return chat_callback_data.new(
        seller_id=seller_id,
        customer_id=customer_id
    )


async def leave_chat_with_the_customer_keyboard(
        seller_id: int, customer_id: int
):
    markup = InlineKeyboardMarkup(row=1)
    markup.row(
        InlineKeyboardButton(
            text=_('Leave the chat'),
            callback_data=make_chat_callback_data(
                seller_id=seller_id, customer_id=customer_id)
        )
    )
    return markup
