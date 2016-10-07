from django.contrib import admin
from models import Product
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    fields = ('created_by', 'title')
    list_display = ('created_by', 'title')

admin.site.register(Product, ProductAdmin)
