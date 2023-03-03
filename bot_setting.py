from tgbot.config import load_config
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
dp = Dispatcher(bot, storage=storage)