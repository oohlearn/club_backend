from django.contrib import admin

from .models import Video, Album, Article, Teacher, IndexStory, Experience

# 修改後台的標題
admin.site.site_header = "後臺管理系統"
admin.site.site_title = "樂團官網管理後台"
admin.site.index_title = "樂團官網資料管理系統"


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
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(IndexStory)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Album)
