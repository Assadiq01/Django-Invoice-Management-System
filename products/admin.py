# 5th

from django.contrib import admin

from .models import (
    Product, Image, Variant, Customer
)

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Variant)
