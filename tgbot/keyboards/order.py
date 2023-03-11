from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.models.db_commands.car_brand import select_all_car_brands
from tgbot.models.db_commands.car_model import select_car_models_of_brand
from tgbot.middlewares.translate import _


create_order_callback_data = CallbackData(
    'create',
    'level',
    'car_brand_id',
    'car_model_id',
    'page_number',
    'key'
)

pagination_callback_data = CallbackData(
    'paginator',
    'page_number',
    'car_brand_id',
    'car_model_id',
)

select_model_callback_data = CallbackData(
    'select_model',
    'car_model_id',
    'car_brand_id'
)

create_order_back_callback_data = CallbackData(
    'back_create_order',
    'car_model_id',
    'car_brand_id'
)


def order_callback_data(
        level,
        car_brand_id='',
        car_model_id='',
        page_number='',
        key='',
):
    return create_order_callback_data.new(
        level=level,
        car_brand_id=car_brand_id,
        car_model_id=car_model_id,
        page_number=page_number,
        key=key
    )


async def select_car_brand_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=2)
    car_brands = await select_all_car_brands()
    for brand in car_brands:
        button_text = brand.name
        callback_data = order_callback_data(
            level=CURRENT_LEVEL + 1,
            car_brand_id=brand.id
        )
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data
            )
        )
    markup.row(
        InlineKeyboardButton(
            text=_('Cancel'),
            callback_data='cancel_create_order'
        )
    )
    return markup


async def all_car_model_keyboard(car_brand_id):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=2)
    models = await select_car_models_of_brand(brand_id=car_brand_id)
    for model in models:
        button_text = model.name
        callback_data = order_callback_data(
            level=CURRENT_LEVEL + 1,
            car_brand_id=car_brand_id,
            car_model_id=model.id
        )
        markup.insert(
            InlineKeyboardButton(
                text=button_text,
                callback_data=callback_data
            )
        )
    markup.row(
        InlineKeyboardButton(
            text=_('Back'),
            callback_data=order_callback_data(
                level=CURRENT_LEVEL - 1
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Cancel'),
            callback_data='cancel_create_order'
        )
    )
    return markup


async def select_car_model_keyboard(
        car_model_id,
        car_brand_id,
        count_pages,
        current_page: int = 1
):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()
    if count_pages <= 1:
        pass
    else:
        previous_page = current_page - 1
        previous_page_text = '⬅️'

        current_page_text = current_page

        next_page = current_page + 1
        next_page_text = '➡️'

        markup = InlineKeyboardMarkup()

        if previous_page > 0:
            markup.insert(
                InlineKeyboardButton(
                    text=previous_page_text,
                    callback_data=pagination_callback_data.new(
                        page_number=previous_page,
                        car_brand_id=car_brand_id,
                        car_model_id=car_model_id
                    )
                )
            )
        
        markup.insert(
            InlineKeyboardButton(
                text=current_page_text,
                callback_data='current'
            )
        )

        if next_page <= count_pages:
            markup.insert(
                InlineKeyboardButton(
                    text=next_page_text,
                    callback_data=pagination_callback_data.new(
                        page_number=next_page,
                        car_brand_id=car_brand_id,
                        car_model_id=car_model_id
                    )
                )
            )
    markup.row(
        InlineKeyboardButton(
            text=_('Select'),
            callback_data=select_model_callback_data.new(
                car_model_id=car_model_id,
                car_brand_id=car_brand_id
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Back'),
            callback_data=order_callback_data(
                level=CURRENT_LEVEL - 1,
                car_brand_id=car_brand_id
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Cancel'),
            callback_data='cancel_create_order'
        )
    )
    return markup


async def get_order_wishes_keyboard(car_model_id: int, car_brand_id: int):
    markup = InlineKeyboardMarkup(row=1)
    markup.row(
        InlineKeyboardButton(
            text=_('No comment'),
            callback_data='order_without_wishess'
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Back'),
            callback_data=create_order_back_callback_data.new(
                car_model_id=car_model_id,
                car_brand_id=car_brand_id,
            )
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=_('Cancel'),
            callback_data='cancel_create_order'
        )
    )
    return markup
