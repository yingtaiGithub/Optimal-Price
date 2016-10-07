from django.db import models
from django.conf import settings
# Create your models here.


class Product(models.Model):
    created_by = models.ForeignKey('core.Shop')
    created = models.DateTimeField(auto_now_add=True)
    shopify_product_id = models.BigIntegerField(default=0)
    shopify_variant_id = models.BigIntegerField(default=0)
    title = models.CharField(max_length=250, default='')
    created_at_shopify = models.DateTimeField()
    updated_at_shopify = models.DateTimeField()
    original_shopify_price = models.DecimalField(
        max_digits=10, decimal_places=2)
    actual_shopify_price = models.DecimalField(max_digits=10, decimal_places=2)
    visits = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    number_of_sells = models.IntegerField(default=0)


class Optimization(models.Model):
    types = [('revenue', 'revenue'), ('profit', 'profit')]
    type_of_optimization = models.CharField(default='revenue',
                                            max_length=7, choices=types)
    Product = models.ForeignKey('Product')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    optimized_price = models.DecimalField(max_digits=12,
                                          decimal_places=2)


class Historic(models.Model):
    Product = models.ForeignKey('Product')
    price = models.DecimalField(max_digits=12,
                                decimal_places=2)
    quantity = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=12,
                                decimal_places=2)
    date = models.DateField()
