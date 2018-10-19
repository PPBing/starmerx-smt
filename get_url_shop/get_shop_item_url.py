#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import redis
from multiprocessing.pool import ThreadPool as Pool
import time
import requests
import random
from multiprocessing import Lock
import sys
sys.path.append("..")
reload(sys)
sys.setdefaultencoding('utf8')
from conf import config
from conf.proxies_pool import ProxiesPool
import datetime
import logging
log_file_name = config.log_path + datetime.date.today().strftime("%Y%m%d") + "shop.log"
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_file_name)
formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class GetShopItemUrl(object):
    def __init__(self,key,r):
        self.key = key
        self.result_file = open(config.shop_url_path  + "shop_url.txt", "a")
        self.r = r
        self.lock = Lock()
        # self.proxies_pool = ProxiesPool()
        # self.proxies = self.proxies_pool.init_proxies()
        self.time_out = 20
        self.num = 0
        self.headers = config.headers

    def answer_the_url(self,url):
        use_time = 0
        # item_h3 = None
        url_list = []
        headers = self.headers
        headers["path"]=url.replace('https://www.aliexpress.com', '')
        while True:
            try:
                if self.num >=500:
                    time.sleep(10)
                    self.num=0
                shop_id = url.split("/")[4] + "_"
                res = requests.get(url,timeout=self.time_out,headers=headers)
                soup = BeautifulSoup(res.content,"lxml")
                item_ul = soup.find("ul", class_="items-list util-clearfix")
                item_h3 = item_ul.find_all("h3")
                for h3 in item_h3:
                    item_a = h3.find("a")
                    item_url = "https:" + str(item_a.get("href")).replace("store/product", "item").replace(shop_id, "")
                    url_list.append(item_url)
                self.num+=1
                break
            except Exception as e:
                time.sleep(random.random() * 2.0 + 0.3)
                use_time += 1
                # if res.status_code == 404:
                #     config.logger.warning("<answer_the_url>" + str(e) + url)
                #     break
                if use_time > 10:
                    print str(e)
                    logger.warning("<answer_the_url>" + str(e) + url)
                    break
                if 'Max retries' in str(e):
                    # new_proxies = self.proxies_pool.get_proxies()
                    # self.proxies = new_proxies
                    continue
                if 'timed out' in str(e):
                    # new_proxies = self.proxies_pool.get_proxies()
                    # self.proxies = new_proxies
                    continue
                if "NoneType" in str(e):
                    # new_proxies = self.proxies_pool.get_proxies()
                    # self.proxies = new_proxies
                    continue
                continue
        return url_list

    def get_url(self):
        while True:
            # url = self.r.spop(self.key)
            # if url:
            #     print url
            #     self.get_url_pool(url)
            # else:
            #     break
            print 100
            lines = []
            for i in range(100):
                url = self.r.spop(self.key)
                if not url:
                    break
                # print url
                lines.append(url)
            if not lines:
                break
            try:
                pool = Pool(10)
                pool.map(self.get_url_pool,lines)
                pool.close()
                pool.join()
            except Exception as e:
                print str(e)
                logger.critical("<answer_the_pool>" + str(e) + str(lines))
                continue
        self.result_file.close()

    def get_url_pool(self,url):
        # item_h3 = self.answer_the_url(url)
        url_list = self.answer_the_url(url)
        # print url
        # shop_id = url.split("/")[4] + "_"
        # print shop_id
        if url_list:
            self.lock.acquire()
            for item_url in url_list:
                self.result_file.write(item_url + "\n")
            # for h3 in item_h3:
            #     item_a = h3.find("a")
            #     item_url = "https:" + str(item_a.get("href")).replace("store/product","item").replace(shop_id,"")
            #     self.result_file.write(item_url + "\n")
            self.result_file.flush()
            self.lock.release()
        else:
            return



if __name__=="__main__":
    r = redis.Redis(host="192.168.3.233",port="6379",password="123456")
    key = "shop_page_url"
    shop_item_url = GetShopItemUrl(key,r)
    shop_item_url.get_url()
