from django.shortcuts import render
from .serializers import CartProductsSerializer, ProductSerializer
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Product, ProductCart


# Create your views here.
# 商品
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Product.objects.filter(id=id)
        return queryset
