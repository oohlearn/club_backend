from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
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
    pagination_class = ActivityListPagination
    queryset = Activity.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"title": item["title"], **item} for item in data]

        return Response({
            "articles": formatted_data
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Activity.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Activity.objects.filter(id=id)
        return queryset
