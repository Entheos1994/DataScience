# coding=utf-8
# @name :  bbc.py
# @time :  16/11/13 
# @Author : zhanghan
# @Email : klay.zhanghan@gmail.com

import urllib
from urllib import request
import collections
import json
from bs4 import BeautifulSoup
from scrapeing import ingredient_Extract
import re
from fuzzywuzzy import process


class bbcGoodFood():
    def __init__(self):
        self.colUrlList = []
        self.dishUrlList = []
        self.resultdict = {}
        self.recipes_list = []
        self.recipes_dict = {}

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
        print('start file writing' + '\n')
        base_url = 'http://www.bbcgoodfood.com'
        f = open('ingred.json', 'r')
        r = f.read()
        ingred_list = json.loads(r)
        f.close()
        num = 0
        for dishUrl in self.dishUrlList:

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
                result = {'name': None, 'qty': None, 'unit': None}
                totaltext = li.text
                if li.find('p'):
                    totaltext = totaltext.replace((li.find('p').text), '')

                if li.find('h2'):
                    totaltext = totaltext.replace((li.find('h2').text), '')

                if totaltext != '':
                    line = totaltext
                    line = re.sub(u"½", u".5", line)
                    line = re.sub(u"¼", u".25", line)

                    numbers = re.search("^[0-9]+", line)
                    unitofmeasure = re.search("ml|g|tbsp|tsp|slices|liters|cm|kg", line)
                    decimal = re.search("^\d*\.\d+", line)
                    needmultiply = re.search(u"^([0-9]+) x ([0-9]+)", line)

                    # ingredient parse to unit, measure, name
                    ingredient = ''
                    fuzzy_match = process.extract(line, ingred_list)
                    best_match_val = fuzzy_match[0][1]
                    candidates = [x for x in fuzzy_match if x[1] == best_match_val]
                    ingredient = max(candidates, key=len)[0]
                    result = {'name': ingredient, 'qty': None, 'unit': None}

                    if decimal:
                        result['qty'] = float(decimal.group())
                    else:
                        if numbers:
                            if needmultiply:
                                result['qty'] = float(needmultiply.group(1)) * float(needmultiply.group(2))
                            else:
                                result['qty'] = float(numbers.group())
                    if unitofmeasure:
                        result['unit'] = unitofmeasure.group()

                    ingredients.append(result)

            acc_distinct_names = set()

            for el in ingredients:
                if el['name'] == '':
                    ingredients.remove(el)
                else:
                    acc_distinct_names.add(el['name'])

            ingredients_detail = str(soup.find("div", {"class": "ingredients-list"}))
            method = str(soup.find("div", {"class": "method"}))


            # recipes information
            dic = collections.OrderedDict()
            dic['name'] = recipeName
            dic['ingredients'] = list(acc_distinct_names)
            dic['url'] = base_url + dishUrl
            dic['quantities'] = ingredients

            dic['list_ingredients'] = ingredients_detail
            dic['method'] = method

            self.recipes_list.append(dic)

            # write in json file




            # print progress
            print(str(num) + ':' + 'store dish data, ' + recipeName)
            num += 1

        self.recipes_dict['Recipes'] = self.recipes_list



        return self.recipes_dict

    def writeToFile(self, reci, fileNameStore):

        new_list = []
        urllist = []
        for item in reci:
            if item['name'] not in urllist:
                new_list.append(item)
                urllist.append(item['name'])

        print('number of recipes to store'+ ':' + len(new_list))
        f = open(fileNameStore, 'w')
        jd = json.dumps(new_list)
        f.write(jd)
        f.close()


if __name__ == '__main__':
    # pipeline, get a json file


    ob = bbcGoodFood()
    ob.colUrlGen()
    ob.dishUrlGen()
    print('ingred_list scrapy')
    ingredient_Extract()

    recipe_list = ob.storeDetail()
    ob.writeToFile(reci=recipe_list, fileNameStore='bbcgoodfood.json')

    print('--------Finish----------')
