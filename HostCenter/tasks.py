from celery import shared_task
from datetime import date
from .models import City, DataCenter, DailyHostStats


@shared_task
def generate_daily_host_stats():
    today = date.today()

    # 检查是否已经生成了今天的统计数据
    if DailyHostStats.objects.filter(date=today).exists():
        return "Today's stats already generated"

    cities = City.objects.all()

    for city in cities:
        data_centers = DataCenter.objects.filter(city=city)

        for dc in data_centers:
            host_count = Host.objects.filter(data_center=dc).count()

            DailyHostStats.objects.create(
                city=city,
                data_center=dc,
                host_count=host_count,
                date=today
            )

    return f"Daily host stats generated for {today}"