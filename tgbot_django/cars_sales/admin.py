from django.contrib import admin
from .models import (
    User,
    CarOrder,
    CarBrand,
    CarModel,
    CarModelPhoto
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
        'car',
        'some_wishes',
        'order_status',
        'seller'
    )


@admin.register(CarBrand)
class CardBrandAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class CarPhotoModelAdmin(admin.TabularInline):
    model = CarModelPhoto


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = (
        'brand',
        'name',
        'description'
    )
    inlines = [CarPhotoModelAdmin,]
