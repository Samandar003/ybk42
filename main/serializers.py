from .models import RoomModel, BookRoomModel
from rest_framework import serializers
from django.utils import timezone
from datetime import date, datetime
from rest_framework import serializers

class RoomSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=RoomModel.CHOICES)
    class Meta:
        model = RoomModel
        fields = ['id', 'name', 'type', 'capacity']
    
class ResidentSerializer(serializers.Serializer):
    name = serializers.CharField()

class BookRoomSerializer(serializers.ModelSerializer):
    resident = ResidentSerializer()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    class Meta:
        model = BookRoomModel
        fields = ["resident", "start", "end"]
        
    def validate(self, data):
        start = data.get("start")
        end = data.get("end")
        current_datetime = timezone.now()
        if start < current_datetime or end < current_datetime:
            raise serializers.ValidationError("Datetime can't be in the past")
        if start >= end:
            raise serializers.ValidationError("Ending datetime of booking must be later than the starting datetime")
        return data
    
class BookedRoomsSerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    
class AvalibilitySerializer(serializers.Serializer):
    date = serializers.DateField(default=date.today)
    

