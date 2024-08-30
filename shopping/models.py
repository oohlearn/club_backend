from django.db import models
from tinymce.models import HTMLField
from activity.models import Activity
import uuid  # 生成隨機ID
from shortuuidfield import ShortUUIDField


# Create your models here.


# 商品相關
class Size(models.Model):
    GROUP_CHOICE = [
        ("大人、成年人", "大人、成年人"),
        ("小孩", "小孩")
    ]
    product = models.ForeignKey('Product', related_name='size_list', on_delete=models.CASCADE, verbose_name="尺寸列表")
    size = models.CharField(max_length=100, verbose_name="尺寸或顏色")
    group = models.CharField(max_length=50, verbose_name="適用族群", blank=True, choices=GROUP_CHOICE)
    description = models.CharField(max_length=255, verbose_name="備註，例：尺寸描述", blank=True)


class Product(models.Model):
    STATE_CHOICES = [
        ("特價中", "特價中"),
        ("缺貨中", "缺貨中"),
        ("完售", "完售"),
        ("新上市", "新上市")
    ]
    CATEGORY_CHOICES = [
        ("stationary", "文具"),
        ("cloth", "服飾（衣服、帽子、襪子）"),
        ("media", "演出影音")
    ]
    id = ShortUUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=500, verbose_name="商品名稱")
    price = models.IntegerField(verbose_name="原始價格")
    discount_price = models.IntegerField(verbose_name="特價價格")
    category = models.CharField(max_length=500, verbose_name="商品種類", choices=CATEGORY_CHOICES)
    description = HTMLField(verbose_name="商品敘述", blank=True)
    state_tag = models.CharField(max_length=100, blank=True, verbose_name="商品標籤",help_text="字樣會顯示在圖片上", choices=STATE_CHOICES)  # 顯示在圖片上的特殊標記，特價中、缺貨
    on_sell = models.BooleanField(default=True, verbose_name="販售中", help_text="若下架該商品，取消勾選")
    on_discount = models.BooleanField(default=False, verbose_name="優惠中", help_text="勾選後，顯示特價價格")
    index_image = models.ImageField(upload_to="Images/products/", verbose_name="商品封面照", default="Image/None/Noimg.jpg")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品列表"


# 購物車
# TODO 訂單編號有問題，無法顯示
class Cart(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)
    deliver_paid = models.IntegerField()
    final_total = models.IntegerField()

    class Meta:
        verbose_name = "購物車"
        verbose_name_plural = "購物車列表"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cartItems", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    need_deliver_paid = models.BooleanField(default=True)
    sum = models.IntegerField()

    def __str__(self):
        return self.cart.id


# 多張商品圖
class Photo(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)
    level = models.CharField(max_length=50, verbose_name="顯示順序", blank=True)
    product = models.ForeignKey(Product, related_name='photos', on_delete=models.CASCADE, verbose_name="商品")
    image_data = models.ImageField(verbose_name="其他商品照片", upload_to="Images/albums/")
    description = models.CharField(max_length=255, verbose_name="照片描述", blank=True)

    def __str__(self):
        return self.description or ""


# 訂單
class Customer(models.Model):
    PAID_METHOD_CHOICE = [
        ("credit_card", "信用卡"),
        ("virtual_ATM", "ATM虛擬帳號"),
    ]
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    address_city = models.CharField(max_length=100)
    address_district = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    paid_method = models.CharField(max_length=100, blank=True, verbose_name="付費方式", choices=PAID_METHOD_CHOICE)  # 顯示在圖片上的特殊標記，特價中、缺貨

    def __str__(self):
        return self.name


class Order(models.Model):
    STATE_CHOICES = [
       ("unpaid", "未付款"),
       ("undelivered", "未出貨"),
       ("finished", "已完成"),
       ("problem",  "問題單")
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    order_state = models.CharField(max_length=100, choices=STATE_CHOICES, default="unpaid", verbose_name="訂單狀態")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, name="products", verbose_name="商品訂單", on_delete=models.CASCADE, blank=True)
    # ticket = models.ForeignKey(Activity, name="tickets", on_delete=models.CASCADE, verbose_name="票券訂單", blank=True)
    customer = models.ForeignKey(Customer, name="customer", verbose_name="訂購人資料", on_delete=models.CASCADE)

    def __str__(self):
        return self.order.created_at.strftime('%Y-%m-%d')
