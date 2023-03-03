import asyncio
import logging
from tgbot.config import django_setting

# setting environment variable and allowing to use ASGI
django_setting()

# from aiogram import Dispatcher
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.contrib.fsm_storage.redis import RedisStorage2


from tgbot.filters.seller_filter import SellerFilter
from tgbot.handlers.create_order import register_create_order
from tgbot.handlers.base import register_back_cancel_order_buttons
from tgbot.handlers.admin_orders_menu import register_admin_menu
from tgbot.handlers.data import register_data_menu
from tgbot.handlers.send_post import register_sending_post
from tgbot.handlers.chat_with_seller_and_customer import (
    register_chat_with_customer
    )
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.translate import i18n
from bot_setting import bot, config, dp

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(i18n)
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(SellerFilter)


def register_all_handlers(dp):
    register_create_order(dp)
    register_admin_menu(dp)
    register_data_menu(dp)
    register_back_cancel_order_buttons(dp)
    register_sending_post(dp)
    register_chat_with_customer(dp)


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
