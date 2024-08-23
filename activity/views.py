from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination

from .models import Activity
from .serializers import ActivitySerializer
# Create your views here.


# 活動
class ActivityListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    pagination = ActivityListPagination

    def get_queryset(self):
        queryset = Activity.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Activity.objects.filter(id=id)
        return queryset