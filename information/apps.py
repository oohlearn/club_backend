from django.apps import AppConfig
from django.db.models.signals import post_migrate


class InformationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'information'
    verbose_name = "樂團資料"

    def ready(self):
        post_migrate.connect(update_home_content, sender=self)


def update_home_content(sender, **kwargs):
    from .models import HomeContent
    home_content, created = HomeContent.objects.get_or_create(pk=1)  # 確保只有一個實例
    if not created:
        home_content.save()  # 這樣會觸發 `save` 方法以更新內容
