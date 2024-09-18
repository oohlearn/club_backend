from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination

from .serializers import ProductSerializer, OrderSerializer, ProductDiscountCodeSerializer, CartSerializer
from .models import Product, Order, ProductCode, Cart


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
        formatted_data = [{"name": item["name"], **item} for item in data]

        return Response({
            "products": formatted_data
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Product.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Product.objects.filter(id=id)
        return queryset


# 購物車
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"created_at": item["created_at"], **item} for item in data]

        return Response({
            "cart": formatted_data
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Cart.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Cart.objects.filter(id=id)
        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"id": item["id"], **item} for item in data]

        return Response({
            "order": formatted_data
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Order.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Order.objects.filter(id=id)
        return queryset


class ProductCodeViewSet(viewsets.ModelViewSet):
    queryset = ProductCode.objects.all()
    serializer_class = ProductDiscountCodeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"name": item["name"], **item} for item in data]

        return Response({
            "productCode": formatted_data
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = ProductCode.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = ProductCode.objects.filter(id=id)
        return queryset
