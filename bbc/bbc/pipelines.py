# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.conf import settings
from scrapy import log

from bs4 import BeautifulSoup, NavigableString
import urllib2
from fuzzywuzzy import process
import re

def replace(c):
        if not isinstance(c,NavigableString):
            if c.has_attr('href'):
                return c.contents[0]
            raise DropItem("Unexpeted tag")
        return c

class ExtractDataPipeline(object):
    with open('ingredients.txt') as f:
        ingredients_list = f.readlines()
        ingredients_list = map(str.strip,ingredients_list)
        ingredients_list = map(lambda x : x.decode("utf-8"), ingredients_list)

    def extract_ingredient(self, line):
        print "Line: "+line[:15]
        ingredient = ''
        fuzzy_match = process.extract(line, self.ingredients_list)
        best_match_val = fuzzy_match[0][1]
        candidates = [ x for x in fuzzy_match if x[1] == best_match_val ]
        ingredient = max( candidates, key=len )[0]
        result = {'name' : ingredient , 'qty' : None , 'unit' : None }
        line = line.decode('utf-8')
        line = re.sub(u"½", u".5", line)
        line = re.sub(u"¼", u".25", line)
        line = line.encode('utf-8')
        line = line[:15]
        numbers = re.search("^[0-9]+", line)
        unitofmeasure = re.search("ml|g|tbsp|tsp|slices|liters|cm|kg", line)
        decimal = re.search("^\d*\.\d+", line)
        needmultiply = re.search(u"^([0-9]+) x ([0-9]+)",line)
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
        return result;

    def process_item(self, item, spider):
        url = item['url']
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read(),"lxml")
        ingredients = soup.find_all("li", {"class": "recipe-ingredients__list-item"})
        acc_ingrendients = []
        acc_distinct_names = set()

        for ingredient in ingredients:
            if ingredient: # check that the ingredient is not empty
                line = u''.join( map( replace, ingredient)).lower().strip().encode("utf-8") # turn the list of elements into a string while removing href tags
                ingr = self.extract_ingredient(line)
                acc_ingrendients.append(ingr)
        for el in acc_ingrendients:
            if el['name'] == '':
                acc_ingrendients.remove(el)
            else:
                acc_distinct_names.add(el['name'])

        item['ingredients'] = list(acc_distinct_names)
        item['quantities'] = acc_ingrendients
        list_ingredients = str(soup.find("div",{"class":"recipe-ingredients"}))
        item['list_ingredients'] = list_ingredients
        method = str(soup.find("ol",{"class" : "recipe-method__list"}))
        item['method'] = method
        return item

class MongoDBPipeline(object):

    def __init__(self):
        self.client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = self.client[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        valid = True
        # TODO IMPLEMENT VALIDATION
        # for data in item:
        #     if not data:
        #         valid = False
        #         raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Recipe "+item['name']+" added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
