from django.db import models
from tinymce.models import HTMLField
from activity.models import Seat, SeatForNumberRow, TicketDiscountCode
import uuid  # 生成隨機ID
from shortuuidfield import ShortUUIDField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal, ROUND_HALF_UP
from django.dispatch import receiver
from decouple import config
from django.db.models.signals import post_save, post_delete




# 商品相關
class Size(models.Model):
    GROUP_CHOICE = [
        ("大人、成年人", "大人、成年人"),
        ("小孩", "小孩")
    ]
    product = models.ForeignKey('Product', related_name='size_list', on_delete=models.CASCADE, verbose_name="尺寸列表")
    size = models.CharField(max_length=100, verbose_name="尺寸或顏色")
    group = models.CharField(max_length=50, verbose_name="適用族群", blank=True, null=True, choices=GROUP_CHOICE)
    description = models.CharField(max_length=255, verbose_name="備註，例：尺寸描述", blank=True, null=True)


# TODO 處理暫售量
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
    name = models.CharField(max_length=500, verbose_name="商品名稱")
    price = models.IntegerField(verbose_name="原始價格")
    discount_price = models.IntegerField(verbose_name="特價價格", blank=True, null=True)
    category = models.CharField(max_length=500, verbose_name="商品種類", choices=CATEGORY_CHOICES, null=True)
    quantity = models.IntegerField(verbose_name="庫存總量", blank=True, null=True)
    sold_qty = models.IntegerField(verbose_name="已售出總量", blank=True, null=True)
    pre_sold_qty = models.IntegerField(verbose_name="暫時售出量", blank=True, null=True)
    description = HTMLField(verbose_name="商品敘述", blank=True, null=True)
    state_tag = models.CharField(max_length=100, blank=True, null=True, verbose_name="商品標籤",help_text="字樣會顯示在圖片上", choices=STATE_CHOICES)  # 顯示在圖片上的特殊標記，特價中、缺貨
    on_sell = models.BooleanField(default=True, verbose_name="販售中", help_text="若下架該商品，取消勾選")
    on_discount = models.BooleanField(default=False, verbose_name="優惠中", help_text="勾選後，顯示特價價格")
    index_image = models.ImageField(upload_to="Images/products/", verbose_name="商品封面照", default="Image/None/Noimg.jpg")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品列表"


# 多張商品圖
class Photo(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)
    level = models.CharField(max_length=50, verbose_name="顯示順序", blank=True)
    product = models.ForeignKey(Product, related_name='photos', on_delete=models.CASCADE, verbose_name="商品")
    image_data = models.ImageField(verbose_name="其他商品照片", upload_to="Images/albums/")
    description = models.CharField(max_length=255, verbose_name="照片描述", blank=True)

    def __str__(self):
        return self.description or ""


class ProductCode(models.Model):
    name = models.CharField(max_length=100, verbose_name="商品折扣碼名稱", help_text="例：團員優惠")
    code = models.CharField(max_length=100, verbose_name="折扣碼", help_text="例：MEMBER")
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="折扣比例，請直接寫小數，例：0.8")  # 折扣率，例如0.9表示9折
    is_valid = models.BooleanField(default=False, verbose_name="開啟優惠碼")
    end_date = models.DateField(verbose_name="有效日期", blank=True, null=True)
    description = models.CharField(max_length=100, verbose_name="備註＆說明", blank=True, null=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "商品優惠碼"
        verbose_name_plural = "商品優惠碼"


# 訂單
class Customer(models.Model):
    PAID_METHOD_CHOICE = [
        ("credit_card", "信用卡"),
        ("virtual_ATM", "ATM虛擬帳號"),
        ("line_pay", "Line Pay"),
        ("apple_pay", "Apple Pay"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name="姓名")
    email = models.EmailField(verbose_name="電子郵件")
    phone = models.CharField(max_length=20, verbose_name="電話")
    postal_code = models.CharField(max_length=10, verbose_name="郵遞區號")
    address_city = models.CharField(max_length=100, verbose_name="城市")
    address_district = models.CharField(max_length=100, verbose_name="區域")
    address = models.CharField(max_length=1000, verbose_name="詳細地址")
    paid_method = models.CharField(max_length=20, blank=True, verbose_name="付費方式", choices=PAID_METHOD_CHOICE)  

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="創建時間", null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新時間", null=True)

    class Meta:
        verbose_name = "顧客"
        verbose_name_plural = "顧客"

    def __str__(self):
        return self.name

    def get_full_address(self):
        return f"{self.postal_code} {self.address_city}{self.address_district}{self.address}"


class Order(models.Model):
    STATE_CHOICES = [
        ("unpaid", "未付款"),
        ("paid", "已付款"),
        ("processing", "處理中"),
        ("shipped", "已出貨"),
        ("delivered", "已送達"),
        ("completed", "已完成"),
        ("cancelled", "已取消"),
        ("refunded", "已退款"),

    ]
    id = ShortUUIDField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="訂單總金額", null=True)
    shipping_fee = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="運費", null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="折扣金額", null=True)


# TODO 優惠碼待修正
class Cart(models.Model):
    STATE_CHOICES = [
       ("unpaid", "未付款"),
       ("undelivered", "已付款，未出貨"),
       ("delivered", "已出貨"),
       ("finished", "已出貨"),
       ("problem",  "問題單"),
       ("canceled",  "已取消"),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, name="customer", verbose_name="訂購人資料", on_delete=models.CASCADE)
    ticket_discount_code = models.ForeignKey(TicketDiscountCode,
                                             related_name="ticket_discount_code",
                                             on_delete=models.SET_NULL, null=True, blank=True)
    product_code = models.ForeignKey(ProductCode,
                                     related_name="product_code",
                                     on_delete=models.SET_NULL, null=True, blank=True)
    need_deliver_paid = models.BooleanField(default=True, verbose_name="要加運費")
    total_price = models.IntegerField(null=True, verbose_name="訂單總金額", blank=True)
    status = models.CharField(max_length=100, choices=STATE_CHOICES, default="unpaid", verbose_name="訂單狀態")
    deliver_price = models.IntegerField(null=True, verbose_name="運費金額", blank=True, default=config("DELIVER_PAID"))

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # 首先保存對象以獲得 primary key
        if is_new:
            self.total_price = 0  # 初始化總價為0
        self.update_total_price()  # 對於已存在的訂單，更新總價

    def update_total_price(self):
        total = self.calculate_total_price()
        Cart.objects.filter(pk=self.pk).update(total_price=total,
                                               need_deliver_paid=self.need_deliver_paid,
                                               deliver_price=self.deliver_price)
        # 重新從數據庫加載更新後的值
        self.refresh_from_db()

    def calculate_total_price(self):
        products_total = sum(item.get_product_subtotal() for item in self.cartItem.all())
        tickets_total = sum(item.get_ticket_subtotal() for item in self.cartItem.all())
        total = products_total + tickets_total + self.deliver_price

        if self.product_code:
            products_total *= self.product_code.discount
        if self.ticket_discount_code:
            tickets_total *= self.ticket_discount_code.discount

        if tickets_total > 0:
            self.need_deliver_paid = False

        if not self.need_deliver_paid:
            self.deliver_price = 0
        else:
            self.deliver_price = config("DELIVER_PAID")

        # 將結果四捨五入到最接近的整數
        return int(Decimal(total).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d %H:%M')} :  {self.customer.name}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cartItem", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    size = models.CharField(max_length=20, verbose_name="尺寸或顏色", null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, null=True, blank=True)
    seat_v2 = models.ForeignKey(SeatForNumberRow, on_delete=models.CASCADE, null=True, blank=True)

    def get_product_subtotal(self):
        if self.product:
            return self.product.price * self.quantity
        return 0

    def get_ticket_subtotal(self):
        if self.seat:
            return self.seat.price
        if self.seat_v2:
            return self.seat_v2.price
        return 0

    def clean(self):
        if not self.product and not self.seat and not self.seat_v2:
            raise ValidationError("At least one of product, seat, or seat_v2 must be specified.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.update_total_price()

    def __str__(self):
        items = []
        if self.product:
            items.append(f"商品：{self.product.name} 個{self.quantity} ")
        if self.seat:
            items.append(f"票券：{self.seat.zone.event.title} {self.seat.seat_num}")
        if self.seat_v2:
            items.append(f"票券：{self.seat_v2.zone.event.title} {self.seat_v2.area}區{self.seat_v2.row_num}排{self.seat_v2.seat_num}號")
        return ", ".join(items) if items else "Empty order item"



@receiver(post_save, sender=CartItem)
def update_cart_total_on_cartItem_save(sender, instance, **kwargs):
    instance.cart.update_total_price()

@receiver(post_delete, sender=CartItem)
def update_cart_total_on_cartitem_delete(sender, instance, **kwargs):
    instance.cart.update_total_price()

@receiver(post_save, sender=Cart)
def update_cart_total_on_cart_save(sender, instance, **kwargs):
    instance.update_total_price()