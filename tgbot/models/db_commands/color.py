from asgiref.sync import sync_to_async
from tgbot_django.cars_sales.models import CarColor


@sync_to_async
def count_car_colors():
    """Counting the number of all colors"""
    return CarColor.objects.all().values('id').count()


@sync_to_async
def select_all_car_colors():
    """Select all car colors"""
    return CarColor.objects.all()


@sync_to_async
def get_car_color(color_id: int):
    """Color selection by id"""
    try:
        return CarColor.objects.get(id=color_id)
    except CarColor.DoesNotExist:
        return None


@sync_to_async
def add_car_color(color_name):
    """Adding a new color"""
    return CarColor.objects.create(name=color_name)


@sync_to_async
def change_car_color(new_color: str, color_id: int):
    """Change car color name"""
    try:
        brand = CarColor.objects.get(id=color_id)
        brand.name = new_color
        brand.save()
        return brand
    except CarColor.DoesNotExist:
        return None


@sync_to_async
def delete_car_color(color_id: int):
    """Deleting the selected vehicle color"""
    try:
        color = CarColor.objects.get(id=color_id)
        color.delete()
        return True
    except CarColor.DoesNotExist:
        return False
