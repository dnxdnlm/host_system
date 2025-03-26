import datetime
import logging
from datetime import datetime, date
from django.db.models import Q, Sum
from base.settings import try_get
from HostCenter.models import Host
from utils.common_util import DateTimeEncoder, StringUtil
from utils.constant import CommStatus
from utils.db_util import BaseDBFunc, BaseModuleFunc


class HostDBFunc(BaseDBFunc):
    def query_Host_by_phone_or_Hostname(self, phone_or_Hostname):
        """"""
        return self.table_obj.objects.filter((Q(phone=phone_or_Hostname))
                                             & Q(status__in=[CommStatus.OK.value, CommStatus.DELETE.value])).first()

    def package_where(self, params):
        """"""

        q = Q()
        # 增加robot
        queryset1 = self.table_obj.objects.filter(id=params['uid'])
        if params.get("phone__contains"):
            q &= Q(phone__contains=params["phone__contains"])
            queryset1 = self.table_obj.objects.filter(id=params['uid'], phone__contains=params["phone__contains"]).all()
        if params.get("HostName__contains"):
            q &= Q(HostName__contains=params["HostName__contains"])
            queryset1 = self.table_obj.objects.filter(id=params['uid'],
                                                      HostName__contains=params["HostName__contains"]).all()
        if params.get("status"):
            q &= Q(status=params["status"])
            queryset1 = self.table_obj.objects.filter(id=params['uid'],
                                                      status=params["status"]).all()
        return dict(robot=queryset1, q=q)

    def query_obj_Host_token(self, create_id):
        return self.table_obj.objects.filter(createId=create_id).aggregate(Sum('tokenNum')).get('tokenNum__sum')

    def get_all_token(self):
        return self.table_obj.objects.aggregate(Sum('usedCoin'))['usedCoin__sum']

    def get_today_Host_num(self):
        today = date.today()
        # 获取当前日期的开始时间
        start_time = datetime.combine(today, datetime.min.time())

        # 获取当前日期的结束时间
        end_time = datetime.combine(today, datetime.max.time())
        return self.table_obj.objects.filter(createTime__range=(start_time, end_time)).count()


class HostFunc(BaseModuleFunc):
    def __init__(self, is_self_where=None):
        super().__init__()
        self.db_func = HostDBFunc(Host, is_self_where=is_self_where)

    def format_base_data(self, query_obj):
        res = {
            "id": query_obj.id,
            "ip_address": query_obj.ip_address,

        }
        return res

    def get_obj(self, params):
        """"""
        return self.db_func.query(params)

    def create(self, params):
        """新增一条数据"""
        logging.info(f"HostFunc create params: {params}")
        self.db_func.insert(params)

    def update(self, params):
        logging.info(f"HostFunc update params: {params}")
        id = params["id"]
        del params["id"]
        self.db_func.update({"id": id}, params)

