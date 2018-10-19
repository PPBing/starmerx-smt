#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import redis
from multiprocessing.pool import ThreadPool as Pool
import sys
sys.path.append("..")
from conf import config
import time
import random
import requests
from api.api_request import ApiRequest
import logging
logging.basicConfig(level=logging.CRITICAL, filename='parseshop.log', filemode='a')

headers = {
        'authority': 'www.aliexpress.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control':'max-age=0',
        'cookie':'ali_apache_id=10.181.239.20.1532396629311.095168.6; cna=WWvTEzvP3wMCAXFmpJ5HeKGe; _ga=GA1.2.1277524822.1532396638; _uab_collina=153242135258565595162801; aep_common_f=HZ1Nz0VL5ytsdjSSZmRfpHyBiKjHMdtPbrUFNxuwbEfo28mSuaKqaQ==; l=AgMDcnzBIPs9NJWvUt-USvDcE8ytSJe6; intl_locale=en_US; __utmc=3375712; __utmz=3375712.1533887475.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=3375712.1277524822.1532396638.1534326024.1534329255.12; _ym_uid=1535532201161954913; _ym_d=1535532201; _hvn_login=13; aep_usuc_t=ber_l=A0; _mle_tmp0=iiCGajxLJhPRfqiVFROq8rCeEFnRQhlsdvq4gChwrvIxqNzmhGDPCIGg7UbWlaZa46XVJwyWjEaRQRsl9D9piE9FbrfXao8dId%2BAH2EwfS34%2FnTAS8UvsnhcUDeX8Y1e; _mle_tmp_harden0=COMyBPKnGxIg1PC5i8Kdr7W2Uhq1Qp3xaepIxbOiZdmSAu%2B0U0Kz5PlI7UdZg%2BK%2B1XP9AlXcvfM38gMqBfc1x1pQJU3lUkE9nuIB0h4rXgDTaPE2ikCTbZxDS%2BzuQGGZ; ali_apache_tracktmp=W_signed=Y; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%0932890383531%0932905173582%0932875359179%0932903961264%0932911623894%0932830254249%0932878620202%0932821420751; _umdata=65F7F3A2F63DF020E9F2D8A14F0A5B57E8450852BDF19B9D203CF091B2CBB3ACE0A0BCE87341EB38CD43AD3E795C914C05A127413ECFAA519859F6A57213D591; _mle_tmp_enc0=Ey%2Fp8LswzxA3J47VsqxI%2B2PXcydc8edA%2BwxDLBlSFGar6RMNWXR7hQqaG9lJ25D%2FT8maTgWl5EGdriODcuAbLQCJNSH%2BtGZ5QBJdaiO04gRXeWxfR%2FUWD5ynbXl3QxOc; _m_h5_tk=de53149a79fec75e290936d69ac9ae47_1535785903027; _m_h5_tk_enc=052488968e1c9b79461d652ed686f90b; _gid=GA1.2.1395472708.1535783474; _gat=1; acs_usuc_t=acs_rt=deccbcb59dbb4cdc9a21f355e3d2d73a&x_csrf=1815eiyw_ew5c; xman_us_t=x_lid=cn13537053iywae&sign=y&x_user=22g32kigrEw4CAu+yqPoUMGL2VYaOtexqUTb5rAuvck=&ctoken=t6yd9_9_jpsp&need_popup=y&l_source=aliexpress; xman_f=xQfvQYGdNY/7PrQ27+uKKDbZkjmrsQ5TOhsd5w7jrqYXROi476Tr+/Qqt1HT/Sb4CUIdLzsqYEzoFs4DETpk/l/HTkFNpFg76h4ETLqqKLw/hQGT9lmRMZG1NnrFwxqPer9acUddqH/HfxJfFdzLxv4Jhi5NDfnHdwVfLqMW5p10JJh/U//uzHdvLe17DytqxRHKsZNyAKXoCP2m+06pwR+WBzIixPcDXqh2bB7cBpnoO7EL4Mg3EYjLmSA3Krti+o4oreITUv57S5gpEt4dDSi7Tjfvrp//mDZ986MTicJHKDvgguK8m6o0nqV/vJ9G+2dDxeb8GFGC+ZyJVYSW1ylatJY0RTp4eRgRl+Mbp+gz8gfPyrh6goWQ+MS9M/kRiwVVqNZf08P0PR206Aq08PEUFe7JaK7T2YgjuCiCc9s=; xman_us_f=zero_order=y&x_locale=en_US&x_l=1&last_popup_time=1533863595311&x_user=CN|huge|bin|ifm|1614960053&no_popup_today=n; aep_usuc_f=site=glo&c_tp=USD&x_alimid=1614960053&isb=y&region=US&b_locale=en_US; intl_common_forever=KMzku24Uc6YbmjbgE690iFnSBKE8IJaTSEJGTt5NgHx5HG9JcQY36g==; JSESSIONID=EE48588A3A92DC74D2B2EC318EED5A9D; isg=BN3d4VHNWva5mT48CtFyD35f7LAXUhKleENNmZ-iAzRjVv2IZ0qzHDaEhAp1likE; ali_apache_track=mt=1|ms=|mid=cn13537053iywae; xman_t=ahtwSxub/uzl2C/OGR4Q8qAbqsOHbkV+43E23kQy+JSPVgU6Osd++VOBjJmkw5x6mbr/4tGquCb53ozGuu73LLCaXUUOIxxsPuBp/j78nfc6W6hX4uM+Q+oxZUjd8wmStStPajIusNbTIuDAXwa7HOtq062r41Nmu3VVQtVLs+8dAGW7XHxx5D4UF7pu/GOLs9/HxIUM47+SYbsIVWqdMAdVvQdUPiCVNZcA3Cv8BdyxG+Sgud4ZZfNAfwNk/E5dMjRNCXdQNzfOwIqP6MvK8Lb61EOv1vaspL6OSkclF6PJXLzZ58TlEpQQBwNVt3As8ynVt/TASlHsCbLK/9WjjKLuoAvYcNj/XMQ9nHVlivu5cpcZOOYhvhfBg76dFXPq1AUc3j3o+WG60GpAg2XM1fMEQFI5DJ0W8KmRMrNOItzvZqodRlK88WJPQLzQz76JLLg9IGcGpqBFj2bFE/JTlIxGdswbKoInYg78T4XvrYTc1nJtSdI+YQwgdEHj/MqeEFn7cl7fj6cEK+c0LR8gXVfFXB2xx3r3E5ssK1EJ+RbjSCwAAxcIRrqhh6R1h/qIYbqOlUWX1gS1MjfXSQTLyqtGR2BFt2clYpZi4zOkgHDHPYrkOfR1DvxKX9JyBGG7',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/68.0.3440.75 Chrome/68.0.3440.75 Safari/537.36'
    }

r = redis.Redis(host="192.168.3.233",port="6379",password="123456")

key = "shopid_next"
# key = "shopid_next"
num = 0

def getres(shopid):
    url =config.shop_url.format(shop_id=shopid)
    use_time = 0
    res = None
    headers["path"] = url.replace('https://www.aliexpress.com', '')
    while True:
        try:
            global num
            if num >= 500:
                time.sleep(10)
                num = 0
            res = requests.get(url, headers=headers)
            num += 1
            break
        except Exception as e:
            time.sleep(random.random() * 2.0 + 0.3)
            logging.critical('<answer_the_url>' + str(e) + '<>' + url)
            print str(e)
            use_time += 1
            if use_time > 10:
                break
            time.sleep(60)
            continue
    return res

def geturl():
    i = 0
    while True:
        shopid = r.spop(key)
        if shopid:
            time.sleep(1)
            res = getres(shopid)
            if res:
                try:
                    soup = BeautifulSoup(res.content,"lxml")
                    item_div = soup.find("div",class_="ui-pagination-navi util-left")
                    item_a = item_div.find_all("a")
                    if item_a:
                        page = int(item_a[-2].get_text()) + 1
                    else:
                        page = 2
                    for x in range(1,page):
                        shop_page_url = config.shop_page_url.format(shop_id=shopid,page=x)
                        r.sadd("shop_page_url",shop_page_url)
                        i+=1
                        print i

                except Exception as e:
                    print str(e),shopid
                    r.sadd("shopid",shopid)
                    # r.sadd("shopid",shopid)
        else:
            break
if __name__=="__main__":
    geturl()