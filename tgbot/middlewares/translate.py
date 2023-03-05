from pathlib import Path
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types
import typing

from tgbot.models.db_commands.user import get_language


I18N_DOMAIN = 'testbot'

BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'


class Localization(I18nMiddleware):
    async def get_user_locale(
            self, action: str, args: typing.Tuple[typing.Any]) -> str:
        user: types.User = types.User.get_current()
        language = await get_language(
            user_id=user.id, full_name=user.full_name
        )
        return language or str(user.locale)


i18n = Localization(I18N_DOMAIN, LOCALES_DIR)

_ = i18n.gettext
