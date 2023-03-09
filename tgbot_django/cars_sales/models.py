from django.db import models
from tgbot.models.db_constants import (
    USER_ROLE,
    ORDER_STATUS,
    LANGUAGES
)


class User(models.Model):

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Users'

    user_id = models.BigIntegerField(
        unique=True,
        verbose_name='ID'
    )

    full_name = models.CharField(
        max_length=50,
        verbose_name='Full name'
    )
    role = models.CharField(
        max_length=15, default='client',
        choices=USER_ROLE, verbose_name='User status'
    )
    language = models.CharField(
        max_length=3,
        default='ru',
        choices=LANGUAGES
    )

    def __str__(self):
        return self.full_name


class CarBrand(models.Model):

    class Meta:
        verbose_name = 'car brand'
        verbose_name_plural = 'Car brands'

    name = models.CharField(
        max_length=150,
        verbose_name='Brand'
    )

    def __str__(self):
        return self.name


class CarColor(models.Model):

    class Meta:
        verbose_name = 'car color'
        verbose_name_plural = 'Car colors'

    name = models.CharField(
        max_length=100,
        verbose_name='Color'
    )

    def __str__(self):
        return self.name


class CarOrder(models.Model):
    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'Orders'
        ordering = ['created_at']

    customer = models.ForeignKey(
        'User',
        verbose_name='Customer',
        on_delete=models.PROTECT,
        related_name='customer'
    )

    car_brand = models.ForeignKey(
        'CarBrand',
        verbose_name='Car brand',
        null=True,
        on_delete=models.SET_NULL
    )
    color = models.ForeignKey(
        'CarColor',
        verbose_name='Car color',
        null=True,
        on_delete=models.SET_NULL
    )
    some_wishes = models.TextField(
        verbose_name='Wishes to order',
        null=True
    )
    order_status = models.CharField(
        max_length=15, default='open',
        choices=ORDER_STATUS, verbose_name='Order status')
    seller = models.ForeignKey(
        'User',
        verbose_name='Seller',
        on_delete=models.PROTECT,
        null=True,
        related_name='seller'
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
