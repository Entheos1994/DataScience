# !/Users/zhanghan/miniconda2/envs/python3.4/bin python
# coding=utf-8
# @name :  recipe-ingred.py
# @time :  16/12/9
# @Author : zhanghan
# @Email : klay.zhanghan@gmail.com

import json
from fuzzywuzzy import process
from collections import Counter
from pymongo import MongoClient



# database
client = MongoClient('localhost', 27017)
db=client.test
bbc = db.bbcfood



recipe_list = json.load(open('cuisine/recipe_name.json','r'))
probability = json.load(open('cuisine/pretty_cuisine.json', 'r'))
ingred_count = json.load(open('cuisine/ingred_count.json', 'r'))
filter = [x[0] for x in ingred_count[:20]]

def cuisine_relate(enter_recipe, recipe_list=recipe_list, probability=probability, filter=filter, bbc=bbc):

    # check input
    if type(enter_recipe) != str:
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
    for x in recipe_ingred:
        if x in filter:
            recipe_ingred.remove(x)


    # cuisine prob add up
    total_init = Counter(None)
    for recipe in recipe_ingred:
        for ingred in recipe_ingred[recipe]:
            a = probability.get(ingred)
            total_init = total_init + Counter(a)
    total = sorted(total_init.items(), key=lambda d: d[1], reverse = True)

    return total






