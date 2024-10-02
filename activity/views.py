from django.shortcuts import render
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Event, Seat, Zone, ZoneForNumberRow
from .serializers import EventSerializer, SeatSerializer, ZoneForNumberRowSerializer, ZoneSerializer

from datetime import datetime, time
from django.utils.timezone import make_aware


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
        page = self.paginate_queryset(queryset)

        data = serializer.data
        formatted_data = [{"title": item["title"], **item} for item in data]

        if page is not None:
            print("Page data count:", len(page))
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            formatted_data = [{"title": item["title"], **item} for item in data]
            return self.get_paginated_response(formatted_data)
        return Response({
            "events": formatted_data,
            "total": queryset.count()
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Event.objects.all()
        id = self.request.query_params.get('id')
        if id is not None:
            queryset = Event.objects.filter(id=id)

        # 處理搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # 處理日期過濾
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                start_datetime = make_aware(datetime.combine(start_date, time.min))
                end_datetime = make_aware(datetime.combine(end_date, time.max))
                queryset = queryset.filter(date__range=[start_datetime, end_datetime])
            except ValueError:
                # 如果日期格式不正確，我們可以選擇忽略這個過濾條件
                pass
        elif start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                start_datetime = make_aware(datetime.combine(start_date, time.min))

                queryset = queryset.filter(date__gte=start_datetime)
            except ValueError:
                pass
        elif end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                end_datetime = make_aware(datetime.combine(end_date, time.max))

                queryset = queryset.filter(date__lte=end_datetime)
            except ValueError:
                pass
        return queryset

    def get_paginated_response(self, data):
        return Response({
            'events': data,
            'total': self.paginator.page.paginator.count,
            'page': self.paginator.page.number,
            'page_size': self.paginator.page.paginator.per_page
        })


# TODO 座位在API的排序順序
class SeatViewSet(viewsets.ModelViewSet):
    serializer_class = SeatSerializer
    queryset = Seat.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.extra(
            select={'letter': 'SUBSTR(seat_num, 1, 1)',
                    'number': 'CAST(SUBSTR(seat_num, 2) AS INTEGER)'}
        ).order_by('letter', 'number')

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None, event_id=None):
        seat = self.get_object()
        new_status = request.data.get('status')
        if new_status in ['on_sell', 'padding']:
            seat.status = new_status
            seat.save()
            return Response({'status': 'success', 'message': f'座位 {seat.seat_num} 狀態已更新為 {new_status}'})
        return Response({'status': 'error', 'message': '無效的狀態'}, status=status.HTTP_400_BAD_REQUEST)


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
