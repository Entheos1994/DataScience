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

import re

def replace(c):
        if not isinstance(c,NavigableString):
            if c.has_attr('href'):
                return c.contents[0]
            raise DropItem("Unexpeted tag")
        return c

#         self.amount = u'(?P<amount>([0-9]|¼|½|¾|ml|lb|oz|/|x|-|fl|tbsp|tsp|g|kg|or| |small|large|medium|slice|tins?|cloves?|of|\.|cm|in|piece|toasted|frozen|fresh|chopped|pints|heaped|free-range)*)?'
#         self.stoplist=[u'\\b-\\b',u'\\b[0-9]+\\b',u'\\bsmall\\b',u'\\blarge\\b',u'\\bmedium\\b',u'\\bslice\\b',u'\\btins\\b',u'\\bcloves\\b',u'\\bof\\b',u'\\bcm\\b',u'\\bin\\b',u'\\bpiece\\b',u'\\btoasted\\b',u'\\bfrozen\\b',u'\\bfresh\\b',u'\\bchopped\\b',u'\\bpints\\b',u'\\bheaped\\b',u'\\bfree-range\\b',u'\\b¼\\b',u'\\b½\\b',u'\\b¾\\b',u'\\bml\\b',u'\\blb\\b',u'\\boz\\b',u'\\b/\\b',u'\\bx\\b',u'\\b-\\b',u'\\bfl\\b',u'\\btbsp\\b',u'\\btsp\\b',u'\\bg\\b',u'\\bkg\\b',u'\\bor\\b',u'\\bplain\\b',u'\\bthin\\b',u'\\bslice\\b','of\\b',u'\\ba\\b',u'\\bfinely\\b',u'\\bleaves\\b',u'\\bfreshly\\b','u\\bthinly\\b',u'\\bhandful\\b',u'\\bdried\\b',u'\\bdrizzle\\b',u'\\bcalorie\\b', u'\\bcontrolled\\b',u'\\bchargrilled\b',u'\\borganic\\b',u'\\bfillet\\b',u'\\bshapes\\b',u'\\bwhole\\b',u'\\blowcalorie\\b',u'\\bsqueeze\\b',u'\\bnew\\b',u'\\bripe\\b',u'\\bpint\\b',u'\\bcooking\\b',u'\\blittle\\b',u'\\byour\\b',u'\\bchoice\\b',u'\\bside\\b']

class ExtractDataPipeline(object):
    with open('ingredients.txt') as f:
        ingredients_list = f.readlines()
        ingredients_list = map(str.strip,ingredients_list)

    def extract_ingredient(self, line):
        # print "Line: "+line
        match = ''
        for el in self.ingredients_list: # for every possible ingredient
            if el in line: # check if the ingredient is in that line
                if len(el) > len(match):
                    match = el
        result = {'name' : match , 'qty' : None , 'unit' : None }
        line = line.decode('utf-8')
        line = re.sub(u"½", u".5", line)
        line = re.sub(u"¼", u".25", line)
        line = line.encode('utf-8')
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
