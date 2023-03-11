from tgbot_django.cars_sales.models import CarOrder, CarModel
from tgbot.middlewares.translate import _


def car_info(car_model: CarModel):
    if car_model.description:
        return _("""{brand} {model}

Description:
{description}
    """).format(
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
    return car_info(car_model=car_model)


def order_info_string(order: CarOrder):
    return '{car_brand} ({color})'.format(
        car_brand=order.car_brand,
        color=order.color
    )


def order_info_admin_menu_without_status(order: CarOrder):
    order_info = order_info_string(order)
    if order.some_wishes:
        return _("""Order: {order}
Comment to the order:
{comment}""").format(order=order_info, comment=order.some_wishes)
    else:
        return _('Order: {order}').format(order=order_info)


def order_info_admin_menu_with_status(order: CarOrder):
    order_info = order_info_string(order)
    if order.some_wishes:
        return _("""Order: {order}
Order status: {status}
Comment to the order:
{comment}""").format(
            order=order_info,
            status=order.order_status,
            comment=order.some_wishes)
    else:
        return _("""Order: {order}
Order status: {status}""").format(
            order=order_info,
            status=order.order_status)
