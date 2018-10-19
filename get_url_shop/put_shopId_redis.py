#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis
import sys
sys.path.append("..")
from conf import config

class PutUrlRedis(object):
    def __init__(self,key,r):
        self.key = key
        self.r = r

    def put_url_redis(self):
        i = 0
        file_name = str(self.key)+".txt"
        with open(config.shop_id_path+file_name,"r") as f:
            lines = f.readlines()
            for line in lines:
                if "productlist.html" not in line:
                    self.r.sadd(self.key,line.strip())
                    i+=1
                    print i
                else:
                    continue
            # for x in range(100):
            #     line = f.readline()
            #     self.r.sadd(self.key,line.strip())
            #     i+=1
            #     print i

if __name__=="__main__":
    r = redis.Redis(host="192.168.3.233",port="6379",password="123456")
    key = "shopid"
    put_redis = PutUrlRedis(key,r)
    put_redis.put_url_redis()
