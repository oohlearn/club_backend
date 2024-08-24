from rest_framework import serializers
from .models import (Video, Album, Teacher, Experience,
                     IndexStory, Article, Tag, Photo)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']  # 假設標籤模型中有 name 欄位


# Videos
class VideoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    # use_url=True時，序列化器將會返回圖片的URL

    class Meta:
        model = Video
        fields = ["id", "title", "date", "performer",
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
    tags = serializers.SerializerMethodField()  # 使用 SerializerMethodField 自定義 tags 字段

    def get_tags(self, obj):
        # 從 Article 實例中獲取關聯的 Tag 對象，並返回它們的名稱列表
        return [tag.name for tag in obj.tags.all()]

    class Meta:
        model = Article
        fields = ["id", "title", "date", "content", "tags", "article_img"]


# 相簿
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image', 'description']


class AlbumSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, required=False)
    
    # tags = serializers.SerializerMethodField()  # 使用 SerializerMethodField 自定義 tags 字段

    # def get_tags(self, obj):
    #     # 從 Article 實例中獲取關聯的 Tag 對象，並返回它們的名稱列表
    #     return [tag.name for tag in obj.tags.all()]

    class Meta:
        model = Album
        fields = ["title", "date", "description", "indexImage", "photos"]


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
