from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from tgbot.models.db_commands.user import is_seller
from tgbot.middlewares.translate import _


class SellerFilter(BoundFilter):
    """The filter checks if the user is a seller"""
    async def check(self, message: types.Message) -> bool:
        seller = await is_seller(user_id=message.from_user.id)
        if not seller:
            text = _('You do not have sufficient rights to use this feature')
            await message.answer(text=text)
        return seller
