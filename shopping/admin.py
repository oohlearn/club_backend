from django.contrib import admin
from .models import Cart, Product, CartItem, Order, OrderItem, Customer, Photo, Size
from django.forms import TextInput


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3  # 初始显示的空白条目数量
    fields = ['image_data', 'description', "level"]  # 控制显示字段的顺序

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'level':
            kwargs['widget'] = TextInput(attrs={'size': "5"})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class SizeInline(admin.TabularInline):
    model = Size
    extra = 5
    fields = ["group", 'size', 'description']

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'size':
            kwargs['widget'] = TextInput(attrs={'size': '10'})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, SizeInline]
    # list_editable = ("price", "discount_price", "state_tag", "on_sell", "on_discount")
    # list_display = ("title", "price", "discount_price", "state_tag", "on_sell", "on_discount")    
    search_fields = ['title', 'description']  # 添加搜索功能


# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Customer)

