from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Event, Seat, Zone, ZoneForNumberRow
from .serializers import EventSerializer, SeatSerializer, ZoneForNumberRowSerializer, ZoneSerializer
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
    queryset = Seat.objects.all()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.extra(
            select={'letter': 'SUBSTR(seat_num, 1, 1)',
                    'number': 'CAST(SUBSTR(seat_num, 2) AS INTEGER)'}
        ).order_by('letter', 'number')


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    @action(detail=True, methods=['patch'], url_path='update-remain')
    def update_remain(self, request, pk=None, event_id=None):
        zone = self.get_object()
        remain = request.data.get('remain')
        if remain is not None:
            zone.remain = remain
            zone.save()
        return Response(ZoneSerializer(zone).data)
