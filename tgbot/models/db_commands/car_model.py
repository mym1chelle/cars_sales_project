from asgiref.sync import sync_to_async
from tgbot_django.cars_sales.models import CarModel


@sync_to_async
def select_car_models_of_brand(brand_id: int):
    return CarModel.objects.filter(brand_id=brand_id)


@sync_to_async
def get_car_model(model_id: int):
    try:
        return CarModel.objects.get(id=model_id)
    except CarModel.DoesNotExist:
        return None
