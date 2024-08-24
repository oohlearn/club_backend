from django.db import models
from tinymce.models import HTMLField
from shortuuidfield import ShortUUIDField


# Create your models here.
class Activity(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=500, verbose_name="活動/演出標題")
    date = models.DateField(verbose_name="日期")
    place = models.CharField(max_length=100, verbose_name="場地")
    price_type = models.CharField(max_length=100, verbose_name="票價（例：200/300/500）")
    poster = models.ImageField(upload_to="Images/activities/", default="Image/None/Noimg.jpg", verbose_name="海報圖")
    description = HTMLField(verbose_name="活動介紹", blank=True)
    ticket = models.JSONField(default=list, verbose_name="票種清單")
    seat_image = models.ImageField(upload_to="Images/activities/", default="Image/None/Noimg.jpg", verbose_name="座位表")
    on_sell = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "活動"  # 自定義單數形式的名稱
        verbose_name_plural = "活動列表"  # 自定義複數形式的名稱


class Program(models.Model):
    title = models.CharField(max_length=500, verbose_name="曲目名稱")
    composer = models.CharField(max_length=500, verbose_name="作曲家", blank=True)
    arranger = models.CharField(max_length=500, verbose_name="編曲家", blank=True)
    lyricist = models.CharField(max_length=500, verbose_name="作詞家", blank=True)
    performer = models.CharField(max_length=500, verbose_name="協奏者", blank=True)
    description = models.TextField(verbose_name="其他註解", blank=True)
    activity = models.ForeignKey('Activity', related_name='programs', on_delete=models.CASCADE, verbose_name="演出內容")

    def __str__(self):
        return self.title
