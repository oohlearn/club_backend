from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination

from .serializers import CartProductsSerializer, ProductSerializer
from .models import Product, Cart


# 商品
# 分頁
class ProductListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    pagination = ProductListPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Product.objects.filter(id=id)
        return queryset
