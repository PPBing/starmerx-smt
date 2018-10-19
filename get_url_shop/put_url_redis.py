#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append("..")
from conf.config import Setting
from dbService.connectRedis import Redis
import os
result_path = os.path.dirname(os.getcwd()) + "/result/"
setting = Setting()
r = Redis()

for root_cate in setting.config["root_cates"]:
    file_name = root_cate.rstrip(".txt")+"_url.txt"
    key = file_name.rstrip(".txt")
    with open(result_path + file_name,"r") as f:
        lines = f.readlines()
        for line in lines:
            r.put_value(key,line.strip())