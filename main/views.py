from django.shortcuts import render
from .serializers import (
    RoomSerializer, BookRoomSerializer, AvalibilitySerializer, 
    BookedRoomsSerializer
)
from django.utils.timezone import make_aware, make_naive
from rest_framework.views import APIView
from django.db.models import Q
from datetime import timedelta, time, date, timezone, datetime
from .models import RoomModel, BookRoomModel
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from . import utils
from rest_framework import status
import datetime as dt
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
        query = self.request.query_params.get('search')
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
    

    @action(detail=True, methods=["GET", "POST"])
    def availability(self, request, *args, **kwargs):
        room = self.get_object()
        date = dt.date.today()
        if request.method == 'POST':
            serializer = AvalibilitySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            date = datetime.strptime(serializer.data.get('date'), '%Y-%m-%d').date()
            booked_time_periods = BookRoomModel.objects.filter(
                room_id=room,
                start__date=date
            ).order_by('start')

            
            start_datetime = make_aware(datetime.combine(date, time.min))
            end_datetime = make_aware(datetime.combine(date, time.max))

            not_booked_time_periods = []
            current_datetime = start_datetime

            for booked_period in booked_time_periods:
                period_start = booked_period.start
                period_end = booked_period.end

                if current_datetime < period_start and (period_start-current_datetime)>=timedelta(minutes=2):
                    not_booked_time_periods.append({
                        'start': current_datetime.isoformat(),
                        'end': period_start.isoformat()
                    })

                current_datetime = period_end

            if current_datetime < end_datetime and (end_datetime-current_datetime)>=timedelta(minutes=2):
                not_booked_time_periods.append({
                    'start': current_datetime.isoformat(),
                    'end': end_datetime.isoformat()
                })
            return Response(BookedRoomsSerializer(not_booked_time_periods, many=True).data)

        elif request.method == 'GET':
            booked_time_periods = BookRoomModel.objects.filter(
                room_id=room,
                start__date=date
            ).order_by('start')

            start_datetime = make_aware(datetime.combine(date, time.min))
            end_datetime = make_aware(datetime.combine(date, time.max))

            not_booked_time_periods = []
            current_datetime = start_datetime

            for booked_period in booked_time_periods:
                period_start = booked_period.start
                period_end = booked_period.end

                if current_datetime < period_start and (period_start-current_datetime)>=timedelta(minutes=2):
                    not_booked_time_periods.append({
                        'start': current_datetime.isoformat(),
                        'end': period_start.isoformat()
                    })

                current_datetime = period_end

            if current_datetime < end_datetime and (end_datetime-current_datetime)>=timedelta(minutes=2):
                not_booked_time_periods.append({
                    'start': current_datetime.isoformat(),
                    'end': end_datetime.isoformat()
                })
            return Response(BookedRoomsSerializer(not_booked_time_periods, many=True).data)

# {
#     "resident":{
#         "name":"Elon Musk"
#     },
#     "start":"2023-06-22 16:21:49.219717",
#     "end":"2023-06-22 18:20:49.219717"
# }
