from django.db import models
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.


class Video(models.Model):
    title = models.CharField(max_length=200, verbose_name="標題")
    date = models.DateField(verbose_name="日期")
    performer = models.CharField(max_length=100, verbose_name="演出者")
    place = models.CharField(max_length=100, verbose_name="演出場地")
    description = models.TextField(blank=True, verbose_name="演出內容敘述")
    url = models.CharField(max_length=500, verbose_name="youtube網址")
    embed_url = models.CharField(max_length=1000, blank=True, verbose_name="youtube內嵌網址(請點選youtube分享)")
    image = models.ImageField(upload_to="Images/videos/", default="Image/None/Noimg.jpg", verbose_name="封面照")
    tags = TaggableManager(help_text="請以逗號分隔標籤", blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "影片"  # 自定義單數形式的名稱
        verbose_name_plural = "影片列表"  # 自定義複數形式的名稱


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="文章標題")
    date = models.DateField(verbose_name="日期")
    content = CKEditor5Field(verbose_name="文章內容", blank=True)
    tags = TaggableManager(help_text="請以逗號分隔標籤", blank=True)  # 添加tag管理器，並自定義說明文字
    article_img = models.ImageField(upload_to="Images/articles/", default="Image/None/Noimg.jpg", verbose_name="文章代表圖片")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章"  # 自定義單數形式的名稱
        verbose_name_plural = "文章列表"  # 自定義複數形式的名稱


class Activity(models.Model):
    title = models.CharField(max_length=500, verbose_name="活動/演出標題")
    date = models.DateField(verbose_name="日期")
    place = models.CharField(max_length=100, verbose_name="場地")
    price_type = models.CharField(max_length=100, verbose_name="票價（例：200/300/500）")
    poster = models.ImageField(upload_to="Images/activities/", default="Image/None/Noimg.jpg", verbose_name="海報圖")
    description = CKEditor5Field(verbose_name="活動介紹", blank=True)
    program = models.JSONField(default=list, verbose_name="演出內容（曲目）")
    ticket = models.JSONField(default=list, verbose_name="票種清單")
    seat_image = models.ImageField(upload_to="Images/activities/", default="Image/None/Noimg.jpg", verbose_name="座位表")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "活動"  # 自定義單數形式的名稱
        verbose_name_plural = "活動列表"  # 自定義複數形式的名稱


class IndexStory(models.Model):
    title = models.CharField(max_length=500, verbose_name="封面故事標題")
    date = models.DateField(verbose_name="日期")
    place = models.CharField(max_length=100, blank=True, verbose_name="場地")
    btn_text = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, verbose_name="描述（不超過10個字）")
    image = models.ImageField(upload_to="Images/index_stories/", default="Image/None/Noimg.jpg", verbose_name="圖片")
    url = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "封面故事（會在網頁上方跑馬燈）"  # 自定義單數形式的名稱
        verbose_name_plural = "封面故事列表"  # 自定義複數形式的名稱


class Experience(models.Model):
    date = models.CharField(max_length=100, verbose_name="日期")
    experience = models.TextField(verbose_name="經歷標題")
    description = CKEditor5Field(verbose_name="經歷細節介紹", blank=True)
    image = models.ImageField(upload_to="Images/experiences/", default="Image/None/Noimg.jpg", verbose_name="圖片")

    def __str__(self):
        return self.experience

    class Meta:
        verbose_name = "經歷"  # 自定義單數形式的名稱
        verbose_name_plural = "經歷列表"  # 自定義複數形式的名稱


class Teacher(models.Model):
    group = models.CharField(max_length=500, verbose_name="組別", blank=True)
    name = models.CharField(max_length=500, verbose_name="老師姓名")
    description = models.TextField(blank=True, verbose_name="老師簡歷")
    image = models.ImageField(upload_to="Images/teachers/", default="Image/None/Noimg.jpg", verbose_name="照片")

    def __str__(self):
        return self.group

    class Meta:
        verbose_name = "分組老師"  # 自定義單數形式的名稱
        verbose_name_plural = "老師列表"  # 自定義複數形式的名稱


# TODO 待解決放入多張照片
class Album(models.Model):
    title = models.CharField(max_length=1000, verbose_name="相簿名稱")
    date = models.DateField(verbose_name="日期")
    description = CKEditor5Field(verbose_name="相簿介紹", blank=True)
    tags = TaggableManager(help_text="請以逗號分隔標籤", blank=True)
    indexImage = models.ImageField(verbose_name="相簿封面照", upload_to="Images/albums/", default="Image/None/Noimg.jpg")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "相簿"  # 自定義單數形式的名稱
        verbose_name_plural = "相簿列表"  # 自定義複數形式的名稱


class AlbumImage(models.Model):
    album = models.ForeignKey(Album, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Images/albums/")
    is_index = models.BooleanField(default=False)


# 商品相關
class Product(models.Model):
    STATE_CHOICES = [
        ("on_discount", "特價中"),
        ("not_sell", "缺貨中"),
        ("sold_out", "完售"),
        ("new", "新上市")
    ]

    title = models.CharField(max_length=500, verbose_name="商品名稱")
    price = models.IntegerField(verbose_name="原始價格")
    discount_price = models.IntegerField(verbose_name="特價價格")
    description = CKEditor5Field(verbose_name="商品敘述", blank=True)
    state_tag = models.CharField(max_length=100, blank=True, verbose_name="商品標籤",help_text="字樣會顯示在圖片上", choices=STATE_CHOICES)  # 顯示在圖片上的特殊標記，特價中、缺貨
    on_sell = models.BooleanField(default=True, verbose_name="販售中", help_text="若下架該商品，取消勾選")
    on_discount = models.BooleanField(default=False, verbose_name="優惠中", help_text="勾選後，顯示特價價格")
    image_index = models.ImageField(upload_to="Images/products/", verbose_name="商品照1(兼列表展示照)", default="Image/None/Noimg.jpg")
    image_2 = models.ImageField(upload_to="Images/products/", verbose_name="商品照2", default="Image/None/Noimg.jpg")
    image_3 = models.ImageField(upload_to="Images/products/", verbose_name="商品照3", default="Image/None/Noimg.jpg")
    image_4 = models.ImageField(upload_to="Images/products/", verbose_name="商品照4", default="Image/None/Noimg.jpg")
    image_5 = models.ImageField(upload_to="Images/products/", verbose_name="商品照5", default="Image/None/Noimg.jpg")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品列表"


# 訂單
class Order(models.Model):
    STATE_CHOICES = [
       ("unpaid", "未付款"),
       ("undelivered", "未出貨"),
       ("finished", "已完成"),
       ("problem",  "問題單")
    ]
    tickets_order = models.JSONField(default=list, verbose_name="票券訂單", blank=True)
    products_order = models.JSONField(default=list, verbose_name="商品訂單", blank=True)
    order_info = models.JSONField(default=list, verbose_name="訂單資料", blank=True)
    order_state = models.CharField(max_length=100, choices=STATE_CHOICES, default="unpaid", verbose_name="訂單狀態")
