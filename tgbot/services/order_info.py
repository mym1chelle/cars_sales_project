from tgbot_django.cars_sales.models import CarOrder
from tgbot.middlewares.translate import _


def order_info_for_customer(order: CarOrder):
    return _("""Model car: {car_brand}
Steering wheel position: {wheel_position}
Color: {color}""").format(
        car_brand=order.car_brand,
        wheel_position=order.steering_wheel_position,
        color=order.color
    )


def order_info_string(order: CarOrder):
    return '{car_brand} ({wheel_position}, {color})'.format(
        car_brand=order.car_brand,
        wheel_position=order.steering_wheel_position,
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
