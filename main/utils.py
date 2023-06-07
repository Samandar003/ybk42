from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def check_availability(start, end, queryset):
    booked = True
    parsed_start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S.%fZ")
    parsed_end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S.%fZ")
    start = timezone.make_aware(parsed_start, timezone.get_default_timezone())
    end = timezone.make_aware(parsed_end, timezone.get_default_timezone())
# 2023-06-07T12:34:56.789Z
# 2023-06-08T12:34:56.789Z

    queryset = queryset.filter(Q(start__range=[start, end]) | Q(end__range=[start, end]))
    if queryset.count()<1:
        booked = False
    return booked


def avaliable(date, queryset):
    queryset = queryset.filter(Q(start__date=date) | Q(end__date=date))
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

