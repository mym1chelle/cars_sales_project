from asgiref.sync import sync_to_async
from tgbot_django.cars_sales.models import User


@sync_to_async()
def get_user(id: int = None, user_id: int = None):
    """Get user via user_id or id"""
    if user_id and not id:
        try:
            return User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return None
    elif id and not user_id:
        try:
            return User.objects.get(id=id)
        except User.DoesNotExist:
            return None


@sync_to_async
def add_user(user_id: int, full_name: str):
    """Add user or get if exists"""
    return User.objects.get_or_create(user_id=user_id,
                                      full_name=full_name)[0]


@sync_to_async
def get_language(user_id: int, full_name: str):
    """Gets the selected language for the current user.
    If there is no such user, it will be created"""
    try:
        user = User.objects.get_or_create(user_id=user_id,
                                          full_name=full_name)[0]
        return user.language
    except User.DoesNotExist:
        return None


@sync_to_async
def change_language(user_id: int, language_code: str):
    """Changes the language of the selected user by user_id"""
    try:
        user = User.objects.get(user_id=user_id)
        user.language = language_code
        user.save()
        return user
    except Exception:
        return None


@sync_to_async
def is_seller(user_id: int):
    """Checks if the user is a seller"""
    try:
        role = User.objects.get(user_id=user_id).role
        if role == 'seller':
            return True
        return False
    except User.DoesNotExist:
        return None


@sync_to_async
def get_all_clients_user_ids():
    """Get a tuple with the user_id of the customers"""
    query_set = User.objects.filter(role='client').values_list('user_id')
    if query_set:
        return query_set[0]
    return None