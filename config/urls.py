
from django.contrib import admin
from django.urls import path, include
from main.views import RoomModelViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('rooms', RoomModelViewSet, basename='rooms')

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Ybky42 API",
      default_version='v1',
      description="Swagger Docs for RESTAPI",
      contact=openapi.Contact("Samandar Shoyimov <samandar20527@gmail.com>"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
     path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),

] + router.urls

