from rest_framework import serializers
from .models import Activity


# JSON格式的欄位特別處理：活動的票券和曲目
class ProgramSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=500)
    composer = serializers.CharField(max_length=100)


class TicketSerializer(serializers.Serializer):
    ticket_type = serializers.CharField(max_length=500)
    price = serializers.IntegerField()
    description = serializers.CharField(max_length=1000)


class ActivitySerializer(serializers.ModelSerializer):
    poster = serializers.ImageField(max_length=None, use_url=True)
    program = ProgramSerializer(many=True)
    ticket = TicketSerializer(many=True)

    class Meta:
        model = Activity
        fields = ["id", "title", "date", "place", "poster", "program", "ticket", "description"]


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['title', 'composer']
