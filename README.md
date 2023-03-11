# Телеграм-бот для продажи автомобилей

## Установка
1. [Установить Poetry](https://python-poetry.org/docs/)
2. [Установить Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
3. Клонировать проект в локальную директорию:
```
git clone git@github.com:mym1chelle/cars_sales_project.git
```
4. В директории клонированного проекта, установить зависимости командой:
```
make install
```
5. Создать файл `.env` и внести туда данные для работы проекта:
```
BOT_CONTAINER_NAME=car_bot
BOT_IMAGE_NAME=botimage_name
BOT_NAME=test_bot
BOT_TOKEN=bot_token
USE_REDIS=False
ADMINS=admin_ids_list

DB_USER=user
DB_PASS=password
DB_NAME=database_name
DB_HOST=localhost
DB_PORT=5432

SECRET_KEY=django_secret_key
DEBUG=True
ALLOWED_HOSTS=allowed_hosts_list
```


## Запуск проекта
Сервер Djnago запускается командой:
```
make run
```
Бот запускается командой:
```
make bot
```
## Запуск проекта в Docker
В данном проекте присутствуют файлы `Dockerfile` и `docker-compose.yml` для запуска проекта в Docker.
Для реализации этой возможности сначала следует установить [Docker](https://docs.docker.com/get-docker/)

*Примечание: в файле `settings.py` нужно изменить значение ` HOST` на `'db'`*

## Django

Создание миграций выполняется командой:
```
make makemigrations
```

Применение миграций выполняется командой:
```
make migrate
```

Создание супер-пользователя выполняется командой:
```
make superuser
```
Админ-панель для управления данными проекта располагается по адресу:
`{domen_name}/admin/`
где `domen_name` – имя используемого домена

## Команды
#### Команды, доступные заказчику

* `/start` — запускает создание заказа
* `/language` — выводит клавиатуру переключения языка в боте

#### Скрытая команда
Команда `/admin` выводит меню управления заказами и доступна только пользователям со статусом продавца (`seller`). При попытке пользователя со статусом клиент (`client`) ввести эту команду, будет отправлено сообщение с предупреждением об ограничении прав доступа.

## Команда `/start`
Команда формирует заказ пользователя.
Сначала происходит проверка есть ли в базе данных текущий пользователь: 
* если такой пользователь существует, то бот берет информацию о нем для создания заказа
* если пользователь не был найден, то он добавляется в базу данных

### Выбор марки автомобиля

![Car brand](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/select_car_brand.png)

При нажатии на кнопку с названием марки автомобиля осуществляется переход в меню на уровень ниже с выбором модели автомобиля соответствующей марки.

***На данном шаге и последующих шагах присутствует кнопка «Отмена» которая прекращает создание заказа***

### Выбор модели автомобиля

![Car color](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/select_car_model.png)

При нажатии на кнопку с названием модели автомобиля осуществляется переход в меню на уровень ниже где выводится изображение (одно, несколько или ни одного) автомобиля.

### Меню модели автомобиля

![Car model menu](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/car_model_menu.png)

В зависимости от количества изображений у модели автомобиля появляются кнопки пагинации, с помощью которых можно перемещаться по изображениям.

После выбора осуществляется переход к следующему шагу.

***На данном шаге и последующих шагах присутствует кнопка «Назад» которая перемещает к предыдущему шагу в заказе***

### Добавление комментария к заказу

![Comment](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/add_comment.png)

При отправке сообщения боту создастся комментарий к заказу.
Нажатие на кнопку «Без комментария» создаст заказ без комментария.

### Окончание формирования заказа

Выводится базовая информация о созданном заказе

![Order](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/end_create_order.png)


## Команда `/language`
Команда вызывает меню с выбором используемого языка

Сначала происходит проверка есть ли в базе данных текущий пользователь:
* если такой пользователь существует, то бот берет информацию о нем для измененения языка
* если пользователь не был найден, то он добавляется в базу данных.

Язык по-умолчанию — русский.

Бот поддерживает следующие языки:

* английский
* русский
* арабский
* иврит

Кнопки для смены языка выводятся относительно установленного языка для пользователя —
выводятся все доступные языки, кроме текущего.

![Languages](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/languages.png)
При нажатии на кнопку с названием языка, изменяется текущий язык пользователя на выбранный и выводится уведомление о смене языка.

![New language](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/new_language.png)

## Команда `/admin`

Открывает меню для управления заказами

![Main menu](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/main_admin_menu.png)

В меню есть следующие кнопки:

* Доступные заказы. В скобках — количество доступных заказов
* Выбранные заказы. В скобках — количество выбранных заказов
* Отправить пост

***На данном шаге и последующих шагах присутствует кнопка «Выйти» которая выходит из меню администратора***

### Доступные заказы

Выводит список всех заказов, которые еще не выбрал ни один продавец.

![Unselected orders](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/unselected_orders.png)

При нажатии на кнопку с заказом, переходим в меню с действиями к данному заказу

***На данном шаге и последующих шагах присутствует кнопка «Назад» которая перемещает в меню на уровень выше***

#### Меню действий с невыбранным заказом
![Unselected order menu](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/unselected_order_menu.png)

Выводит базовую информацию о заказе и кнопку выбора данного заказа

#### Выбор заказа
![Select order](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/select_order.png)

При нажатии на кнопку «Выбрать заказ» выводит сообщении о заказе, который был выбран

### Выбранные заказы
Выводит список всех заказов, которые были выбранны текущим пользователем.

При нажатии на кнопку с заказом, переходим в меню с действиями к заказу

![Selected orders](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/selected_orders.png)

***На данном шаге и последующих шагах присутствует кнопка «Назад» которая перемещает в меню на уровень выше***

#### Меню действий с выбранным заказом
![Selected order menu](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/selected_order_menu.png)

Выводит базовую информацию о заказе с комментарием к данному заказу (если комментарий есть) и кнопки:

* Чат с заказчиком
* Отменить выбор заказа
* Изменить статус заказа

#### Чат с заказчиком
![Chat](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/chat.png)

При отправке сообщения создается чат с заказчиком. После отправки сообщения заказчику, продавцу выводится сообщение о созданном чате с кнопкой «Выйти из чата»

*Окно продавца:*
![Chat seller](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/chat_seller.png)


Заказчику приходит сообщение с заголовком, что оно было отправленно продавцом.

*Окно заказчика:*
![Chat customer](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/chat_customer.png)


Дальнейший обмен сообщениями между заказчиком и продавцом осуществляется как в обычном чате между двумя пользователями.
Все сообщения в чате могут содержать любые файлы (фото, видео и т.д.)

После того, как продавец нажмет на кнопку «Выйти из чата», чат между заказчиком и продавцом будет закрыт и заказчик будет уведомлен о том, что последующие отправленые сообщения продавцу не будут обработаны и доставлены.

![Leave chat](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/leave_chat.png)

#### Отменить выбор заказа
Снимает выбор с заказа и возвращает его в список всех невыбранных заказов. Если до этого момента продавец изменил статус заказа, то он становится `open` (значение по умолчанию)

![Unselect order](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/unselect_order.png)

#### Изменить статус заказа
Всего доступно три статуса заказа:

* открыт (`open`)
* в процессе (`in_process`)
* закрыт (`close`)

В зависимости от статуса заказа выводятся кнопки с возможными статусами для заказа, исключая текущий статус.

![Change status menu](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/change_status_menu.png)

При нажатии на кнопку с названием статуса происходит уведомление о смене статуса заказа

![Changed status](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/changed_status.png)

### Отправить пост

![Send post](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/send_post.png)
При отправке сообщения, бот отправляет его всем пользователям со статусом `client`.
Сообщение может содержать любые файлы (фото, видео и т.д.)

![Sending post](https://github.com/mym1chelle/cars_sales_project/raw/master/screens/sending_post.png)