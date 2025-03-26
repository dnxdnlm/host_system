#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : yinchengping
# @Time     : 2022/10/14 13:13
# @File     : token_util.py
# @Project  : src
# @Function : xxx
import base64
from itsdangerous import URLSafeTimedSerializer as utsr


class TokenUtil:

    def __init__(self, security_key="hcrm"):
        self.serializer = utsr(security_key)
        # 将非ASCILL码字符转化为ASCILL码字符，salt是用来做加密的随机字符串
        self.salt = base64.encodebytes(security_key.encode('utf8'))

    def generate_validate_token(self, uid):
        """生成一个Token, dumps产生一个字符串"""
        return self.serializer.dumps(uid, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        """# 验证  （解密）"""
        # max_age是过期时间，loads是做序列化的
        return self.serializer.loads(token, salt=self.salt, max_age=expiration)

    def remove_validate_token(self, token):
        """过期之后将token移除"""
        return self.serializer.loads(token, salt=self.salt)

    def get_token_uid(self, token):
        """"""
        return self.serializer.loads(token, salt=self.salt)
