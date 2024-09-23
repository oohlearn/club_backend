from django.contrib import admin
from django.urls import path, include
from shopping.views import (ProductViewSet, OrderViewSet,
                            ProductCodeViewSet, CartViewSet,
                            CreateCartView, CartDetailView)
from user.views import create_contact, register_user, login_user, validate_token, register_admin
from activity.views import EventViewSet, ZoneViewSet
from information.views import (VideoViewSet, AlbumViewSet, ArticleViewSet,
                               IndexStoryViewSet, TeacherViewSet,
                               HomeContentViewSet,
                               ExperienceViewSet, ConductorViewSet,
                               IntroductionViewSet)

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
router.register(r'zones', ZoneViewSet, basename="zones")
router.register(r'carts', CartViewSet, basename="carts")
router.register(r'orders', OrderViewSet, basename="orders")
router.register(r'productCode', ProductCodeViewSet, basename="productCode")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/information/', include(router.urls)),
    path("api/shopping/", include(router.urls)),
    path("api/activity/", include(router.urls)),
    path('activity/events/<int:event_id>/zones/<int:pk>/', ZoneViewSet.as_view({'patch': 'update_remain'}), name='zone-update-remain'),
    path('api/contact/', create_contact, name='create_contact'),
    path('api/user/register/', register_user, name='register_user'),
    path('api/admin-register/', register_admin, name='register_admin'),
    path('api/user/login/', login_user, name='login_user'),
    path('api/validate-token/', validate_token, name='validate_token'),
    path('api/create-cart/', CreateCartView.as_view(), name='create_cart'),
    path('api/cart/<str:pk>/', CartDetailView.as_view(), name='cart_detail'),





]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + router.urls
