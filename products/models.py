from django.db import models


# Create your models here.
class ProductCategories(models.Model):
    name = models.CharField('Категория', max_length=64)
    description = models.CharField('Описание', max_length=256, blank=True)


class Products(models.Model):
    category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=64)
    image = models.ImageField(upload_to='product_images', blank=True)
    description = models.CharField('Описание', max_length=256, blank=True)
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2, default=0)
    quantity = models.IntegerField('Количество на складе', default=0)
