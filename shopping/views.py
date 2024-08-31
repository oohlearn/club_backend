from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination

from .serializers import ProductSerializer
from .models import Product


# 商品
# 分頁
class ProductListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination = ProductListPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"title": item["title"], **item} for item in data]

        return Response({
            "products": formatted_data
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Product.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Product.objects.filter(id=id)
        return queryset
