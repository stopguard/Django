# Generated by Django 3.2 on 2021-11-03 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_alter_shopuser_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='age',
            field=models.IntegerField(verbose_name='Возраст'),
        ),
    ]
