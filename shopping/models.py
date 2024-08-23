from django.db import models
from tinymce.models import HTMLField
from activity.models import Activity
import uuid  # 生成隨機ID

# Create your models here.


# 商品相關
class Product(models.Model):
    STATE_CHOICES = [
        ("on_discount", "特價中"),
        ("not_sell", "缺貨中"),
        ("sold_out", "完售"),
        ("new", "新上市")
    ]
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500, verbose_name="商品名稱")
    price = models.IntegerField(verbose_name="原始價格")
    discount_price = models.IntegerField(verbose_name="特價價格")
    category = models.CharField(max_length=500, verbose_name="商品種類")
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
# TODO 訂單編號有問題，無法顯示
class Cart(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, editable=False)
    deliver_paid = models.IntegerField()
    final_total = models.IntegerField()

    class Meta:
        verbose_name = "購物車"
        verbose_name_plural = "購物車列表"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    need_deliver_paid = models.BooleanField(default=True)
    sum = models.IntegerField()

    def __str__(self):
        return self.cart.id


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
