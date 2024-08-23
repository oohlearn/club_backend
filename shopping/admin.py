from django.contrib import admin
from.models import Cart, Product, CartItem, Order, OrderItem, Customer


# class ProductAdmin(admin.ModelAdmin):
    # list_display = ("title", "price", "discount_price", "state_tag", "on_sell", "on_discount")
    # list_editable = ("price", "discount_price", "state_tag", "on_sell", "on_discount")


# class ProductCartAdmin(admin.ModelAdmin):
    # list_display = ("need_deliver_paid", "total")


# Register your models here.
admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Customer)
