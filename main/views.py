from django.shortcuts import render
from .serializers import (
    RoomSerializer, BookRoomSerializer, AvalibilitySerializer, 
    BookedRoomsSerializer
)
from django.utils.timezone import make_aware, make_naive
from rest_framework.views import APIView
from django.db.models import Q
from datetime import timedelta, time, date, timezone
from .models import RoomModel, BookRoomModel
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from . import utils
from rest_framework import status
from datetime import datetime, date
from rest_framework.exceptions import NotFound
from django.http import Http404
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class RoomModelViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = RoomModel.objects.all()
    http_method_names = ['get', 'post']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']

    def get_queryset(self):
        queryset = self.queryset
        query = self.request.query_params.get('q')
        if query is not None:
            queryset = queryset.filter(name__icontains=query)
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            raise NotFound({"error":"topilmadi"})

    @action(detail=True, methods=['POST'])
    def book(self, request, *args, **kwargs):
        room = self.get_object()
        serializer = BookRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        bookedrooms = BookRoomModel.objects.filter(room_id=room)
        result = utils.check_availability(serializer.data.get('start'), serializer.data.get('end'), bookedrooms)
        if result is False:
            obj = BookRoomModel(resident=serializer.data['resident'], room_id=room,
                start=serializer.data.get('start'), end=serializer.data.get('end'))
            obj.save()
            return Response({"message":"xona muvaffaqiyatli band qilindi"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "uzr, siz tanlagan vaqtda xona band"}, status=status.HTTP_410_GONE)
    

    @action(detail=True, methods=['GET', "POST"])
    def availability(self, request, *args, **kwargs):
        room = self.get_object()
        queryset = BookRoomModel.objects.filter(room_id=room)
        if request.method == 'POST':
            serializer = AvalibilitySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # result = utils.avaliable(date=serializer.data.get('date'), queryset=queryset)
            date = datetime.strptime(serializer.data.get('date'), '%Y-%m-%d').date()
            booked_time_slots = BookRoomModel.objects.filter(
            room_id=room,
            start__date=date
            ).values_list('start', 'end')
            # booked_time_slots = [(make_naive(start), make_naive(end)) for start, end in booked_time_slots]

            start_datetime = datetime.combine(date, time.min)
            end_datetime = datetime.combine(date, time.max)
            current_datetime = start_datetime

            available_time_slots = []
            while current_datetime < end_datetime:
                next_datetime = current_datetime + timedelta(minutes=30)
                if not any(make_naive(start) <= current_datetime < make_naive(end) or make_naive(start) < next_datetime <= make_naive(end) for start, end in booked_time_slots):
                    available_time_slots.append({
                        'start': current_datetime.time().strftime('%I:%M %p'),
                        'end': next_datetime.time().strftime('%I:%M %p')
                    })
                current_datetime = next_datetime
            # return Response({'not_booked_time_slots': available_time_slots}, status=status.HTTP_200_OK)
            return Response(BookedRoomsSerializer(available_time_slots, many=True).data)

        elif request.method == 'GET':
            # result = utils.avaliable(date=date.today(), queryset=queryset)
            date = serializer.data.get('date')
            booked_time_slots = BookRoomModel.objects.filter(
            room_id=room,
            start__date=date
            ).values_list('start', 'end')
            # booked_time_slots = [(make_naive(start), make_naive(end)) for start, end in booked_time_slots]

            start_datetime = datetime.combine(date, time.min)
            end_datetime = datetime.combine(date, time.max)
            current_datetime = start_datetime

            available_time_slots = []
            while current_datetime < end_datetime:
                next_datetime = current_datetime + timedelta(minutes=30)
                if not any(make_naive(start) <= current_datetime < make_naive(end) or make_naive(start) < next_datetime <= make_naive(end) for start, end in booked_time_slots):
                    available_time_slots.append({
                        'start': current_datetime.time().strftime('%I:%M %p'),
                        'end': next_datetime.time().strftime('%I:%M %p')
                    })
                current_datetime = next_datetime
            # return Response({'not_booked_time_slots': available_time_slots}, status=status.HTTP_200_OK)
            return Response(BookedRoomsSerializer(available_time_slots, many=True).data)
    

# {         
#     "resident":{
#         "name":"Samandar"
#     },
#     "start":"2023-06-21 14:26:49.219717",
#     "end":"2023-06-21 16:26:49.219717"
# }
