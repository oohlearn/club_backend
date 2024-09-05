from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from .models import Event, Seat
from .serializers import EventSerializer, SeatSerializer
# Create your views here.


# 活動
class EventListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    pagination_class = EventListPagination
    queryset = Event.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = serializer.data
        formatted_data = [{"title": item["title"], **item} for item in data]

        return Response({
            "events": formatted_data
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Event.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Event.objects.filter(id=id)
        return queryset

# TODO 座位在API的排序順序
class SeatViewSet(viewsets.ModelViewSet):
    serializer_class = SeatSerializer
    queryset = Event.objects.all()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.extra(
            select={'letter': 'SUBSTR(seat_num, 1, 1)',
                    'number': 'CAST(SUBSTR(seat_num, 2) AS INTEGER)'}
        ).order_by('letter', 'number')
