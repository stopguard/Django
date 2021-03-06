# Generated by Django 3.2 on 2021-11-03 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Категория')),
                ('description', models.CharField(blank=True, max_length=256, verbose_name='Описание')),
                ('is_active', models.BooleanField(default=True, verbose_name='Доступность')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
                ('image', models.ImageField(blank=True, upload_to='product_images')),
                ('description', models.CharField(blank=True, max_length=256, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Цена')),
                ('quantity', models.IntegerField(default=0, verbose_name='Количество на складе')),
                ('is_active', models.BooleanField(default=True, verbose_name='Доступность')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productscategory')),
            ],
        ),
    ]
