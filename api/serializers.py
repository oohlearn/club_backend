from rest_framework import serializers
from .models import (Video, Activity, Album, AlbumImage, Teacher, Experience,
                     IndexStory, Article, Product, Order)
from taggit.serializers import (TagListSerializerField, TaggitSerializer)


# Videos
class VideoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    # use_url=True時，序列化器將會返回圖片的URL
    tags = TagListSerializerField()

    class Meta:
        model = Video
        fields = ["id", "title", "date", "performer", "tags",
                  "place", "description", "url", "embed_url", "image"]


# JSON格式的欄位特別處理：活動的票券和曲目、文章和相簿的tag
class ProgramSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=500)
    composer = serializers.CharField(max_length=100)


class TicketSerializer(serializers.Serializer):
    ticket_key = serializers.CharField(max_length=500)
    ticket_type = serializers.CharField(max_length=500)
    price = serializers.IntegerField()
    description = serializers.CharField(max_length=1000)


class ActivitySerializer(serializers.ModelSerializer):
    poster = serializers.ImageField(max_length=None, use_url=True)
    program = ProgramSerializer(many=True)
    ticket = TicketSerializer(many=True)

    class Meta:
        model = Activity
        fields = ["id", "title", "date", "place", "poster", "program", "ticket", "description"]


# 老師
class TeacherSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Teacher
        fields = '__all__'


# 封面故事
class IndexStorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = IndexStory
        fields = '__all__'


# 經歷
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'


# 文章
class ArticleSerializer(serializers.ModelSerializer):
    article_img = serializers.ImageField(max_length=None, use_url=True)
    tags = TagListSerializerField()

    class Meta:
        model = Article
        fields = ["id", "title", "date", "content", "tags", "article_img"]


# 相簿
class AlbumImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumImage
        fields = ['id', 'image', 'is_index']


class AlbumSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    images = AlbumImageSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ["title", "date", "description", "tags", "indexImage", "images"]


# 商品
class ProductSerializer(serializers.ModelSerializer):
    image_index = serializers.ImageField(max_length=None, use_url=True)
    image_2 = serializers.ImageField(max_length=None, use_url=True)
    image_3 = serializers.ImageField(max_length=None, use_url=True)
    image_4 = serializers.ImageField(max_length=None, use_url=True)
    image_5 = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Product
        fields = ["id", "title", "price", "discount_price", "state_tag",
                  "description", "on_sell", "on_discount", "image_index",
                  "image_2", "image_3", "image_4", "image_5"]


# 訂單
   
# 票
class TicketOrderSerializer(serializers.Serializer):
    
    ticket = serializers.CharField(max_length=500)
    price = serializers.IntegerField()
    description = serializers.CharField(max_length=1000)
# 商品
# 購買人資訊
# class OrderSerializer(serializers.ModelSerializer):
    