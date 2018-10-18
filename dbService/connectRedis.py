#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
from conf.config import Setting


class Redis(object):
    def __init__(self):
        setting = Setting()
        redis_config = {
            "host": setting.config["redis"]["host"],
            "port": setting.config["redis"]["port"],
            "password":"123456"
         }
        redis_pool = redis.ConnectionPool(**redis_config)
        self.r = redis.Redis(connection_pool=redis_pool)

# 根据key 从redis获取值

    def get_value(self, key):
        value = self.r.get(key)
        return value

# 在redis中设置key -> value

    def set_key(self, key, value, expire_time=3600*100):
        self.r.set(key, value, expire_time)

