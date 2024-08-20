from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser


from .models import Activity
from .serializers import ActivitySerializer
# Create your views here.


# 活動
class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        queryset = Activity.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Activity.objects.filter(id=id)
        return queryset