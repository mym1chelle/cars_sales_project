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
def get_car_brand(brand_id: int):
    """Choosing a car brand by ID"""
    try:
        return CarBrand.objects.get(id=brand_id)
    except CarBrand.DoesNotExist:
        return None


@sync_to_async
def change_car_brand(new_brand: str, brand_id: int):
    """Changing the brand name of the car"""
    try:
        brand = CarBrand.objects.get(id=brand_id)
        brand.name = new_brand
        brand.save()
        return brand
    except CarBrand.DoesNotExist:
        return None


@sync_to_async
def delete_car_brand(brand_id: int):
    """Deleting the selected car brand"""
    try:
        brand = CarBrand.objects.get(id=brand_id)
        brand.delete()
        return True
    except CarBrand.DoesNotExist:
        return False
