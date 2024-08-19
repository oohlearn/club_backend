from django.shortcuts import render
from .models import Video, Activity, IndexStory, Album, Article, Experience, Teacher

# Create your views here.
from rest_framework import viewsets
from .serializers import VideoSerializer, ActivitySerializer, IndexStorySerializer, AlbumSerializer, ArticleSerializer, ExperienceSerializer, TeacherSerializer


# 影片
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


# 活動
class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        queryset = Activity.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Activity.objects.filter(id=id)
        return queryset


# 文章
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Article.objects.filter(id=id)
        return queryset


# 相簿
class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer

    def get_queryset(self):
        queryset = Album.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Album.objects.filter(id=id)
        return queryset


# 老師
class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


# 封面故事
class IndexStoryViewSet(viewsets.ModelViewSet):
    serializer_class = IndexStorySerializer

    def get_queryset(self):
        queryset = IndexStory.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = IndexStory.objects.filter(id=id)
        return queryset


# 經歷
class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
