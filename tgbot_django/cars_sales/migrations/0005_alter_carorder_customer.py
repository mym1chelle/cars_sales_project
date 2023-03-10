# Generated by Django 4.1.7 on 2023-03-10 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars_sales', '0004_carmodel_carmodelphoto_remove_carorder_car_brand_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carorder',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='cars_sales.user', verbose_name='Customer'),
        ),
    ]
