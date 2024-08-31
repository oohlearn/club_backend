from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
from .models import (Video, IndexStory, Album, Article, Experience, Conductor,
                     Teacher, Introduction)
from .serializers import (VideoSerializer,
                          IndexStorySerializer, AlbumSerializer,
                          ArticleSerializer, ExperienceSerializer,
                          TeacherSerializer, ConductorSerializer, IntroductionSerializer)


# 影片
class VideoListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by("-date")
    serializer_class = VideoSerializer
    pagination_class = VideoListPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"title": item["title"], **item} for item in data]

        return Response({
            "videos": formatted_data
        }, status=status.HTTP_200_OK)


# 文章
class ArticleListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = ArticleListPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"title": item["title"], **item} for item in data]

        return Response({
            "articles": formatted_data
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Article.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Article.objects.filter(id=id)
        return queryset


# 相簿
class AlbumListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    parser_classes = (MultiPartParser, FormParser)
    pagination = AlbumListPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"title": item["title"], **item} for item in data]

        return Response({
            "albums": formatted_data
        }, status=status.HTTP_200_OK)

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

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"title": item["name"], **item} for item in data]

        return Response({
            "teachers": formatted_data
        }, status=status.HTTP_200_OK)


# 指揮
class ConductorViewSet(viewsets.ModelViewSet):
    serializer_class = ConductorSerializer
    queryset = Conductor.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"title": item["name"], **item} for item in data]

        return Response({
            "conductors": formatted_data
        }, status=status.HTTP_200_OK)


# 封面故事
class IndexStoryViewSet(viewsets.ModelViewSet):
    serializer_class = IndexStorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"title": item["title"], **item} for item in data]

        return Response({
            "indexStories": formatted_data
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = IndexStory.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = IndexStory.objects.filter(id=id)
        return queryset


# 經歷
class ExperienceListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    pagination = ExperienceListPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"title": item["experience"], **item} for item in data]

        return Response({
            "experiences": formatted_data
        }, status=status.HTTP_200_OK)


# 樂團介紹
class IntroductionViewSet(viewsets.ModelViewSet):
    serializer_class = IntroductionSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = Introduction.objects.all()
        return queryset
