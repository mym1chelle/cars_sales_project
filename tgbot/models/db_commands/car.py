from asgiref.sync import sync_to_async
from tgbot_django.cars_sales.models import CarBrand, CarColor


@sync_to_async
def select_all_car_brands():
    """Selects all car brands"""
    return CarBrand.objects.all()


@sync_to_async
def select_all_car_colors():
    """Select all car colors"""
    return CarColor.objects.all()