# coding=utf-8
# @name :  bbc.py
# @time :  16/11/13 
# @Author : zhanghan
# @Email : klay.zhanghan@gmail.com

import urllib
import collections
import json
from bs4 import BeautifulSoup



class bbcGoodFood():


    def __init__(self):
        self.colUrlList = []
        self.dishUrlList = []


    # url list for 54 collections
    def colUrlGen(self):

        base_url = 'http://www.bbcgoodfood.com'
        gf_path = '/recipes/category/healthy'

        # url parse process using beautifulSoup
        url = base_url + gf_path
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'lxml')

        # find div section containing url link
        article = soup.find('div', {
            'class': 'row pad-left pad-right content-recipe-categories'}).findAll('article')

        # pasrs html, add url link to list
        for collection in article:
            for i in collection.select('h3 a'):
                self.colUrlList.append(i.attrs['href'])
        return self.colUrlList


    def dishUrlGen(self):
        '''
        Parse and store dish url from each collection stoted in colUrlList
        '''
        print('collect dish url ' + '\n')
        page_id = [0, 1, 2, 3]

        # loop collection link
        for url in self.colUrlList:

            # loop page of each collection
            for page in page_id:
                dishList = []

                # create specific url
                pagePostFix = '?page=' + str(page) + '#c'
                healthy_base = 'http://www.bbcgoodfood.com'
                dish_url = healthy_base + url + pagePostFix

                # dish url parse

                dish_req = urllib.request.Request(dish_url, headers={'User-Agent': 'Mozilla/5.0'})
                dish_html = urllib.request.urlopen(dish_req).read()
                dish_soup = BeautifulSoup(dish_html, 'lxml')
                dish_body = dish_soup.body
                article_content = dish_body.find('div', {'class': 'view-content'})

                # check page validation

                if article_content != None:
                    article_content.findAll('article')

                    # store dish url if page exist

                    for dish in article_content:
                        for i in dish.select('h3 a'):
                            dishList.append(i.attrs['href'])
                self.dishUrlList.extend(dishList)

            # print progress
            print('store dishes from ' + str(url))
        return self.dishUrlList


    def storeDetail(self):
        '''
        Parse each dish url, store details in json format
        '''
        print('start file writing'+'\n')
        base_url = 'http://www.bbcgoodfood.com'
        f = open('goodfood.json', 'w')
        num = 0

        for dishUrl in self.dishUrlList:

            # dish html parse
            req = urllib.request.Request(base_url + dishUrl, headers={'User-Agent': 'Mozilla/5.0'})
            html = urllib.request.urlopen(req).read()
            soup = BeautifulSoup(html, 'lxml')
            body = soup.body

            article = soup.find('ul', {
                'class': 'ingredients-list__group'})

            # name , string
            recipeName = dishUrl.split('/')[-1]

            # ingredients, list of strings
            ingredients = []
            for li in article.findAll('li'):
                ingredients.append(li.text)

            # method, html
            method = soup.find('div', {
                'class': 'method'
            })

            # dict to store infos
            dic = collections.OrderedDict()
            dic['recipe'] = recipeName
            dic['ingredients'] = ingredients
            dic['method'] = str(method)

            # write in json file
            j = json.dumps(dic)
            f.write(j)

            # print progress
            print(str(num) + ':' + 'store dish data, ' + recipeName)
            num += 1
        f.close()




if __name__ == '__main__':

    # Walk through pipeline, get a json file


    ob = bbcGoodFood()
    ob.colUrlGen()
    ob.dishUrlGen()
    ob.storeDetail()
    print('--------Finish----------')


