#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : yinchengping
# @Time     : 2022/10/13 10:24
# @File     : middleware.py
# @Project  : src
# @Function : 中间处理类
import logging
import time
import traceback

from django.http import HttpResponse

from utils.http_base import ResponseHelp, ReturnCode
from utils.logger import *

from django.utils.deprecation import MiddlewareMixin

from utils.logger import log_error


class ExceptionMiddleware(MiddlewareMixin):
    # 如果注册多个process_exception函数，那么函数的执行顺序与注册的顺序相反。(其他中间件函数与注册顺序一致)
    # 中间件函数，用到哪个就写哪个，不需要写所有的中间件函数。
    # 去setting.py文件MIDDLEWARE数组下增加'middle.middleware.ExceptionMiddleware'才能生效
    @staticmethod
    def process_exception(request, exception):
        """视图函数发生异常时调用"""
        log_error(f"{type(exception)} {exception}")
        try:
            traceback.format_exc(exception)
        except Exception as e:
            logging.error(e)
        if isinstance(exception.args[0], HttpResponse):
            return exception.args[0]
        return ResponseHelp.define_result(code=ReturnCode.InternalError.value, msg=f"{exception}")


class RequestTimeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        return None

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response['X-Request-Duration'] = f"{duration:.2f}s"

            # 也可以记录到日志或数据库中
            print(f"Request to {request.path} took {duration:.2f} seconds")

        return response


def token_decorator(func):
    def wrapper(request, *args, **kwargs):
        Token.check_token(request)
        return func(request, *args, **kwargs)

    return wrapper
