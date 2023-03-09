from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from tgbot.misc.create_order_states import CreateOrderStates
from tgbot.models.db_commands.user import add_user
from tgbot.models.db_commands.order import add_order
from tgbot.services.order_info import order_info_for_customer
from tgbot.keyboards.order import (
    create_order_callback_data,
    select_car_brand_keyboard,
    select_car_color_keyboard,
    get_order_wishes_keyboard
)
from tgbot.middlewares.translate import _
from bot_setting import bot


async def select_car_brand(
        message: types.Message,
        state: FSMContext):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    user = await add_user(
        user_id=user_id,
        full_name=full_name
    )
    id_user = user.id
    await message.answer(
        text=_('Choose a car brand:'),
        reply_markup=await select_car_brand_keyboard())
    async with state.proxy() as data:
        data['id_user'] = id_user
    await CreateOrderStates.select_car_brand.set()


async def select_car_color(
    call: types.CallbackQuery,
    callback_data: dict,
    state: FSMContext
):
    await call.message.edit_text(
        text=_('Choose car color:'),
        reply_markup=await select_car_color_keyboard()
    )
    async with state.proxy() as data:
        data['car_brand_id'] = callback_data['car_brand_id']
    await CreateOrderStates.select_car_color.set()


async def add_order_wishes(
    call: types.CallbackQuery,
    callback_data: dict,
    state: FSMContext
):
    message = await call.message.edit_text(
        text=_('Add a comment to the order:'),
        reply_markup=await get_order_wishes_keyboard()
    )

    async with state.proxy() as data:
        data['car_color_id'] = callback_data['car_color_id']
        data['message_id'] = message.message_id
    await CreateOrderStates.add_order_wishes.set()


async def save_order_wishes(
    message: types.Message,
    state: FSMContext
):
    data = await state.get_data()
    await bot.delete_message(
        chat_id=message.from_id,
        message_id=message.message_id
    )
    order = await add_order(
        customer_id=data['id_user'],
        steering_wheel_position=data['steering_wheel_position'],
        car_brand_id=data['car_brand_id'],
        color_id=data['car_color_id'],
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


def register_create_order(dp: Dispatcher):
    dp.register_message_handler(select_car_brand, CommandStart())
    dp.register_callback_query_handler(
        select_car_color,
        create_order_callback_data.filter(),
        state=CreateOrderStates.select_car_brand
    )
    dp.register_callback_query_handler(
        add_order_wishes,
        create_order_callback_data.filter(),
        state=CreateOrderStates.select_car_color
    )
    dp.register_message_handler(
        save_order_wishes,
        state=CreateOrderStates.add_order_wishes
    )
