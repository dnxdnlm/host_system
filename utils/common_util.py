#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : yinchengping
# @Time     : 2022/10/17 8:57
# @File     : common_util.py
# @Project  : src
# @Function : xxx
import base64
import datetime
import json
import math
import os
import random
import time
import uuid
from datetime import date
import tiktoken
from base.settings import BASE_DIR


class StringUtil:
    """字符串相关常用方法"""

    @classmethod
    def str_2_base64(cls, s):
        """字符串转base64"""
        return base64.b64encode(s.encode("utf-8"))

    @classmethod
    def make_code(cls, prefix=''):
        """生成订单编号"""
        base_str = str(time.time()).replace('.', '')[:15] + str(random.randint(10000, 99999))
        return (prefix or '') + '{:0<15}'.format(base_str)

    @classmethod
    def make_srv_code(cls, count: int):
        """"""
        code_orig = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTt1234567890"
        promote_code = ""

        for x in range(count):
            promote_code += random.choice(code_orig)
        return promote_code


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)


class DateTimeUtil:
    """日期常用方法"""

    @classmethod
    def get_datetime_by_days(cls, days, type_str="after"):
        """"""
        temp_date = datetime.datetime.now()  # 获取当前时间 年月日时分秒
        if type_str == "after":
            return temp_date + datetime.timedelta(days=days)
        else:
            return temp_date + datetime.timedelta(days=-days)

    @classmethod
    def check_datetime_with_current(cls, s_datetime):
        """"""
        return datetime.datetime.strptime(s_datetime, '%Y-%m-%d %H:%M:%S') > datetime.datetime.now()

    @classmethod
    def get_datestr_by_days(cls, days, type_str="after"):
        """"""
        return str(cls.get_datetime_by_days(days, type_str=type_str))[:10]

    @classmethod
    def get_datetime_by_datestr_with_days(cls, datestr, days, type_str="after"):
        if type_str == "after":
            return datetime.datetime.strptime(datestr, '%Y-%m-%d') + datetime.timedelta(days=days)
        else:
            return datetime.datetime.strptime(datestr, '%Y-%m-%d') + datetime.timedelta(days=-days)

    @classmethod
    def get_datestr_by_datestr_with_days(cls, datestr, days, type_str="after"):
        return str(cls.get_datetime_by_datestr_with_days(datestr, days, type_str=type_str))[:10]

    def add_month(cls, d, md):
        """
        日期按月份累加
        :param d: 日期
        :param md: 相加月数
        :return: 相加月数之后的日期
        """
        month_30 = [2, 4, 6, 9, 11]
        yd = md // 12
        m = d.month + md % 12
        if m != 12:
            yd += m // 12
            m = m % 12
        if d.day == 31 and m in month_30:
            return date(d.year + yd, m, 30)
        return date(d.year + yd, m, d.day)


class BaiDuMapUtil:
    """"""

    @classmethod
    def get_longitude_latitude(cls, area_name):
        """
        根据地区名获取经纬度
        :param area_name:
        :return:
        """
        try:
            import requests
            from base.settings import BAIDU_MAP_URL, BAIDU_OUTPUT
            url = BAIDU_MAP_URL + '/?address=' + area_name + BAIDU_OUTPUT
            response_data = requests.get(url)
            answer = response_data.json()
            return str(answer['result']['location']['lng']), str(answer['result']['location']['lat'])
        except Exception as e:
            return '', ''


class MathUtil:

    @classmethod
    def get_str_rate_has_2_point(cls, data1, data2):
        """"""
        if not (data1 - data2):
            return "0", "0"
        if not data2:
            return "100.00", "0"
        return '%.2f' % (math.fabs(data1 - data2) / data2 * 100), "0" if data1 > data2 else "1"


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


class FileUtil:
    def save_file(self, request, type):
        icon_file = request.FILES.get(type, None)
        if icon_file:
            dir = os.path.join(BASE_DIR, 'media', type)
            if not os.path.exists(dir):
                os.makedirs(dir)
            destination = open(os.path.join(dir, icon_file.name),
                               'wb+')
            for chunk in icon_file.chunks():
                destination.write(chunk)
            destination.close()
            return icon_file.name
        return ''
