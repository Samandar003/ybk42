from django.shortcuts import render
from .serializers import RoomSerializer, BookRoomSerializer
from .models import RoomModel, BookRoomModel
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
class RoomModelViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = RoomModel.objects.all()

    @action(detail=True, methods=['POST'])
    def book(self, request, *args, **kwargs):
        


