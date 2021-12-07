from django.db import models

from django.utils.functional import cached_property


class ProductsCategory(models.Model):
    name = models.CharField('Категория', max_length=64)
    description = models.CharField('Описание', max_length=256, blank=True)
    is_active = models.BooleanField('Доступность', default=True, db_index=True)

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        if self.is_active:
            self.is_active = False
            self.save(using=using)

    def get_products(self, qte_check=True):
        return self.product_set.filter(is_active=True, quantity__gt=0) \
            if qte_check \
            else self.product_set.filter(is_active=True)

    @cached_property
    def get_all_products(self):
        return self.product_set.all()


class Product(models.Model):
    category = models.ForeignKey(ProductsCategory, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=64)
    image = models.ImageField(upload_to='product_images', blank=True)
    description = models.CharField('Описание', max_length=256, blank=True)
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2, default=0)
    quantity = models.IntegerField('Количество на складе', default=0)
    is_active = models.BooleanField('Доступность', default=True, db_index=True)

    def __str__(self):
        return f'{self.name} / {self.category}'
