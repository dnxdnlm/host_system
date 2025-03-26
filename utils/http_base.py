import json
from enum import Enum
from django.http import HttpResponse


class ReturnCode(Enum):
    OK = 200
    BadRequest = 400
    NotFound = 404
    RequestMethodError = 405
    RequestTimeout = 408
    PreconditionFailed = 412
    ClientTerminate = 499
    InternalError = 500
    NotImplemented = 501
    Failed = 201
    Timeout = 202
    Terminated = 203
    NOK = 204
    NotToken = 205
    TokenTimeOut = 206
    TokenError = 207


CodeMsg = {
    ReturnCode.OK.value: "请求成功",
    ReturnCode.BadRequest.value: "请求错误",
    ReturnCode.NotFound.value: "请求不存在",
    ReturnCode.RequestMethodError.value: "请求方式错误",
    ReturnCode.InternalError.value: "请求异常",
    ReturnCode.Failed.value: "请求失败",
    ReturnCode.Timeout.value: "请求超时",
    ReturnCode.Terminated.value: "请求终止",
    ReturnCode.NotToken.value: "缺少token",
    ReturnCode.TokenTimeOut.value: "token过期",
    ReturnCode.TokenError.value: "token错误",
}


class ResponseHelp(object):

    @classmethod
    def define_result(cls, code=ReturnCode.OK.value, msg="", data=""):
        """"""
        return HttpResponse(json.dumps({"code": code, "msg": msg or CodeMsg[code], "data": data}))


