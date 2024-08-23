from django.db import models
from taggit.managers import TaggableManager
from tinymce.models import HTMLField
import uuid  # 生成隨機ID


# Create your models here.
class Activity(models.Model):
    id = models.CharField(primary_key=True, editable=False, default=uuid.uuid4, max_length=100)
    title = models.CharField(max_length=500, verbose_name="活動/演出標題")
    date = models.DateField(verbose_name="日期")
    place = models.CharField(max_length=100, verbose_name="場地")
    price_type = models.CharField(max_length=100, verbose_name="票價（例：200/300/500）")
    poster = models.ImageField(upload_to="Images/activities/", default="Image/None/Noimg.jpg", verbose_name="海報圖")
    description = HTMLField(verbose_name="活動介紹", blank=True)
    program = models.JSONField(default=list, verbose_name="演出內容（曲目）")
    ticket = models.JSONField(default=list, verbose_name="票種清單")
    seat_image = models.ImageField(upload_to="Images/activities/", default="Image/None/Noimg.jpg", verbose_name="座位表")
    on_sell = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "活動"  # 自定義單數形式的名稱
        verbose_name_plural = "活動列表"  # 自定義複數形式的名稱