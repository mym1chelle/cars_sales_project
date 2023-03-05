bot:
	poetry run python bot.py

makemigrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

superuser:
	poetry run python manage.py createsuperuser

run:
	poetry run python manage.py runserver

extract:
	poetry run pybabel extract . -o tgbot/locales/testbot.pot

update:
	poetry run pybabel update -d tgbot/locales -D testbot -i tgbot/locales/testbot.pot

compile:
	poetry run pybabel compile -d tgbot/locales -D testbot

install:
	poetry install

lint:
	poetry run flake8 tgbot tgbot_django