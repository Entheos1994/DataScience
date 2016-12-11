# !/Users/zhanghan/miniconda2/envs/python3.4/bin python
# coding=utf-8
# @name :  pic_store.py
# @time :  16/12/10 
# @Author : zhanghan
# @Email : klay.zhanghan@gmail.com

import requests
import urllib
from urllib import request
from pymongo import MongoClient

from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)
db=client.test
bbc = db.bbcgoodfood





# bbcgoodfood picture

def pic_store_goodfood(client_col):
    goodfood_url = {}
    for recipe in client_col.find():
        goodfood_url[recipe['name']] = recipe['url']

    picture_url = {}
    for item in goodfood_url.keys():
        dish_req = urllib.request.Request(goodfood_url[item], headers={             'User-Agent': 'Mozilla/5.0'})
        dish_html = urllib.request.urlopen(dish_req).read()
        dish_soup = BeautifulSoup(dish_html, 'lxml')
        dish_body = dish_soup.body
        article_content = dish_body.find('div', {'class':                           'recipe-header__media'})

        pic = article_content.findAll('img')[0].get('src')
        picture_url[item] = pic
        print('url collection: '+ item)

    for item in picture_url.keys():
        filename = item +'.jpg'
        req = requests.get(url=picture_url[item], headers={'User-Agent':                'Mozilla/5.0'})

        f = open(filename, 'wb')
        f.write(req.content)
        f.close()
        print('store the pic'+filename)



# bbchealhy picture
client2 = MongoClient('localhost', 27017)
db2=client2.test
bbc2 = db2.bbchealthy

def pic_store_healthy(client_col):
    healthy_url = {}
    for recipe in client_col.find():
        healthy_url[recipe['name']] = recipe['url']

    picture_url = {}
    for item in healthy_url.keys():
        try:
            dish_req = urllib.request.Request(healthy_url[item], headers={
                'User-Agent': 'Mozilla/5.0'})
            dish_html = urllib.request.urlopen(dish_req).read()
            dish_soup = BeautifulSoup(dish_html, 'lxml')
            dish_body = dish_soup.body
            article_content = dish_body.find('div', {'class': 'recipe-media'})
            pic = article_content.findAll('img')[0].get('src')
            picture_url[item] = pic
            print('url collection: '+ item)
        except:
            continue

    for item in picture_url.keys():
        try:
            filename = item +'.jpg'
            req = requests.get(url=picture_url[item], headers={'User-Agent':                'Mozilla/5.0'})

            f = open(filename, 'wb')
            f.write(req.content)
            f.close()
            print('store the pic'+filename)
        except:
            continue


if __name__ == '__main__':
    pic_store_goodfood(bbc)
    pic_store_healthy(bbc2)
