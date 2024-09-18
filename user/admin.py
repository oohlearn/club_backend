from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.models import User

from .models import Contact, UserProfile, Customer


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'category', 'title', 'created_at', 'replied')
    search_fields = ('name', 'title', 'content')
    readonly_fields = ('name', 'email', 'phone', 'category', 'title', 'content', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if 'reply' in form.changed_data:
            obj.replied = True
            self.send_reply_email(obj)
        super().save_model(request, obj, form, change)

    def send_reply_email(self, obj):
        subject = f'回覆：{obj.title}'
        message = f"親愛的 {obj.name}，\n\n這是對您的來信的回覆：\n\n{obj.reply}\n\n祝好，\n管理團隊"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [obj.email]
        send_mail(subject, message, from_email, recipient_list)


# 使用者
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_filter = ()  # 顯式禁用過濾器


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Customer)
