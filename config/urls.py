
from django.contrib import admin
from django.urls import path
from main.views import RoomModelViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('rooms', RoomModelViewSet, basename='rooms')


urlpatterns = [
    path('admin/', admin.site.urls),
] + router.urls

