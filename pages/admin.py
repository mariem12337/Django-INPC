# Register your models here.
from django.contrib import admin
from .models import Product, ProductType, PointOfSale, ProductPrice, Cart, CartProducts

admin.site.register(Product)
admin.site.register(ProductType)
admin.site.register(PointOfSale)
admin.site.register(ProductPrice)
admin.site.register(Cart)
admin.site.register(CartProducts)
