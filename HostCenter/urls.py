from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CityViewSet,
    DataCenterViewSet,
    HostViewSet,
    HostPingLogViewSet,
    DailyHostStatsViewSet
)

router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='cities-basename')
router.register(r'datacenters', DataCenterViewSet, basename='datacenters-basename')
router.register(r'hosts', HostViewSet, basename='hosts-basename')
router.register(r'ping-logs', HostPingLogViewSet, basename='ping-logs-basename')
router.register(r'daily-stats', DailyHostStatsViewSet, basename='daily-stats-basename')

urlpatterns = [
    path('', include(router.urls)),
]