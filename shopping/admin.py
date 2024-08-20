from django.contrib import admin
from.models import ProductCart, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "discount_price", "state_tag", "on_sell", "on_discount")
    list_editable = ("price", "discount_price", "state_tag", "on_sell", "on_discount")


# Register your models here.
admin.site.register(ProductCart)
admin.site.register(Product, ProductAdmin)
