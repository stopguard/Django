# Generated by Django 3.2 on 2021-12-01 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Доступность'),
        ),
        migrations.AlterField(
            model_name='productscategory',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Доступность'),
        ),
        migrations.AlterField(
            model_name='productscategory',
            name='name',
            field=models.CharField(db_index=True, max_length=64, verbose_name='Категория'),
        ),
    ]
