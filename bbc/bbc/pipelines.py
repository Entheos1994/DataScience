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

class ExtractDataPipeline(object):
    def __init__(self):
        self.amount = u'(?P<amount>([0-9]|¼|½|¾|ml|lb|oz|/|x|-|fl|tbsp|tsp|g|kg|or| |small|large|medium|slice|tins?|cloves?|of|\.|cm|in|piece|toasted|frozen|fresh|chopped|pints|heaped|free-range)*)?'
        self.stoplist=[u'\\b-\\b',u'\\b[0-9]+\\b',u'\\bsmall\\b',u'\\blarge\\b',u'\\bmedium\\b',u'\\bslice\\b',u'\\btins\\b',u'\\bcloves\\b',u'\\bof\\b',u'\\bcm\\b',u'\\bin\\b',u'\\bpiece\\b',u'\\btoasted\\b',u'\\bfrozen\\b',u'\\bfresh\\b',u'\\bchopped\\b',u'\\bpints\\b',u'\\bheaped\\b',u'\\bfree-range\\b',u'\\b¼\\b',u'\\b½\\b',u'\\b¾\\b',u'\\bml\\b',u'\\blb\\b',u'\\boz\\b',u'\\b/\\b',u'\\bx\\b',u'\\b-\\b',u'\\bfl\\b',u'\\btbsp\\b',u'\\btsp\\b',u'\\bg\\b',u'\\bkg\\b',u'\\bor\\b',u'\\bplain\\b',u'\\bthin\\b',u'\\bslice\\b','of\\b',u'\\ba\\b',u'\\bfinely\\b',u'\\bleaves\\b',u'\\bfreshly\\b','u\\bthinly\\b',u'\\bhandful\\b',u'\\bdried\\b',u'\\bdrizzle\\b',u'\\bcalorie\\b', u'\\bcontrolled\\b',u'\\bchargrilled\b',u'\\borganic\\b',u'\\bfillet\\b',u'\\bshapes\\b',u'\\bwhole\\b',u'\\blowcalorie\\b',u'\\bsqueeze\\b',u'\\bnew\\b',u'\\bripe\\b',u'\\bpint\\b',u'\\bcooking\\b',u'\\blittle\\b',u'\\byour\\b',u'\\bchoice\\b',u'\\bside\\b']
        self.words_to_remove = re.compile('|'.join(self.stoplist).encode('utf-8'))

    def extract_ingredient(self, ingredient):
        ingredient.encode('utf-8')
        verbose_ingredients = re.match(self.amount+u' (?P<ingredient>[^,(]*)', ingredient).group('ingredient')
        ingr = re.sub(self.words_to_remove,'',verbose_ingredients) # remove all unwanted words
        ingr = re.sub('(\s)+',' ',ingr) # turn multiple whitespaces into one
        ingr = ingr.strip(' ') # remove preceding and trailing whitespaces
        return ingr

    def process_item(self, item, spider):
        url = item['url'] 
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page.read(),"lxml")
        ingredients = soup.find_all("li", {"class": "recipe-ingredients__list-item"})
        acc = []
        for ingredient in ingredients:
            line = u''.join( map( replace, ingredient))
            ingr = self.extract_ingredient(line)
            if ingredient:
                acc.append(ingr)
        item['ingredients'] = acc
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
