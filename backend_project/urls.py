from django.contrib import admin
from django.urls import path, include
from shopping.views import (ProductViewSet, OrderViewSet,
                            ProductCodeViewSet, CartViewSet,
                            CreateCartView, CartDetailView, SizeViewSet)
from user.views import create_contact, register_user, login_user, validate_token, register_admin
from activity.views import EventViewSet, ZoneViewSet, SeatViewSet
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
    # 管理者
    path('admin/', admin.site.urls),
    path('api/admin-register/', register_admin, name='register_admin'),
    # 資訊
    path('api/information/', include(router.urls)),
    # 使用者
    path('api/user/register/', register_user, name='register_user'),
    path('api/user/login/', login_user, name='login_user'),
    # 售票活動
    path("api/activity/", include(router.urls)),
    path('activity/events/<int:event_id>/zones/<int:pk>/', ZoneViewSet.as_view({'patch': 'update_remain'}), name='zone-update-remain'),
    path('api/activity/<str:event_id>/seats/<int:pk>/', SeatViewSet.as_view({'patch': 'update_status'}), name='seat-update-status'),
    # 購物
    path("api/shopping/", include(router.urls)),
    path('api/create-cart/', CreateCartView.as_view(), name='create_cart'),
    path('api/cart/<str:pk>/', CartDetailView.as_view(), name='cart_detail'),
    # 單一產品詳情
    path('api/shopping/products/<str:id>', ProductViewSet.as_view({'get': 'retrieve'}), name='product-detail'),
    # 獲取產品的所有尺寸
    path('api/shopping/products/<str:id>/sizes/', SizeViewSet.as_view({'get': 'list'}), name='product-sizes-list'),

    # 獲取產品的特定尺寸
    path('api/shopping/products/<str:id>/sizes/<int:pk>/', SizeViewSet.as_view({'get': 'retrieve'}), name='product-size-detail'),

    # 更新產品特定尺寸的預售數量
    path('api/shopping/products/<str:id>/sizes/<int:pk>/pre_sold/',
         SizeViewSet.as_view({'post': 'update_pre_sold'}), name='product-size-pre-sold'),

    # 釋放產品特定尺寸的預售數量
    path('api/shopping/products/<str:id>/sizes/<int:pk>/release_pre_sold/',
         SizeViewSet.as_view({'post': 'release_pre_sold'}), name='product-size-release-pre-sold'),
    # 優惠碼檢查
    path('api/shopping/productCode/', ProductCodeViewSet.as_view({'get': 'list'}), name='product-code'),
    # 其他
    path('api/contact/', create_contact, name='create_contact'),
    path('api/validate-token/', validate_token, name='validate_token'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + router.urls
