# Generated by Django 4.1.7 on 2023-03-10 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars_sales', '0003_remove_carorder_steering_wheel_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Model')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars_sales.carbrand', verbose_name='Brand')),
            ],
            options={
                'verbose_name': 'car model',
                'verbose_name_plural': 'Car models',
            },
        ),
        migrations.CreateModel(
            name='CarModelPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Photo')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars_sales.carmodel')),
            ],
            options={
                'verbose_name': 'car model photo',
                'verbose_name_plural': 'Car model photos',
            },
        ),
        migrations.RemoveField(
            model_name='carorder',
            name='car_brand',
        ),
        migrations.RemoveField(
            model_name='carorder',
            name='color',
        ),
        migrations.DeleteModel(
            name='CarColor',
        ),
        migrations.AddField(
            model_name='carorder',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cars_sales.carmodel', verbose_name='Car'),
        ),
    ]
