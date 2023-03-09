from dataclasses import dataclass
import os
import django
from environs import Env


@dataclass
class DataBaseConfig:
    host: str
    password: str
    user: str
    database: str
    port: str


@dataclass
class BotConfig:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class DjangoConfig:
    secret_key: str
    use_debug: bool
    allowed_hosts: list[str]
    internal_ips: list[str]


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: BotConfig
    db: DataBaseConfig
    django: DjangoConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=BotConfig(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DataBaseConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
            port=env.str('DB_PORT')
        ),
        django=DjangoConfig(
            secret_key=env.str('SECRET_KEY'),
            use_debug=env.bool('DEBUG'),
            allowed_hosts=list(map(str, env.list('ALLOWED_HOSTS'))),
            internal_ips=list(map(str, env.list('INTERNAL_IPS')))
        ),
        misc=Miscellaneous()
    )


def django_setting():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tgbot_django.settings')
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    django.setup()
