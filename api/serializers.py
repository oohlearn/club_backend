from rest_framework import serializers
from .models import Video, Activity, Album, Teacher, Experience, IndexStory, Article
from taggit.serializers import (TagListSerializerField, TaggitSerializer)


# Videos
class VideoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    # use_url=True時，序列化器將會返回圖片的URL

    class Meta:
        model = Video
        fields = ["id", "title", "date", "performer", "tags"
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
        fields = ["title", "date", "place", "poster", "program", "ticket", "description"]


# 老師
class TeacherSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Teacher
        fields = '__all__'


# 相簿
class AlbumSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    tags = TagListSerializerField()

    class Meta:
        model = Album
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
        fields = ["title", "date", "content", "tags", "article_img"]
