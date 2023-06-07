from .models import RoomModel, BookRoomModel
from rest_framework import serializers

class RoomSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=RoomModel.CHOICES)
    class Meta:
        model = RoomModel
        fields = ['name', 'type', 'capacity']
    
class BookRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookRoomModel
        fields = "__all__"


