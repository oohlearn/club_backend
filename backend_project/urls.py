from django.contrib import admin
from django.urls import path, include
from shopping.views import ProductViewSet
from activity.views import EventViewSet
from information.views import (VideoViewSet, AlbumViewSet, ArticleViewSet,
                               IndexStoryViewSet, TeacherViewSet, HomeContentViewSet,
                               ExperienceViewSet, ConductorViewSet, IntroductionViewSet)
# API
from rest_framework import routers
# static files
from django.conf.urls.static import static
from django.conf import settings

router = routers.SimpleRouter()

# 前面是path,後面是view名稱
router.register("videos", VideoViewSet)
router.register(r"events", EventViewSet,  basename='event')
router.register(r"albums", AlbumViewSet, basename="album")
router.register(r"articles", ArticleViewSet, basename="article")
router.register(r"index_stories", IndexStoryViewSet, basename="indexStory")
router.register(r"teachers", TeacherViewSet, basename="teacher")
router.register(r"experiences", ExperienceViewSet, basename="experience")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"conductors", ConductorViewSet, basename="conductor")
router.register(r"introduction", IntroductionViewSet, basename="introduction")
router.register(r"home_content", HomeContentViewSet, basename="homeContent")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/information/', include(router.urls)),
    path("api/shopping/", include(router.urls)),
    path("api/activity/", include(router.urls))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + router.urls
