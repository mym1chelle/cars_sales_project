from asgiref.sync import sync_to_async
from tgbot_django.cars_sales.models import CarOrder, User


@sync_to_async
def add_order(
    customer_id,
    steering_wheel_position,
    car_brand_id,
    color_id,
    some_wishes=None,
):
    """Creates a new order"""
    return CarOrder.objects.create(
        customer_id=customer_id,
        steering_wheel_position=steering_wheel_position,
        car_brand_id=car_brand_id,
        color_id=color_id,
        some_wishes=some_wishes
    )


@sync_to_async
def get_order(order_id):
    """Select order by id"""
    try:
        return CarOrder.objects.get(id=order_id)
    except CarOrder.DoesNotExist:
        return None


@sync_to_async
def change_order_status(order_id: int, status: str):
    """Change order status"""
    order = CarOrder.objects.get(id=order_id)
    order.order_status = status
    order.save()
    return order


@sync_to_async
def all_unselected_orders():
    """Selects all unselected orders with status 'open'"""
    return CarOrder.objects.filter(
        order_status='open'
    ).filter(seller__isnull=True).order_by('created_at')


@sync_to_async
def count_unselected_orders():
    """Get the count of unselected orders with status 'open'"""
    return CarOrder.objects.filter(
        order_status='open'
    ).filter(seller__isnull=True).count()


@sync_to_async
def all_selected_orders(user_id: int):
    """Selects all selected orders records
    by the current user with any order status"""
    try:
        user = User.objects.get(user_id=user_id)
        return CarOrder.objects.filter(
            seller=user.id
            ).order_by('created_at')
    except User.DoesNotExist:
        return None


@sync_to_async
def count_selected_orders(user_id: int):
    """Get the count of all selected orders
    by the current user with any order status"""
    try:
        user = User.objects.get(user_id=user_id)
        return CarOrder.objects.filter(seller_id=user.id).count()
    except User.DoesNotExist:
        return None


@sync_to_async
def select_or_unselect_order(order_id: int, user_id: int = None):
    """Selects an order for the current user or deselect it"""
    order = CarOrder.objects.get(id=order_id)
    if user_id:
        user = User.objects.get(user_id=user_id)
        order.seller_id = user.id
    else:
        order.seller_id = None
        order.order_status = 'open'
    order.save()
    return order
