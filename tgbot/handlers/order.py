from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from tgbot.misc.create_order_states import CreateOrderStates
from tgbot.misc.pagination import get_current_car_info
from tgbot.models.db_commands.user import add_user, get_user
from tgbot.models.db_commands.order import add_order
from tgbot.services.order_info import car_info_full, order_info_for_customer
from tgbot.keyboards.order import (
    create_order_callback_data,
    pagination_callback_data,
    select_model_callback_data,
    select_car_brand_keyboard,
    all_car_model_keyboard,
    select_car_model_keyboard,
    get_order_wishes_keyboard
)
from tgbot.middlewares.translate import _
from bot_setting import bot


async def start_create_order(message: types.Message):
    """Runs the order creation logic"""
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    await add_user(
        user_id=user_id,
        full_name=full_name
    )
    await select_car_brand(message)


async def select_car_brand(
        message: types.Message | types.CallbackQuery, **kwargs
):
    """Displays a keyboard with car brands and
    prompts you to select one of them."""
    text = _('Choose a car brand:')
    markup = await select_car_brand_keyboard()
    if isinstance(message, types.Message):
        await message.answer(
            text=text,
            reply_markup=markup
        )
    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_text(
            text=text,
            reply_markup=markup
        )


async def show_car_models(
    call: types.CallbackQuery,
    car_brand_id: int,
    **kwargs,
):
    """
    Displays a keyboard with car models of the previously selected brand
    and prompts you to select one of them.

    Since the previous message can be not only text,
    but also contain a photo, you need to delete it and create a new one
    """
    await call.message.delete()
    await call.message.answer(
        text=_('Choose car model:'),
        reply_markup=await all_car_model_keyboard(car_brand_id=car_brand_id)
    )


async def select_car_model(
    call: types.CallbackQuery,
    car_brand_id,
    car_model_id,
    **kwargs
):
    """
    Displays information about the selected car model,
    buttons for switching by car photo (if there is more than one),
    menu navigation buttons and a button for selecting this model
    and adding it to the order
    """
    photo, count_photos, model = await get_current_car_info(
        car_model_id=car_model_id
    )
    await call.message.delete()
    text = car_info_full(car_model=model)
    markup = await select_car_model_keyboard(
        count_pages=count_photos,
        car_brand_id=car_brand_id,
        car_model_id=car_model_id
    )
    if photo:
        await call.message.answer_photo(
            photo=types.InputFile(
                '.' + photo.photo.url
            ),
            caption=text,
            reply_markup=markup
        )
    else:
        await call.message.answer(
            text=text,
            reply_markup=markup
        )


async def show_chosen_photo(
        call: types.CallbackQuery,
        callback_data: dict
):
    """
    Move between photos of car models.
    Additionally, data is taken from callback data
    to return to the previous menu
    """
    current_page = int(callback_data.get('page_number'))
    car_brand_id = int(callback_data.get('car_brand_id'))
    car_model_id = int(callback_data.get('car_model_id'))

    photo, count_photos, model = await get_current_car_info(
        car_model_id=car_model_id,
        current_page=current_page
    )
    print(photo.photo.url[1:])
    await call.message.edit_media(
        media=types.InputMediaPhoto(
            types.InputFile(
                '.' + photo.photo.url
            ),
            caption=car_info_full(car_model=model),
        ),
        reply_markup=await select_car_model_keyboard(
            count_pages=count_photos,
            current_page=current_page,
            car_model_id=car_model_id,
            car_brand_id=car_brand_id
        )
    )


async def add_order_wishes(
        call: types.CallbackQuery,
        callback_data: dict,
        state: FSMContext
):
    """
    The step of adding a comment to the order.
    This is where the state machine is used.
    """
    car_model_id = int(callback_data.get('car_model_id'))
    car_brand_id = int(callback_data.get('car_brand_id'))
    await call.message.delete()
    message = await call.message.answer(
        text=_('Add a comment to the order:'),
        reply_markup=await get_order_wishes_keyboard(
            car_model_id=car_model_id,
            car_brand_id=car_brand_id
        )
    )
    async with state.proxy() as data:
        data['car_model_id'] = car_model_id
        data['message_id'] = message.message_id
    await CreateOrderStates.add_order_wishes.set()


async def save_order_wishes(
    message: types.Message,
    state: FSMContext
):
    """Creating an order with a comment from a customer"""
    data = await state.get_data()
    await bot.delete_message(
        chat_id=message.from_id,
        message_id=message.message_id
    )
    user = await get_user(user_id=message.from_user.id)
    order = await add_order(
        customer_id=user.id,
        car_model_id=data['car_model_id'],
        some_wishes=message.text,

    )

    show_order = order_info_for_customer(order=order)
    text = _("""
Your order
{order}
has been created"""
             ).format(order=show_order)

    await bot.edit_message_text(
        chat_id=message.from_id,
        message_id=int(data['message_id']),
        text=text
    )
    await state.finish()


async def navigate(
        call: types.CallbackQuery,
        callback_data: dict
):
    """Function for navigating through the inline menu"""
    current_level = str(callback_data.get('level'))
    car_brand_id = callback_data.get('car_brand_id')
    car_model_id = callback_data.get('car_model_id')
    message_id = callback_data.get('message_id')

    levels = {
        '0': select_car_brand,
        '1': show_car_models,
        '2': select_car_model
    }
    current_level_func = levels[current_level]

    await current_level_func(
        call=call,
        message=call,
        car_brand_id=car_brand_id,
        car_model_id=car_model_id,
        message_id=message_id
    )


def register_create_order(dp: Dispatcher):
    dp.register_message_handler(start_create_order, CommandStart())
    dp.register_callback_query_handler(
        show_chosen_photo,
        pagination_callback_data.filter()
    )
    dp.register_callback_query_handler(
        navigate, create_order_callback_data.filter())
    dp.register_callback_query_handler(
        add_order_wishes,
        select_model_callback_data.filter()
    )
    dp.register_message_handler(
        save_order_wishes,
        state=CreateOrderStates.add_order_wishes
    )
