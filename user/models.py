from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# 意見回饋
class Contact(models.Model):
    name = models.CharField(max_length=20, verbose_name="姓名", blank=True, null=True,)
    phone = models.CharField(max_length=20, verbose_name="電話", blank=True, null=True,)
    email = models.EmailField(max_length=20, verbose_name="email", blank=True, null=True,)
    category = models.CharField(max_length=20, verbose_name="問題種類", blank=True, null=True,)
    title = models.CharField(max_length=20, verbose_name="標題", blank=True, null=True,)
    content = models.TextField(verbose_name="內容", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立日期")
    reply = models.TextField(blank=True, null=True)
    replied = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.title}"

    class Meta:
        ordering = ['-created_at']


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('user', '一般用戶'),
        ('admin', '管理員'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=5, choices=USER_TYPE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

    class Meta:
        verbose_name = "用戶資料"
        verbose_name_plural = "用戶資料"


class Customer(models.Model):
    PAID_METHOD_CHOICE = [
        ("credit_card", "信用卡"),
        ("virtual_ATM", "ATM虛擬帳號"),
        ("line_pay", "Line Pay"),
        ("apple_pay", "Apple Pay"),
    ]
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
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