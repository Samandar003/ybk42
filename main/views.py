from django.shortcuts import render
from .serializers import RoomSerializer, BookRoomSerializer
from .models import RoomModel, BookRoomModel
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from . import utils

class RoomModelViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = RoomModel.objects.all()

    @action(detail=True, methods=['POST'])
    def book(self, request, *args, **kwargs):
        room = self.get_object()
        serializer = BookRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bookedrooms = BookRoomModel.objects.filter(room_id=room)
        result = utils.check_availability(serializer.data.get('start'), serializer.data.get('end'), bookedrooms)
        print(result)
        obj = BookRoomModel(resident=serializer.data.get('resident'), room_id=room,
            start=serializer.data.get('start'), end=serializer.data.get('end'))
        obj.save()
        return Response(f"{room} room is booked")
        
    # @action(detail=True, mthods=['GET'])
    # def availability(self, request, *args, **kwargs):
    #     room = self.get_object()
        
        

