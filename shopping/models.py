from django.db import models
from tinymce.models import HTMLField
from activity.models import Seat, SeatForNumberRow, TicketDiscountCode
import uuid  # 生成隨機ID
from shortuuidfield import ShortUUIDField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal, ROUND_HALF_UP


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
       ("undelivered", "未出貨"),
       ("finished", "已完成"),
       ("problem",  "問題單"),
       ("canceled",  "已取消"),

    ]
    id = ShortUUIDField(primary_key=True, editable=False)    
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, name="customer", verbose_name="訂購人資料", on_delete=models.CASCADE)
    need_deliver_paid = models.BooleanField(default=True, verbose_name="要加運費")
    total_price = models.IntegerField(null=True, verbose_name="訂單總金額", blank=True)
    status = models.CharField(max_length=100, choices=STATE_CHOICES, default="unpaid", verbose_name="訂單狀態")
    deliver_price = models.IntegerField(null=True, verbose_name="運費金額", blank=True, default=70)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # 首先保存對象以獲得 primary key
        if is_new:
            self.total_price = 0  # 初始化總價為0
        else:
            self.update_total_price()  # 對於已存在的訂單，更新總價

    def update_total_price(self):
        total = self.calculate_total_price()
        Order.objects.filter(pk=self.pk).update(total_price=total, need_deliver_paid=self.need_deliver_paid)
        # 重新從數據庫加載更新後的值
        self.refresh_from_db()

    def calculate_total_price(self):
        total = sum(item.calculate_subtotal() for item in self.orderItem.all())

        if total > 500:
            self.need_deliver_paid = False

        if self.need_deliver_paid:
            # 假設運費是固定的100元
            total += self.deliver_price

        # 將結果四捨五入到最接近的整數
        return int(Decimal(total).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d %H:%M')} :  {self.customer.name}"

# TODO 優惠碼待修正

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orderItem", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    size = models.CharField(max_length=20, verbose_name="尺寸或顏色", null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    ticket_discount_code = models.ForeignKey(TicketDiscountCode,
                                             related_name="ticket_discount_code",
                                             on_delete=models.SET_NULL, null=True, blank=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, null=True, blank=True)
    seat_v2 = models.ForeignKey(SeatForNumberRow, on_delete=models.CASCADE, null=True, blank=True)
    product_code = models.ForeignKey(ProductCode, 
                                     related_name="product_code",
                                     on_delete=models.SET_NULL, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def clean(self):
        if not self.product and not self.seat and not self.seat_v2:
            raise ValidationError("At least one of product, seat, or seat_v2 must be specified.")

    def save(self, *args, **kwargs):
        self.subtotal = self.calculate_subtotal()
        super().save(*args, **kwargs)
        self.update_order_total()

    def calculate_subtotal(self):
        subtotal = 0
        if self.product:
            product_price = self.product.price * self.quantity
            if self.product_code:
                product_price *= self.product_code.discount
            subtotal += product_price

        if self.seat:
            seat_price = self.seat.price
            if self.ticket_discount_code.is_valid:
                seat_price *= self.ticket_discount_code.discount
            subtotal += seat_price

        if self.seat_v2:
            seat_v2_price = self.seat_v2.price
            if self.ticket_discount_code:
                seat_v2_price *= self.ticket_discount_code.discount
            subtotal += seat_v2_price

        return int(Decimal(subtotal).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

    def update_order_total(self):
        order_total = sum(item.subtotal for item in self.order.orderItem.all())
        self.order.total_amount = order_total
        self.order.save()

    def __str__(self):
        items = []
        if self.product:
            items.append(f"商品：{self.product.name} 個{self.quantity} ")
        if self.seat:
            items.append(f"票券：{self.seat.zone.event.title} {self.seat.seat_num}")
        if self.seat_v2:
            items.append(f"票券：{self.seat_v2.zone.event.title} {self.seat_v2.area}區{self.seat_v2.row_num}排{self.seat_v2.seat_num}號")
        return ", ".join(items) if items else "Empty order item"