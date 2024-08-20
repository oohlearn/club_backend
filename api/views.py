from django.shortcuts import render
from .models import (Video, Activity, IndexStory, Album, Article, Experience,
                     Teacher, Product)

# Create your views here.
from rest_framework import viewsets
from .serializers import (VideoSerializer, ActivitySerializer,
                          IndexStorySerializer, AlbumSerializer,
                          ArticleSerializer, ExperienceSerializer,
                          TeacherSerializer, ProductSerializer)
from rest_framework.parsers import MultiPartParser, FormParser


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
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        album_data = request.data

        album_serializer = self.get_serializer(data=album_data)
        album_serializer.is_valid(raise_exception=True)
        album = album_serializer.save()

        for image in images:
            AlbumImage.objects.create(album=album, image=image)

        return Response(album_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if images:
            instance.images.all().delete()  # 刪除舊圖片
            for image in images:
                AlbumImage.objects.create(album=instance, image=image)

        return Response(serializer.data)

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


# 商品
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer