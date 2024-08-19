from django.contrib import admin
from django.utils.html import format_html  #修改日期用

from .models import Video, Activity, Album, Article, Teacher, IndexStory, Experience

# 修改後台的標題
admin.site.site_header = "後臺管理系統"
admin.site.site_title = "樂團官網"
admin.site.index_title = "樂團官網資料管理系統"


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


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "date",)
    search_fields = ("title",)


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("date", "experience")


class TeacherAdmin(admin.ModelAdmin):
    list_display = ("group", "name")


class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "place", "performer")


# Register your models here.
admin.site.register(Video, VideoAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(IndexStory)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Album)
