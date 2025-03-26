#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : yinchengping
# @Time     : 2022/10/18 9:07
# @File     : db_util.py
# @Project  : src
# @Function : xxx
import datetime
import json
import logging
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views import View

from middle.middleware import token_decorator
from utils.constant import CommStatus
from utils.http_base import ResponseHelp


class BaseDBFunc:
    """"""

    def __init__(self, table_obj, is_self_where=False):
        self.table_obj = table_obj
        self.is_self_where = is_self_where

    def insert(self, params):
        """"""
        self.table_obj.objects.create(**params)

    def update(self, query_params, update_params):
        """"""
        self.table_obj.objects.filter(**query_params).update(**update_params)

    def query(self, query_params, query_type="one", order_str="", order_type=""):
        """"""
        if not self.is_self_where:
            query_set = self.table_obj.objects.filter(**query_params)
        else:
            query_set = self.table_obj.objects.filter(self.package_where(query_params))
        if order_str:
            query_set = query_set.order_by(f"{'-' if order_type == 'desc' else ''}{order_str}")
        if query_type == "one":
            return query_set.first()
        elif query_type == "lastOne":
            return query_set.last()
        else:
            return query_set.all()

    def package_where(self, query_params):
        """"""
        q = dict()
        return q

    def query_pagination(self, query_params, page, per_page, order_str="", order_type=""):
        """"""
        if not self.is_self_where:
            query_set = self.table_obj.objects.filter(**query_params)
        else:
            # query_set = self.table_obj.objects.filter(self.package_where(query_params))
            pw = self.package_where(query_params)
            query_set = self.table_obj.objects.filter(pw)
        if order_str:
            query_set = query_set.order_by(f"{'-' if order_type == 'desc' else ''}{order_str}")
        count = query_set.count()
        return Paginator(query_set.all(), int(per_page)).page(int(page)), count

    def count(self, query_params):
        return self.table_obj.objects.filter(**query_params).count()


class BaseModuleFunc:
    """"""

    def __init__(self):
        self.db_func = None

    def format_base_data(self, query_obj):
        """"""
        pass

    def get(self, params):
        """获取一条数据"""
        logging.info(f"BaseModuleFunc get params: {params}")
        obj = self.db_func.query(params)
        return self.format_base_data(obj)

    def get_list(self, params):
        """获取列表数据"""
        logging.info(f"BaseModuleFunc get_list params: {params}")
        params['status'] = CommStatus.OK.value
        obj_list = self.db_func.query(params, query_type="all")
        res = []
        for obj in obj_list:
            res.append(self.format_base_data(obj))
        return res

    def get_list_by_pagination(self, query_params, page=1, per_page=10, order_str='', order_type=''):
        """获取分页列表数据"""
        logging.info(f"BaseModuleFunc get_list_by_pagination params: {query_params}; page: {page}; "
                     f"per_page: {per_page}; order_str: {order_str}; order_type:{order_type}")
        args = dict()
        if order_str:
            args["order_str"] = order_str
        if order_type:
            args["order_type"] = order_type
        obj_list, count = self.db_func.query_pagination(query_params, int(page), int(per_page), **args)
        res = []
        for obj in obj_list:
            res.append(self.format_base_data(obj))
        return {"count": count, "list": res}

    def delete(self, params):
        """删除（实际是修改状态）"""
        logging.info(f"BaseModuleFunc delete params: {params}")
        self.db_func.update(params, {"status": CommStatus.DELETE.value})


class BaseView(View):

    def __init__(self, ):
        super().__init__()
        self.fun_obj = None

    @method_decorator(token_decorator)
    def get(self, request):
        """获取详情"""
        # 小程序get请求，不能通过body上传参数，故作此兼容处理
        params = json.loads(request.body) if request.body else {i: request.GET[i] for i in request.GET}
        data = self.fun_obj.get(params)
        return ResponseHelp.define_result(data=data)

    @method_decorator(token_decorator)
    def post(self, request):
        """新增/编辑"""
        params = json.loads(request.body)
        if params.get("id"):
            self.fun_obj.update(params)
        else:
            self.fun_obj.create(params)
        return ResponseHelp.define_result()

    @method_decorator(token_decorator)
    def delete(self, request):
        """删除"""
        params = json.loads(request.body)
        self.fun_obj.delete(params)
        return ResponseHelp.define_result()

    @method_decorator(token_decorator)
    def put(self, request):
        """获取列表"""
        params = json.loads(request.body)
        res = self.fun_obj.get_list(params)
        return ResponseHelp.define_result(data=res)

    @method_decorator(token_decorator)
    def patch(self, request):
        """获取分页列表"""
        params = json.loads(request.body)

        del_keys = ["page", "per_page", "order_str", "order_type"]
        new_params = dict()
        for key in del_keys:
            if params.get(key):
                new_params[key] = params[key]
                del params[key]
            else:
                new_params[key] = ""
        res = self.fun_obj.get_list_by_pagination(params, new_params["page"], new_params["per_page"],
                                                  new_params["order_str"], new_params["order_type"])
        return ResponseHelp.define_result(data=res)
