# !/Users/zhanghan/miniconda2/envs/python3.4/bin python
# coding=utf-8
# @name :  recipe-ingred.py
# @time :  16/12/9
# @Author : zhanghan
# @Email : klay.zhanghan@gmail.com

import json
import os

from fuzzywuzzy import process
from collections import Counter
from pymongo import MongoClient



# database
client = MongoClient('localhost', 27017)
db=client.test
bbc = db.bbc

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DIRECTORY = os.path.join(APP_ROOT)

recipe_list = json.load(open(DIRECTORY + '\\recipe_name.json','r'))
probability = json.load(open(DIRECTORY + '\\probability_update.json', 'r'))
ingred_count = json.load(open(DIRECTORY + '\\ingred_count.json', 'r'))
#ingred_count = json.load(open('ingred_count.json', 'r'))

#weight = json.load(open('cuisine/ingred_weight.json','r'))


def cuisine_relate(enter_recipe, recipe_list=recipe_list, probability=probability, filter=filter, bbc=bbc):

    # check input

    if type(enter_recipe) != str:
        print(type(enter_recipe))
        return ('Not an earth food')

    format_enter = (str(enter_recipe)).lower()
    fuzzy_match = process.extract(format_enter, recipe_list)

    match_recipe = []
    for i in fuzzy_match:
        match_recipe.append(i[0])



    recipe_ingred = {}

    for recipe in match_recipe:
        recipe_ingred[recipe] = bbc.find_one({'name':recipe})['ingredients']

    ## remove common ingreds


    # cuisine prob add up
    total_init = Counter()
    for recipe in recipe_ingred:
        for ingred in recipe_ingred[recipe]:
            a = probability.get(ingred)
            total_init = total_init + Counter(a)

    # Sort results and output json
    result = [{'cuisine': key, 'value': value} for key, value in total_init.items()]
    result = sorted(result, key=lambda d:d['value'], reverse=True)

    return json.dumps(result)



