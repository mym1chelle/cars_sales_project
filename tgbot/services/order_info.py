from tgbot_django.cars_sales.models import CarOrder, CarModel
from tgbot.middlewares.translate import _


def _car_info_for_button(car_model: CarModel):
    return '{brand} {model}'.format(
        brand=car_model.brand,
        model=car_model.name
    )


def car_info_full(car_model: CarModel):
    if car_model.description:
        return _("""{brand} {model}

<em>Description:</em>
{description}""").format(
            brand=car_model.brand,
            model=car_model.name,
            description=car_model.description
        )
    else:
        return '{brand} {model}'.format(
            brand=car_model.brand,
            model=car_model.name
        )


def order_info_for_customer(order: CarOrder):
    car_model = order.car
    return car_info_full(car_model=car_model)


def order_info_string(order: CarOrder):
    return _car_info_for_button(
        car_model=order.car
    )


def order_info_admin_menu_without_status(order: CarOrder):
    car = car_info_full(car_model=order.car)
    if order.some_wishes:
        return _("""<b>Order</b>
{car}

Comment to the order:
{comment}""").format(car=car, comment=order.some_wishes)
    else:
        return _("""<b>Order</b>
{car}""").format(car=car)


def order_info_admin_menu_with_status(order: CarOrder):
    car = car_info_full(car_model=order.car)
    if order.some_wishes:
        return _("""<b>Order</b>
{car}

Order status: {status}

Comment to the order:
{comment}""").format(
            car=car,
            status=order.order_status,
            comment=order.some_wishes)
    else:
        return _("""<b>Order</b>
{car}

Order status: {status}""").format(
            car=car,
            status=order.order_status)
