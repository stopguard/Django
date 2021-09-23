from django.db import models


# Create your models here.
class ProductsCategory(models.Model):
    name = models.CharField('Категория', max_length=64)
    description = models.CharField('Описание', max_length=256, blank=True)
    is_active = models.BooleanField('Доступность', default=True)

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        if self.is_active:
            self.is_active = False
            self.save(using=using)


class Product(models.Model):
    category = models.ForeignKey(ProductsCategory, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=64)
    image = models.ImageField(upload_to='product_images', blank=True)
    description = models.CharField('Описание', max_length=256, blank=True)
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2, default=0)
    quantity = models.IntegerField('Количество на складе', default=0)
    is_active = models.BooleanField('Доступность', default=True)

    def __str__(self):
        return f'{self.name} / {self.category}'
