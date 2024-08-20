from django.contrib import admin
from.models import ProductCart, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "discount_price", "state_tag", "on_sell", "on_discount")
    list_editable = ("price", "discount_price", "state_tag", "on_sell", "on_discount")


class ProductCartAdmin(admin.ModelAdmin):
    list_display = ("need_deliver_paid", "total")


# Register your models here.
admin.site.register(ProductCart, ProductCartAdmin)
admin.site.register(Product, ProductAdmin)
