#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : yinchengping
# @Time     : 2022/10/14 16:52
# @File     : constant.py
# @Project  : src
# @Function : xxx
from enum import Enum


class CommStatus(Enum):
    OK = "0"  # 正常
    DELETE = "1"  # 停用
    STOP = "2"  # 删除


class RoleEnum(Enum):
    """"""
    user = '0'  # 客户
    SupAdmin = "2"  # 超级管理员
    robot = "1"  # 企业管理员


class Grade(Enum):
    """"""
    vip1 = '1'  # GPT4
    vip2 = "2"  # GPT3.5
    vip3 = "3"  # WZAI


class MessageType(Enum):
    """消息类型"""
    Sys = "0"  # AI消息
    Srv = "1"  # 客户消息（业务消息）


class MessageSource(Enum):
    """消息业务"""
    DocumentDialogue = "103"  # 文档问答
    Comm = "105"  # 通用


class OrderStatus(Enum):
    """"""
    Pending = '0'  # 待支付
    Finish = '1'  # 已完成 (订单完成状态)
    Cancel = '2'  # 已取消
    Delete = '3'  # 删除


class ServiceLogStatus(Enum):
    """"""
    Pending = '0'  # 待处理(未支付)
    Use = '1'  # 使用中
    Delete = '2'  # 已删除


class PayOrderStatus(Enum):
    """"""
    Pending = '0'  # 待处理（支付中）
    Finish = '1'  # 已支付
    Refunding = '2'  # 退款中
    Refund = '3'  # 已退款
    Cancel = '4'  # 已取消


class GptModel(Enum):
    """"""
    XingHuo = 1
    MoonShot = 2
    DeepSeek = 3
    MiniMaxAi = 4


