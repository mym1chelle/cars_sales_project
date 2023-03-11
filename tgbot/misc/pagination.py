from tgbot.models.db_commands.car_model import get_car_model


def get_page_number(iterable, page_number: int = 1):
    """takes the page number and returns the corresponding index

    iterable: any iterable object
    page_number: (int) page number
    """
    page_index = page_number - 1
    return iterable[page_index]


async def get_current_car_info(car_model_id: int, current_page: int = 1):
    """
    General logic for switching between multiple photos
    """
    model = await get_car_model(model_id=car_model_id)
    model_photos = model.carmodelphoto_set
    photo = get_page_number(model_photos.all(), page_number=current_page)
    count_photos = model_photos.count()
    return photo, count_photos, model
