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


# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=500, verbose_name="姓名")
    title = models.CharField(max_length=500, verbose_name="職稱、腳色", blank=True)
    event = models.ForeignKey('Event', related_name='player', on_delete=models.CASCADE, verbose_name="演出活動")

    def __str__(self):
        return self.title


class Venue(models.Model):
    SIZE_CHOICES = [
        ("小型場地", "小型場地（總座位數＜300，座位區塊3塊以內）"),
        ("中小型場地", "中小型場地（總座位數介於300～500，座位區塊6塊以內）"),
        ("中型場地", "中型場地（總座位數介於500-1200，座位區塊6塊以內）"),
        ("中大型場地", "中大型場地（總座位數介於1200-2000，座位區塊8塊以內）"),
    ]
    size = models.CharField(max_length=100, choices=SIZE_CHOICES)
    name = models.CharField(max_length=300)
    total_seats = models.IntegerField(blank=True)
    address = models.CharField(max_length=500)
    traffic_info = HTMLField(verbose_name="交通資訊", blank=True)
    map_url = models.CharField(max_length=1000, blank=True)
    official_seat_image = models.ImageField(upload_to="Images/articles/", default="Image/None/Noimg.jpg")

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=500, verbose_name="活動/演出標題")
    date = models.DateTimeField(verbose_name="日期時間")
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, verbose_name="場地", blank=True, null=True)
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

    AREA_CHOICES = [
        ("前左", "前左"),
        ("前中", "前中"),
        ("前右", "前右"),
        ("中左", "中左"),
        ("中中", "中中"),
        ("中右", "中右"),
        ("後左", "後左"),
        ("後中", "後中"),
        ("後右", "後右"),
    ]
    name = models.CharField(max_length=50, verbose_name="票種")
    eng_name = models.CharField(max_length=50, verbose_name="票種英文簡稱")
    area = models.CharField(max_length=50, choices=AREA_CHOICES, verbose_name="區域相對位置", help_text="例：普通票A區、普通票B區", blank=True, null=True)
    color = models.CharField(max_length=10, choices=COLOR_CHOICE, verbose_name="座位圖顯示顏色")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='zone', verbose_name="對應的演出名稱")
    price = models.IntegerField(verbose_name="票價")
    total = models.IntegerField(verbose_name="總數", blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True, verbose_name="票券說明（下拉式顯示）")
    help_words = models.CharField(max_length=500, blank=True, null=True, help_text="票券說明（直接顯示）")


class DiscountCode(models.Model):
    name = models.CharField(max_length=100, verbose_name="折扣碼名稱", help_text="例：團員優惠")
    code = models.CharField(max_length=100, verbose_name="折扣碼", help_text="例：MEMBERROCK")
    discount = models.CharField(max_length=50, verbose_name="折扣比例")
    description = models.CharField(max_length=200, verbose_name="備註＆說明")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='discount_code')

    def __str__(self) -> str:
        return self.name


class Seat(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE,  related_name='seat', verbose_name="區域")
    seat_num = models.CharField(max_length=10, verbose_name="座位號碼")
    is_chair = models.BooleanField(default=False, verbose_name="輪椅席")
    is_sold = models.BooleanField(default=False, verbose_name="已售出")

    def __str__(self) -> str:
        return self.seat_num
