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
    registration_date = models.DateTimeField(
        verbose_name='Registration date',
        auto_now_add=True
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


class CarModel(models.Model):

    class Meta:
        verbose_name = 'car model'
        verbose_name_plural = 'Car models'
    name = models.CharField(
        max_length=250,
        verbose_name='Model'
    )

    brand = models.ForeignKey(
        'CarBrand',
        verbose_name='Brand',
        on_delete=models.CASCADE
    )

    description = models.TextField(
        verbose_name='Description',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.brand} {self.name}'


class CarModelPhoto(models.Model):
    class Meta:
        verbose_name = 'car model photo'
        verbose_name_plural = 'Car model photos'
    car = models.ForeignKey(
        'CarModel',
        on_delete=models.CASCADE
    )
    photo = models.ImageField(
        verbose_name='Photo', upload_to='photos/%Y/%m/%d/', null=True
    )


class CarOrder(models.Model):
    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'Orders'
        ordering = ['created_at']

    customer = models.ForeignKey(
        'User',
        verbose_name='Customer',
        on_delete=models.CASCADE,
        related_name='customer'
    )
    car = models.ForeignKey(
        'CarModel',
        verbose_name='Car',
        on_delete=models.PROTECT
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
        on_delete=models.SET_NULL,
        null=True,
        related_name='seller'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')

    def __str__(self):
        return f'{self.customer}: {self.car}'