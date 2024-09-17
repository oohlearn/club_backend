from django.db import models


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
