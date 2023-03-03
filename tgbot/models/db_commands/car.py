from asgiref.sync import sync_to_async
from tgbot_django.cars_sales.models import CarBrand


@sync_to_async
def select_all_car_brands():
    """Selects all car brands"""
    return CarBrand.objects.all()


@sync_to_async
def add_car_brand(car_brand: str):
    """Adds a new car brand"""
    return CarBrand.objects.create(
        name=car_brand
    )


@sync_to_async
def count_car_brands():
    """Counts the number of all car brands"""
    return CarBrand.objects.all().values('id').count()

@sync_to_async
def get_car_brand(brand_id):
    try:
        return CarBrand.objects.get(id=brand_id)
    except CarBrand.DoesNotExist:
        return None
