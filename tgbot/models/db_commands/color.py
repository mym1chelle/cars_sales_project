from asgiref.sync import sync_to_async
from tgbot_django.cars_sales.models import CarColor


@sync_to_async
def count_car_colors():
    return CarColor.objects.all().values('id').count()


@sync_to_async
def select_all_car_colors():
    """Select all car colors"""
    return CarColor.objects.all()


@sync_to_async
def get_car_color(color_id: int):
    try:
        return CarColor.objects.get(id=color_id)
    except CarColor.DoesNotExist:
        return None