from rest_framework import serializers
from .models import Event, Zone, Seat, Venue, Program, DiscountCode


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["title", "composer"]


class SeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seat
        fields = ["seat_num"]


class ZoneSerializer(serializers.ModelSerializer):
    seat = SeatSerializer(many=True, required=False)

    class Meta:
        model = Zone
        fields = ["id", "name", "price", "seat"]


class DiscountCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DiscountCode
        fields = ["name", "code", "discount", "description"]


class VenueSerializer(serializers.ModelSerializer):
    official_img = serializers.ImageField(max_length=None, use_url=True)
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
    discount_code = DiscountCodeSerializer(many=True)

    class Meta:
        model = Event
        fields = ["id", "title", "date", "place", "venue", "poster",
                  "description", "program", "zone", "discount_code"]
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