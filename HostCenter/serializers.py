from rest_framework import serializers
from .models import City, DataCenter, Host, HostPingLog, DailyHostStats


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class DataCenterSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        source='city',
        write_only=True
    )

    class Meta:
        model = DataCenter
        fields = '__all__'


class HostSerializer(serializers.ModelSerializer):
    data_center = DataCenterSerializer(read_only=True)
    data_center_id = serializers.PrimaryKeyRelatedField(
        queryset=DataCenter.objects.all(),
        source='data_center',
        write_only=True
    )

    class Meta:
        model = Host
        fields = '__all__'


class HostPingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostPingLog
        fields = '__all__'


class DailyHostStatsSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    data_center = DataCenterSerializer(read_only=True)

    class Meta:
        model = DailyHostStats
        fields = '__all__'