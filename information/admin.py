from django.contrib import admin

from .forms import ArticleAdminForm

from .models import Tag, Video, Album, Article, Teacher, IndexStory, Experience, Photo

# 修改後台的標題
admin.site.site_header = "後臺管理系統"
admin.site.site_title = "樂團官網管理後台"
admin.site.index_title = "樂團官網資料管理系統"


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ("title", "date",)
    search_fields = ("title",)

    def save_model(self, request, obj, form, change):
        # 在保存模型時處理標籤
        if form.cleaned_data.get('tags_input'):
            tag_names = [name.strip() for name in form.cleaned_data['tags_input'].split(',')]
            tags = []
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            obj.tags.set(tags)
        super().save_model(request, obj, form, change)


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("date", "experience")


class TeacherAdmin(admin.ModelAdmin):
    list_display = ("group", "name")


class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "place", "performer")


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1  # 初始显示的空白条目数量
    fields = ['image', 'description']  # 控制显示字段的顺序


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    list_display = ['title', 'date', 'indexImage']  # 控制列表显示的字段
    search_fields = ['title', 'description']  # 添加搜索功能


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['album', 'image', 'description']
    search_fields = ['description']



# Register your models here.
admin.site.register(Video, VideoAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(IndexStory)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Tag)
