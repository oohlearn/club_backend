from django.db import models
from tinymce.models import HTMLField
import uuid  # 生成隨機ID
from shortuuidfield import ShortUUIDField


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    # 這個字段將用於存儲圖片
    # 可以選擇添加其他字段來描述圖片

    def __str__(self):
        return f"Image {self.id}"


class Video(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=200, verbose_name="標題")
    date = models.DateField(verbose_name="日期")
    performer = models.CharField(max_length=100, verbose_name="演出者")
    place = models.CharField(max_length=100, verbose_name="演出場地")
    description = models.TextField(blank=True, verbose_name="演出內容敘述")
    url = models.CharField(max_length=500, verbose_name="youtube網址")
    embed_url = models.CharField(max_length=1000, blank=True, verbose_name="youtube內嵌網址(請點選youtube分享)")
    image = models.ImageField(upload_to="Images/videos/", default="Image/None/Noimg.jpg", verbose_name="封面照")


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "影片"  # 自定義單數形式的名稱
        verbose_name_plural = "影片列表"  # 自定義複數形式的名稱


class Article(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=200, verbose_name="文章標題")
    date = models.DateField(verbose_name="日期")
    content = HTMLField(verbose_name="文章內容", blank=True)
    article_img = models.ImageField(upload_to="Images/articles/", default="Image/None/Noimg.jpg", verbose_name="文章代表圖片")
    tags_input = models.CharField(max_length=300, blank=True)
    tags = models.ManyToManyField(Tag, related_name="articles", blank=True)

    def save(self, *args, **kwargs):
        # 在保存之前處理 tags_input
        if self.tags_input:
            tag_names = [name.strip() for name in self.tags_input.split(',')]
            tags = []
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            self.tags.set(tags)
        super().save(*args, **kwargs)

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


# TODO 修改日期格式
class Experience(models.Model):
    date = models.CharField(max_length=100, verbose_name="日期", help_text="格式：113年8月")
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
# TODO tags
class Photo(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    album = models.ForeignKey('Album', related_name='photos', on_delete=models.CASCADE, verbose_name="相簿")
    image = models.ImageField(verbose_name="照片", upload_to="Images/albums/")
    description = models.CharField(max_length=255, verbose_name="照片描述", blank=True)

    def __str__(self):
        return self.description


class Album(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=1000, verbose_name="相簿名稱")
    date = models.DateField(verbose_name="日期")
    description = HTMLField(verbose_name="相簿介紹", blank=True)
    indexImage = models.ImageField(verbose_name="相簿封面照", upload_to="Images/albums/", default="Image/None/Noimg.jpg")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "相簿"  # 自定義單數形式的名稱
        verbose_name_plural = "相簿列表"  # 自定義複數形式的名稱
