from django.contrib import admin
from .models import Category, SubCategory, Product, CartItem, Cart, Order, ShippingAddress


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(ShippingAddress)
