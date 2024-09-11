from rest_framework import serializers
from .models import Event, Zone, Seat, Venue, Program, TicketDiscountCode, Player, SeatForNumberRow, ZoneForNumberRow
import re


# TODO 座位資料整理



class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["title", "composer"]


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["title", "name"]


class SeatSerializer(serializers.ModelSerializer):


    class Meta:
        model = Seat
        fields = ["seat_num","area", "price", "color", "not_sell", "is_sold", "is_chair"]


class ZoneSerializer(serializers.ModelSerializer):
    seat = SeatSerializer(many=True, required=False)

    class Meta:
        model = Zone
        fields = ["id", "name", "eng_name", "area", "remain", "color", "price", "seat", "description", "help_words"]

    def get_remain(self, obj):
        return obj.seat.filter(is_sold=False, not_sell=False).count()

    def update(self, instance, validated_data):
        remain = validated_data.get('remain', instance.remain)
        instance.remain = remain
        instance.save()
        return instance


class TicketDiscountCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketDiscountCode
        fields = ["name", "code", "discount", "is_valid", "description"]


# Number Row
class SeatFroNumberRowSerializer(serializers.ModelSerializer):

    class Meta:
        model = SeatForNumberRow
        fields = ["row_num", "seat_num", "area", "price", "color", "not_sell", "is_sold", "is_chair"]


class ZoneForNumberRowSerializer(serializers.ModelSerializer):
    seat = SeatFroNumberRowSerializer(many=True, required=False)

    class Meta:
        model = Zone
        fields = ["id", "name", "eng_name", "area", "remain", "color", "price", "seat", "description", "help_words"]


class VenueSerializer(serializers.ModelSerializer):
    official_seat_image = serializers.ImageField(max_length=None, use_url=True)
    # use_url=True時，序列化器將會返回圖片的URL

    class Meta:
        model = Venue
        fields = ["id", "name", "total_seats",
                  "address", "traffic_info", "map_url",
                  "official_seat_image"]


class EventSerializer(serializers.ModelSerializer):
    poster = serializers.ImageField(max_length=None, use_url=True)
    program = ProgramSerializer(many=True)
    zone = ZoneSerializer(many=True)
    venue = VenueSerializer()
    ticket_discount_code = TicketDiscountCodeSerializer(many=True, required=False)
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    weekday = serializers.SerializerMethodField()
    player = PlayerSerializer(many=True)
    zoneForNumberRow = ZoneForNumberRowSerializer(many=True)

    class Meta:
        model = Event
        fields = ["id", "title", "date", "weekday", "time", "venue", "price_type", "poster",
                  "description", "program", "player", "ticket_system_url", "zone", "discount_code",
                  "zoneForNumberRow", "ticket_discount_code"]

    def get_date(self, obj):
        return obj.date.strftime("%Y-%m-%d") if obj.date else None

    def get_time(self, obj):
        return obj.date.strftime("%H:%M") if obj.date else None

    def get_weekday(self, obj):
        if obj.date:
            weekdays = ["一", "二", "三", "四", "五", "六", "日"]
            return weekdays[obj.date.weekday()]
        return None
