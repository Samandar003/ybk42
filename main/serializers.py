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
    start = serializers.DateTimeField(input_formats=["%d-%m-%Y %H:%M:%S"])
    end = serializers.DateTimeField(input_formats=["%d-%m-%Y %H:%M:%S"])

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
    
    def validate_start(self, value):
        try:
            value.strftime('%d-%m-%Y %H:%M:%S')
        except ValueError:
            raise serializers.ValidationError("Invalid datetime format. Expected '%d-%m-%Y %H:%M:%S'.")
        return value
    
    def validate_end(self, value):
        try:
            value.strftime('%d-%m-%Y %H:%M:%S')
        except ValueError:
            raise serializers.ValidationError("Invalid datetime format. Expected '%d-%m-%Y %H:%M:%S'.")
        return value
    def create(self, validated_data):
        resident_name = validated_data.pop("resident")
        start = validated_data.pop("start")
        end = validated_data.pop("end")
        return BookRoomModel.objects.create(resident=resident_name, start=start, end=end)
        
class BookedRoomsSerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    

class CustomDateTimeField(serializers.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs['format'] = '%d-%m-%Y %H:%M:%S'
        super().__init__(*args, **kwargs)
    
class AvalibilitySerializer(serializers.Serializer):
    date = serializers.DateField(default=date.today, input_formats=['%d-%m-%Y'])

    # def validate_date(self, value):
    #     try:
    #         value.strftime('%d-%m-%Y')
    #     except ValueError:
    #         raise serializers.ValidationError("Invalid date format. Expected '%d-%m-%Y'.")
    #     return value