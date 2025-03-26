from django.db import models
from django.utils import timezone


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DataCenter(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'city')

    def __str__(self):
        return f"{self.name} ({self.city})"


class Host(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Maintenance'),
        ('retired', 'Retired'),
    ]

    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(unique=True)
    data_center = models.ForeignKey(DataCenter, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"


class HostPingLog(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    is_reachable = models.BooleanField()
    response_time = models.FloatField(null=True, blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.host} - {'Reachable' if self.is_reachable else 'Unreachable'}"


class DailyHostStats(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    data_center = models.ForeignKey(DataCenter, on_delete=models.CASCADE)
    host_count = models.IntegerField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('city', 'data_center', 'date')

    def __str__(self):
        return f"{self.city} - {self.data_center}: {self.host_count} hosts on {self.date}"