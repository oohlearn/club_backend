from django.db import models
from tinymce.models import HTMLField


# Create your models here.


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
    description = HTMLField(verbose_name="商品敘述", blank=True)
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


# 購物車
class ProductCart(models.Model):
    products = models.JSONField()
    need_deliver_paid = models.BooleanField(default=True)
    total = models.IntegerField()


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


