from django.db import models
from tinymce.models import HTMLField
from shortuuidfield import ShortUUIDField
import pandas as pd
from django.core.files.storage import FileSystemStorage


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
    # 自定義文件存儲（可選）
    fs = FileSystemStorage(location='/media/excel_files')
    id = ShortUUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=500, verbose_name="活動/演出標題")
    date = models.DateTimeField(verbose_name="日期時間")
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, verbose_name="場地", blank=True, null=True)
    price_type = models.CharField(max_length=100, verbose_name="票價（例：200/300/500）")
    poster = models.ImageField(upload_to="Images/activities/", default="Image/None/Noimg.jpg", verbose_name="海報圖")
    description = HTMLField(verbose_name="活動介紹", blank=True)
    ticket_system_url = models.CharField(max_length=1000, blank=True, null=True, verbose_name="外部售票系統網址")
    seat_image = models.ImageField(upload_to="Images/activities/", default="Image/None/Noimg.jpg", verbose_name="座位表")
    on_sell = models.BooleanField(default=True)
    excel_file = models.FileField(upload_to="Excel_files", blank=True, null=True, verbose_name="Excel 檔案")

    def __str__(self):
        return self.title

    @classmethod
    def process_excel(cls, file_path, event):
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            zone = cls.objects.create(
                event=event,
                area=row['區域名稱'],
                row=row['排數名稱'],
                start=row['起始座號'],
                end=row['結束座號'],
                price=row['票價']  # 假設 Excel 中有票價列
            )
            # 生成座位
            for num in range(zone.start, zone.end + 1, 2):
                seat_num = f"{zone.row}{num}"
                Seat2.objects.create(zone=zone, seat_number=seat_num)

    class Meta:
        verbose_name = "活動"  # 自定義單數形式的名稱
        verbose_name_plural = "活動列表"  # 自定義複數形式的名稱


class Zone(models.Model):
    COLOR_CHOICE = [
        ('#FF5151', '紅'),
        ('#BE77FF', '紫'),
        ('#9AFF02', '淺綠'),
        ('#84C1FF', '淺藍'),
        ('#F9F900', '黃'),
        ("#FFAF60", "橘"),
        ('#4F9D9D', '青'),
        ('#00A600', '深綠'),
        ('#0073E3', '深藍'),
        ('#844200', '深棕'),
        ('#ADADAD', '灰(非賣票)')
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
    price = models.IntegerField(verbose_name="區域票價", help_text="下方可指定單一票的票價")
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
    COLOR_CHOICE = [
        ('#FF5151', '紅'),
        ('#BE˙˙FF', '紫'),
        ('#9AFF02', '淺綠'),
        ('#84C1FF', '淺藍'),
        ('#F9F900', '黃'),
        ("#FFAF60", "橘"),
        ('#4F9D9D', '青'),
        ('#00A600', '深綠'),
        ('#0073E3', '深藍'),
        ('#844200', '深棕'),
        ('#ADADAD', '灰(非賣票)')
    ]
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE,  related_name='seat', verbose_name="區域")
    seat_num = models.CharField(max_length=10, verbose_name="座位號碼")
    price = models.IntegerField(verbose_name="票價", blank=True, null=True)
    color = models.CharField(max_length=10, choices=COLOR_CHOICE, verbose_name="座位圖顯示顏色", blank=True)
    is_chair = models.BooleanField(default=False, verbose_name="輪椅席")
    is_sold = models.BooleanField(default=False, verbose_name="已售出", editable=False)
    not_sell = models.BooleanField(default=False, verbose_name="非賣票")

    def __str__(self) -> str:
        return self.seat_num


# TODO 待處理
# 地理分區
class Zone2(models.Model):
    fs = FileSystemStorage(location='/media/excel_files')

    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='zone2', verbose_name="對應的演出名稱")
    area = models.CharField(max_length=100, verbose_name="區域名稱", blank=True, null=True)
    row = models.CharField(max_length=10, verbose_name="排數名稱", blank=True, null=True)
    start = models.IntegerField(verbose_name="起始座位號", blank=True, null=True)
    end = models.IntegerField(verbose_name="結束座位號", blank=True, null=True)
    price = models.IntegerField(verbose_name="票價", blank=True, null=True)
    excel_file = models.FileField(upload_to=fs, blank=True, null=True, verbose_name="Excel 檔案")

    def __str__(self):
        return f"{self.event} - {self.area} {self.row}"

    @classmethod
    def process_excel(cls, file_path, event):
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            zone = cls.objects.create(
                event=event,
                area=row['區域名稱'],
                row=row['排數名稱'],
                start=row['起始座號'],
                end=row['結束座號'],
                price=row['票價']  # 假設 Excel 中有票價列
            )
            # 生成座位
            for num in range(zone.start, zone.end + 1, 2):
                seat_num = f"{zone.row}{num}"
                Seat.objects.create(zone=zone, seat_number=seat_num)


class Seat2(models.Model):
    zone = models.ForeignKey(Zone2, on_delete=models.CASCADE, related_name='seat2')
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.zone} - {self.seat_number}"
