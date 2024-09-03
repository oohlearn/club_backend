from django.db import models
from tinymce.models import HTMLField
from shortuuidfield import ShortUUIDField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction
from activity.models import Event
# 更新model內容的狀態
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    # 這個字段將用於存儲圖片
    # 可以選擇添加其他字段來描述圖片

    def __str__(self):
        return f"Image {self.id}"


class Video(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=200, verbose_name="標題")
    date = models.DateField(verbose_name="日期")
    performer = models.CharField(max_length=100, verbose_name="演出者")
    place = models.CharField(max_length=100, verbose_name="演出場地")
    description = models.TextField(blank=True, verbose_name="演出內容敘述",  null=True)
    url = models.CharField(max_length=500, verbose_name="youtube網址")
    embed_url = models.CharField(max_length=1000, blank=True,null=True, verbose_name="youtube內嵌網址(請點選youtube分享)")
    image = models.ImageField(upload_to="Images/videos/", default="Image/None/Noimg.jpg", verbose_name="封面照")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "影片"  # 自定義單數形式的名稱
        verbose_name_plural = "影片列表"  # 自定義複數形式的名稱


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = [
        ("已發佈", "已發佈"),
        ("草稿", "草稿"),
        ("下架封存", "下架封存"),
    ]
    id = ShortUUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=200, verbose_name="文章標題")
    date = models.DateField(verbose_name="日期")
    content = HTMLField(verbose_name="文章內容")
    article_img = models.ImageField(upload_to="Images/articles/", default="Image/None/Noimg.jpg", verbose_name="文章代表圖片")
    status = models.CharField(max_length=50, verbose_name="發布狀態", default="草稿", choices=STATUS_CHOICES)
    tags_input = models.CharField(max_length=300, blank=True, null=True, verbose_name="Hashtag 標記")
    tags = models.ManyToManyField(Tag, related_name="articles", blank=True)

    # def save(self, *args, **kwargs):
    #     # 在保存之前處理 tags_input
    #     if self.tags_input:
    #         tag_names = [name.strip() for name in self.tags_input.split(',')]
    #         tags = []
    #         for name in tag_names:
    #             tag, created = Tag.objects.get_or_create(name=name)
    #             tags.append(tag)
    #         self.tags.set(tags)
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = "文章"  # 自定義單數形式的名稱
        verbose_name_plural = "文章列表"  # 自定義複數形式的名稱

    def save(self, *args, **kwargs):
        # 先保存文章
        super().save(*args, **kwargs)


class HomeContent(models.Model):
    articles = models.ManyToManyField(Article, blank=True, related_name="home_contents")
    events = models.ManyToManyField(Event, blank=True, related_name="home_contents")

    def save(self, *args, **kwargs):
        # Save the instance first to get an ID
        super().save(*args, **kwargs)

        # Get the latest 5 published articles
        latest_articles = Article.objects.filter(status="已發佈").order_by('-date')[:5]
        self.articles.set(latest_articles)

        # Get the events that are currently on sale
        on_sale_events = Event.objects.filter(on_sell=True).order_by('-date')[:5]
        self.events.set(on_sale_events)


# 更新 HomeContent 实例的文章和活动
def update_home_content():
    home_content = HomeContent.objects.first()
    if home_content:
        latest_articles = Article.objects.filter(status="已發佈").order_by('-date')[:5]
        home_content.articles.set(latest_articles)

        on_sale_events = Event.objects.filter(on_sell=True).order_by('-date')[:5]
        home_content.events.set(on_sale_events)
        home_content.save()

# 当 Event 保存或删除时触发更新 HomeContent
@receiver(post_save, sender=Event)
@receiver(post_delete, sender=Event)
@receiver(post_save, sender=Article)
@receiver(post_delete, sender=Article)
def update_home_content_events(sender, instance, **kwargs):
    update_home_content()

@receiver(post_save, sender=Article)
def handle_tags(sender, instance, **kwargs):
    if instance.tags_input:
        tag_names = [name.strip() for name in instance.tags_input.split(',')]
        tags = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tags.append(tag)
        with transaction.atomic():
            instance.tags.set(tags)


class IndexStory(models.Model):
    title = models.CharField(max_length=500, verbose_name="封面故事標題")
    date = models.DateField(verbose_name="日期")
    place = models.CharField(max_length=100, blank=True, null=True, verbose_name="場地")
    btn_text = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="描述（不超過10個字）")
    image = models.ImageField(upload_to="Images/index_stories/", default="Image/None/Noimg.jpg", verbose_name="圖片")
    url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "封面故事（會在網頁上方跑馬燈）"  # 自定義單數形式的名稱
        verbose_name_plural = "封面故事列表"  # 自定義複數形式的名稱


    

# TODO 修改日期格式
class Experience(models.Model):
    date = models.DateField(verbose_name="日期", help_text="顯示範例：113年2月")
    experience = models.TextField(verbose_name="經歷標題")
    description = HTMLField(verbose_name="經歷細節介紹", blank=True, null=True,)
    image = models.ImageField(upload_to="Images/experiences/", default="Image/None/Noimg.jpg", verbose_name="圖片")

    def __str__(self):
        return self.experience

    def get_republican_year(self):
        """民國年"""
        if self.date:
            return self.date.year - 1911
        return None

    def get_formatted_date(self):
        "前端顯示格式：113年2月"
        return f"{self.get_republican_year()}年{self.date.month}月"

    class Meta:
        verbose_name = "經歷"  # 自定義單數形式的名稱
        verbose_name_plural = "經歷列表"  # 自定義複數形式的名稱


class Teacher(models.Model):
    group = models.CharField(max_length=500, verbose_name="組別", blank=True, null=True)
    name = models.CharField(max_length=500, verbose_name="老師姓名")
    description = models.TextField(blank=True, verbose_name="老師簡歷")
    image = models.ImageField(upload_to="Images/teachers/", default="Image/None/Noimg.jpg", verbose_name="照片")

    def __str__(self):
        return self.group

    class Meta:
        verbose_name = "分組老師"  # 自定義單數形式的名稱
        verbose_name_plural = "老師列表"  # 自定義複數形式的名稱


class Conductor(models.Model):
    name = models.CharField(max_length=500, verbose_name="指揮姓名")
    description = HTMLField(blank=True, null=True, verbose_name="指揮簡介")
    experiences = HTMLField(blank=True, null=True, verbose_name="指揮經歷")
    image = models.ImageField(upload_to="Images/teachers/", default="Image/None/Noimg.jpg", verbose_name="照片")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "指揮"  # 自定義單數形式的名稱
        verbose_name_plural = "指揮列表"  # 自定義複數形式的名稱


# TODO 待解決一次放入多張照片
# TODO tags
class Photo(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)
    album = models.ForeignKey('Album', related_name='photos', on_delete=models.CASCADE, verbose_name="相簿")
    image = models.ImageField(verbose_name="照片", upload_to="Images/albums/", blank=True)
    description = models.CharField(max_length=255, verbose_name="照片描述", blank=True, null=True,)

    def __str__(self):
        return self.description


class Album(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=1000, verbose_name="相簿名稱")
    date = models.DateField(verbose_name="日期")
    description = HTMLField(verbose_name="相簿介紹", blank=True, null=True,)
    indexImage = models.ImageField(verbose_name="相簿封面照", upload_to="Images/albums/", default="Image/None/Noimg.jpg")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "相簿"  # 自定義單數形式的名稱
        verbose_name_plural = "相簿列表"  # 自定義複數形式的名稱


class Introduction(models.Model):
    date = models.DateField(verbose_name="更新日期")
    description = HTMLField(verbose_name="介紹內容", blank=True, null=True)
    indexImage = models.ImageField(verbose_name="團照", upload_to="Images/intro/", default="Image/None/Noimg.jpg")
    image_2 = models.ImageField(verbose_name="LOGO", upload_to="Images/intro/", default="Image/None/Noimg.jpg")

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "樂團介紹"  # 自定義單數形式的名稱
        verbose_name_plural = "樂團介紹"  # 自定義複數形式的名稱
