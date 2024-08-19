"""
URL configuration for backend_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views import VideoViewSet, ActivityViewSet, AlbumViewSet, ArticleViewSet, IndexStoryViewSet, TeacherViewSet, ExperienceViewSet
# API
from rest_framework import routers
# static files
from django.conf.urls.static import static
from django.conf import settings

router = routers.SimpleRouter()
# 前面是path,後面是view名稱
router.register("videos", VideoViewSet)
router.register(r"activities", ActivityViewSet,  basename='activity')
router.register(r"albums", AlbumViewSet, basename="album")
router.register(r"articles", ArticleViewSet, basename="article")
router.register(r"indexStories", IndexStoryViewSet, basename="indexStory")
router.register(r"teachers", TeacherViewSet, basename="teacher")
router.register(r"experiences", ExperienceViewSet, basename="experience")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + router.urls
