from rest_framework import serializers
from .models import Event, Zone, Seat, Venue, Program, DiscountCode, Player


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
        fields = ["seat_num"]


class ZoneSerializer(serializers.ModelSerializer):
    seat = SeatSerializer(many=True, required=False)

    class Meta:
        model = Zone
        fields = ["id", "name", "price", "seat", "description", "help_words"]


class DiscountCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiscountCode
        fields = ["name", "code", "discount", "description"]


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
    discount_code = DiscountCodeSerializer(many=True)
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    weekday = serializers.SerializerMethodField()
    player = PlayerSerializer(many=True)

    class Meta:
        model = Event
        fields = ["id", "title", "date", "weekday", "time", "venue", "price_type", "poster",
                  "description", "program", "player", "zone", "discount_code"]

    def get_date(self, obj):
        return obj.date.strftime("%Y-%m-%d") if obj.date else None

    def get_time(self, obj):
        return obj.date.strftime("%H:%M") if obj.date else None

    def get_weekday(self, obj):
        if obj.date:
            weekdays = ["一", "二", "三", "四", "五", "六", "日"]
            return weekdays[obj.date.weekday()]
        return None
# TODO尚未完成票券部分
# 票
# class TicketOrderSerializer(serializers.Serializer):
#     STATE_CHOICES = [
#        ("diy", "自行選位"),
#        ("com", "電腦配位"),
#     ]
#     ticket_type = serializers.CharField(max_length=500)
#     price = serializers.IntegerField()
#     amount = serializers.IntegerField()
#     seats = serializers.CharField(max_length=800)

#     class Meta:
#         model = Product
#         fields = ["id", ]
