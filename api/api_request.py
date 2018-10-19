#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import time
from multiprocessing import Lock
from conf.config import Setting
import sys
import random
sys.path.append('..')
from log.accessLog import Logger


logger = Logger().logger


class ApiRequest(object):
    def __init__(self):
        setting = Setting()
        self.lock=Lock()
        self.proxies = None
        self.time_out = 20
        self.num = 0
        self.headers = setting.config["headers"]

    def answer_the_url(self,url):
        """
        这个方法是所有方法的入口
        :param url:
        :return:
        """
        #传入url
        #返回结果
        use_time = 0
        res = None
        headers = self.headers
        headers["path"]=url.replace('https://www.aliexpress.com', '')
        while True:
            try:
                if self.num >=500:
                    time.sleep(10)
                    self.num=0
                res = requests.get(url,timeout=self.time_out,headers=headers)
                self.num+=1
                break
            except Exception as e:
                time.sleep(random.random() * 2.0 + 0.3)
                use_time += 1
                if use_time > 10:
                    logger.error("<answer_the_url>" + str(e) + url)
                    break
                time.sleep(60)
                continue
        return res

