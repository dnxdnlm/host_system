from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import subprocess
import platform
from .models import City, DataCenter, Host, HostPingLog, DailyHostStats
from .serializers import (
    CitySerializer,
    DataCenterSerializer,
    HostSerializer,
    HostPingLogSerializer,
    DailyHostStatsSerializer
)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class DataCenterViewSet(viewsets.ModelViewSet):
    queryset = DataCenter.objects.all()
    serializer_class = DataCenterSerializer


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer

    @action(detail=True, methods=['get'])
    def ping(self, request, pk=None):
        host = self.get_object()
        ip_address = host.ip_address

        # 根据操作系统选择ping命令
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', ip_address]

        try:
            output = subprocess.run(command, stdout=subprocess.PIPE, timeout=2)
            is_reachable = output.returncode == 0
            response_time = None

            # 尝试提取响应时间 (仅适用于Linux/Mac)
            if is_reachable and platform.system().lower() != 'windows':
                time_line = [line for line in output.stdout.decode().split('\n')
                             if 'time=' in line][0]
                response_time = float(time_line.split('time=')[1].split(' ')[0])

            # 记录ping结果
            HostPingLog.objects.create(
                host=host,
                is_reachable=is_reachable,
                response_time=response_time
            )

            return Response({
                'host': host.name,
                'ip_address': ip_address,
                'is_reachable': is_reachable,
                'response_time': response_time
            })

        except subprocess.TimeoutExpired:
            HostPingLog.objects.create(
                host=host,
                is_reachable=False,
                response_time=None
            )
            return Response({
                'host': host.name,
                'ip_address': ip_address,
                'is_reachable': False,
                'response_time': None
            }, status=status.HTTP_408_REQUEST_TIMEOUT)


class HostPingLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HostPingLogSerializer

    def get_queryset(self):
        host_id = self.request.query_params.get('host_id')
        if host_id:
            return HostPingLog.objects.filter(host_id=host_id).order_by('-checked_at')
        return HostPingLog.objects.all().order_by('-checked_at')


class DailyHostStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyHostStats.objects.all().order_by('-date')
    serializer_class = DailyHostStatsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        city_id = self.request.query_params.get('city_id')
        data_center_id = self.request.query_params.get('data_center_id')

        if city_id:
            queryset = queryset.filter(city_id=city_id)
        if data_center_id:
            queryset = queryset.filter(data_center_id=data_center_id)

        return queryset