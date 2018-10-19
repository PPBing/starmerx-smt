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
            "password":setting.config["redis"]["password"]
         }
        redis_pool = redis.ConnectionPool(**redis_config)
        self.r = redis.Redis(connection_pool=redis_pool)

# 根据key 从redis获取值

    def get_value(self, key):
        value = self.r.spop(key)
        return value

# 将链接放入redis中

    def put_value(self,key,url):
        self.r.sadd(key,url)

