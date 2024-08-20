from django.contrib import admin
from django.utils.html import format_html  #修改日期用
from .models import Activity


# Register your models here.


# 自定義欄位
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "price_type", "place")
    search_fields = ("title", "place")

    def formatted_date(self, obj):
        # 將日期格式化為 YYYY,M,D
        return format_html(f"{obj.date.year}.{obj.date.month}.{obj.date.day}")

    formatted_date.short_description = 'date'


# 可編輯欄位
    list_editable = ("date", "price_type", "place")


admin.site.register(Activity, ActivityAdmin)
