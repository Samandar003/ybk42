from django.utils import timezone
from datetime import datetime, time
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def check_availability(start, end, queryset):
    booked = True
    
    parsed_start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
    parsed_end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
    start = timezone.make_aware(parsed_start, timezone.get_default_timezone())
    end = timezone.make_aware(parsed_end, timezone.get_default_timezone())
# 2023-06-07T12:34:56.789Z
# 2023-06-08T12:34:56.789Z

    queryset = queryset.filter(Q(start__range=[start, end]) | Q(end__range=[start, end]))
    if queryset.count()<1:
        booked = False
    return booked


def avaliable(date, queryset):
    start_of_day = time.min
    end_of_day = time.max
    queryset = queryset.filter(Q(start__date=date) | Q(end__date=date))
    # (Q(start__range=[start, end]) | Q(end__range=[start, end]))
    return queryset

    

class CustomPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })

# from rest_framework.response import Response
# from datetime import date, datetime, time

# class NotBookedTimeSlotsView(APIView):
#     serializer_class = TimeSlotSerializer

#     def get(self, request, *args, **kwargs):
#         specific_date = date(2023, 6, 21)  # Replace with your desired date

#         # Retrieve bookings for the specific date
#         booked_slots = Booking.objects.filter(start_time__date=specific_date)

#         # Generate a list of all possible time slots for the specific date
#         start_of_day = datetime.combine(specific_date, time.min)
#         end_of_day = datetime.combine(specific_date, time.max)
#         all_slots = []

#         current_slot = start_of_day
#         while current_slot < end_of_day:
#             next_slot = current_slot + timedelta(minutes=30)
#             all_slots.append((current_slot.time(), next_slot.time()))
#             current_slot = next_slot

#         # Exclude booked time slots from all possible time slots
#         not_booked_slots = [
#             slot for slot in all_slots if not any(
#                 start <= slot[0] < end or start < slot[1] <= end
#                 for start, end in booked_slots.values_list('start_time', 'end_time')
#             )
#         ]

#         # Serialize and return the not booked time slots
#         serializer = self.serializer_class(not_booked_slots, many=True)
#         return Response(serializer.data)
