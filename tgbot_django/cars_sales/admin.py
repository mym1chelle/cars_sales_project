from django.contrib import admin
from .models import (
    User,
    CarOrder,
    CarBrand,
    CarColor,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_id',
        'full_name',
        'role',
        'language'
    )


@admin.register(CarOrder)
class CarOrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'customer',
        'car_brand',
        'steering_wheel_position',
        'color',
        'some_wishes',
        'order_status',
        'seller'
    )


@admin.register(CarBrand)
class CardBrandAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )


@admin.register(CarColor)
class CarColorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )
