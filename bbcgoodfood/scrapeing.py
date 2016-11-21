# !/Users/zhanghan/miniconda2/envs/python3.4/bin python
# coding=utf-8
# @name :  scrapeIng.py
# @time :  16/11/20 
# @Author : zhanghan
# @Email : klay.zhanghan@gmail.com


import urllib
from urllib import request
import json
from bs4 import BeautifulSoup


def ingredient_Extract():
    base_url = 'http://www.bbc.co.uk/'
    ingre_url = 'food/ingredients/by/letter/'

    letter = ('q w e r t y u i o p a s d f g h j k l z c v b n m').split(' ')
    ingred_list = []
    for char in letter:
        html_url = base_url + ingre_url + char

        req = urllib.request.Request(html_url, headers ={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'lxml')

        ol = soup.find('ol', {
            'class': 'resources-by-letter'}).findAll('li')
        a = ol[0].select('a')

    # pasrs html, add url link to list
        for ingred in a:
            tex = (ingred.text).strip()
            if 'Related' not in str(tex):
                ingred_list.append((tex))
        print ('store ingredients of '+ str(char))

    f = open('ingred.json', 'w')
    f.write(json.dumps(ingred_list))
    f.close()

