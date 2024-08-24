from django.contrib import admin
from .models import Cart, Product, CartItem, Order, OrderItem, Customer, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1  # 初始显示的空白条目数量
    fields = ['image_data', 'description']  # 控制显示字段的顺序


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    # list_editable = ("price", "discount_price", "state_tag", "on_sell", "on_discount")
    # list_display = ("title", "price", "discount_price", "state_tag", "on_sell", "on_discount")    
    search_fields = ['title', 'description']  # 添加搜索功能


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['product', 'description']
    search_fields = ['description']

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Customer)

