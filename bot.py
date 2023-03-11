import asyncio
import logging
from tgbot.config import django_setting

# setting environment variable and allowing to use ASGI
django_setting()


from tgbot.filters.seller_filter import SellerFilter

from tgbot.handlers.menu.admin_orders import register_admin_menu
from tgbot.handlers.menu.languages import registration_language_menu

from tgbot.handlers.order import register_create_order
from tgbot.handlers.post import register_sending_post
from tgbot.handlers.chat import register_chat_with_customer

from tgbot.handlers.base import register_cancel_or_exit_buttons
from tgbot.handlers.base import register_back_button_for_states
from tgbot.handlers.base import register_of_additional_ordeer_buttons

from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.translate import i18n
from bot_setting import bot, config, dp
from tgbot.services.set_bot_commands import set_default_commands


logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(i18n)
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(SellerFilter)


def register_all_handlers(dp):
    register_admin_menu(dp)
    registration_language_menu(dp)
    register_create_order(dp)
    register_sending_post(dp)
    register_chat_with_customer(dp)
    register_cancel_or_exit_buttons(dp)
    register_back_button_for_states(dp)
    register_of_additional_ordeer_buttons(dp)


async def main(bot, config):
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = config

    bot['config'] = config
    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    await set_default_commands(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        # another way to use session since the old settings are deprecated
        session = await bot.get_session()
        await session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main(
            bot=bot,
            config=config
        ))
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
