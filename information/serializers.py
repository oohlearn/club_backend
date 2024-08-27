from rest_framework import serializers
from .models import (Video, Album, Conductor, Experience, Introduction,
                     IndexStory, Article, Tag, Photo, Teacher)


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


# 指揮
class ConductorSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Conductor
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
    image = serializers.ImageField(max_length=None, use_url=True)

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
        fields = ["id", "title", "date", "description", "indexImage", "photos"]


# TODO 更改結構
# 樂團介紹
class IntroductionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Introduction
        fields = ["id", "date", "description", "indexImage", "image_2"]
