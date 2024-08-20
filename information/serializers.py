from rest_framework import serializers
from .models import (Video, Album, AlbumImage, Teacher, Experience,
                     IndexStory, Article)
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


# 票
# class TicketOrderSerializer(serializers.Serializer):
#     STATE_CHOICES = [
#        ("diy", "自行選位"),
#        ("com", "電腦配位"),
#     ]
#     ticket_type = serializers.CharField(max_length=500)
#     price = serializers.IntegerField()
#     amount = serializers.IntegerField()
#     seats = serializers.CharField(max_length=800)

#     class Meta:
#         model = Product
#         fields = ["id", ]
