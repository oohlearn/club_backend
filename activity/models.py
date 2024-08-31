from django.db import models
from tinymce.models import HTMLField
from shortuuidfield import ShortUUIDField


# Create your models here.
class Program(models.Model):
    title = models.CharField(max_length=500, verbose_name="曲目名稱")
    composer = models.CharField(max_length=500, verbose_name="作曲家", blank=True)
    arranger = models.CharField(max_length=500, verbose_name="編曲家", blank=True)
    lyricist = models.CharField(max_length=500, verbose_name="作詞家", blank=True)
    performer = models.CharField(max_length=500, verbose_name="協奏者", blank=True)
    description = models.TextField(verbose_name="其他註解", blank=True)
    event = models.ForeignKey('Event', related_name='program', on_delete=models.CASCADE, verbose_name="演出內容")

    def __str__(self):
        return self.title


class Venue(models.Model):
    name = models.CharField(max_length=300)
    total_seats = models.IntegerField()
    address = models.CharField(max_length=500)
    traffic_info = models.TextField()
    map_url = models.CharField(max_length=1000)
    official_seat_image = models.ImageField(upload_to="Images/articles/", default="Image/None/Noimg.jpg")

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=500, verbose_name="活動/演出標題")
    date = models.DateTimeField(verbose_name="日期時間")
    place = models.CharField(max_length=100, verbose_name="場地", blank=True, null=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, verbose_name="預設場地清單", blank=True, null=True)
    price_type = models.CharField(max_length=100, verbose_name="票價（例：200/300/500）")
    poster = models.ImageField(upload_to="Images/activities/", default="Image/None/Noimg.jpg", verbose_name="海報圖")
    description = HTMLField(verbose_name="活動介紹", blank=True)
    seat_image = models.ImageField(upload_to="Images/activities/", default="Image/None/Noimg.jpg", verbose_name="座位表")
    on_sell = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "活動"  # 自定義單數形式的名稱
        verbose_name_plural = "活動列表"  # 自定義複數形式的名稱


class Zone(models.Model):
    COLOR_CHOICE = [
        ('#FF0000', '紅'),
        ('#00FF00', '綠'),
        ('#0000FF', '藍'),
        ('#FFFF00', '黃'),
        ("#808080", "灰")
    ]
    name = models.CharField(max_length=100)
    eng_name = models.CharField(max_length=100)
    color = models.CharField(max_length=10, choices=COLOR_CHOICE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='zone')
    price = models.IntegerField()


class DiscountCode(models.Model):
    name = models.CharField(max_length=100, verbose_name="折扣碼名稱", help_text="例：團員優惠")
    code = models.CharField(max_length=100, verbose_name="折扣碼", help_text="例：MEMBERROCK")
    discount = models.CharField(max_length=50, verbose_name="折扣比例")
    description = models.CharField(max_length=200, verbose_name="備註＆說明")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='discount_code')

    def __str__(self) -> str:
        return self.name


class Seat(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE,  related_name='seat',)
    seat_num = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.seat_num
