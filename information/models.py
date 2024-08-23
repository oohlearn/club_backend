from django.db import models
from taggit.managers import TaggableManager
from tinymce.models import HTMLField
import uuid  # 生成隨機ID


class Video(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
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
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=200, verbose_name="文章標題")
    date = models.DateField(verbose_name="日期")
    content = HTMLField(verbose_name="文章內容", blank=True)
    tags = TaggableManager(help_text="請以逗號分隔標籤", blank=True)  # 添加tag管理器，並自定義說明文字
    article_img = models.ImageField(upload_to="Images/articles/", default="Image/None/Noimg.jpg", verbose_name="文章代表圖片")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章"  # 自定義單數形式的名稱
        verbose_name_plural = "文章列表"  # 自定義複數形式的名稱





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
    description = HTMLField(verbose_name="經歷細節介紹", blank=True)
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
    description = HTMLField(verbose_name="相簿介紹", blank=True)
    tags = TaggableManager(help_text="請以逗號分隔標籤", blank=True)
    indexImage = models.ImageField(verbose_name="相簿封面照", upload_to="Images/albums/", default="Image/None/Noimg.jpg")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "相簿"  # 自定義單數形式的名稱
        verbose_name_plural = "相簿列表"  # 自定義複數形式的名稱


class AlbumImage(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    album = models.ForeignKey(Album, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Images/albums/")
    is_index = models.BooleanField(default=False)
