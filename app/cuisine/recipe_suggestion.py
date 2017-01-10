# !/Users/zhanghan/miniconda2/envs/python3.4/bin python
# coding=utf-8
# @name :  recipe_suggestion_change.py
# @time :  17/1/10 
# @Author : zhanghan
# @Email : klay.zhanghan@gmail.com
from pymongo import MongoClient
from bson import json_util
import os
import json
from fuzzywuzzy import process
import random

from collections import Counter


client = MongoClient('localhost', 27017)
db=client.test

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DIRECTORY = os.path.join(APP_ROOT)

recipe_list = json.load(open(DIRECTORY + '/'+'recipe_name.json','r'))

def get_recipe(user_input):
    user_input = user_input.lstrip(' ')
    user_input = user_input.rstrip(' ')
    user_input = user_input.capitalize()

    if db.bbc.find_one({'name':user_input}):
        bbc_food = db.bbc.find_one({'name':user_input})
    else:
        recipe = process.extract(user_input, recipe_list)
        possible_recipe = [x[0] for x in recipe]
        random_recipe = random.choice(possible_recipe)
        recipe_name = random_recipe
        bbc_food = db.bbc.find_one({'name':recipe_name})

    print(bbc_food['name'])



    ingre = bbc_food.get('ingredients')
    Rank=db.Rank.find_one()

    I1 = {}

    for ingreds in ingre:
        if ingreds in Rank.keys():
            I1[ingreds] = Rank[ingreds]

    # I1 = { key:Rank[key] for key in Rank.keys() & ingre}
    I2 = sorted(I1.items(), key=lambda d: d[1], reverse = True) #order the ingredient as rank

    ing =[]
    for k, v in I2:
        ing.append(k) #transform the type of ingredient to list
    print(ing) # the ingredient of the recipe

    hrecipe1 = db.bbcHealthy.find({'ingredients':{"$regex": ing[0], "$options": "i"}}) #query the recipes that include the first ingredient

    Hrecipe1 = []
    Hrecipe2 = []
    for i in hrecipe1:
        Hrecipe1.append(i['name'])   #tranform the type of receipe to list



    level_divided = {}
    n = 2
    level = [len(Hrecipe1)]
    for num in range(1,len(ing)):
        if len(Hrecipe1)>=1:

            for x in db.bbcHealthy.find({'ingredients':{"$regex": ing[num], "$options": "i"}}):
                Hrecipe2.append(x['name'])

            set1=set(Hrecipe1)
            set2=set(Hrecipe2)
            Hrecipe1 = (list(set1 & set2))
            level_divided[n]= Hrecipe1
            n = n+1
            #select the recipe whcih have the same name betweent the two group

            level.append(len(Hrecipe1))
            del Hrecipe2[:] #clear the list
        else:
            break


    No_ingre=[]
    # delete the ingre which is the same as different level
    new_divided = {}
    for i in range(2,len(level_divided)+1):
        print(i)
        #print('level:',len(level_divided))
        if len(level_divided[i]) != 1:

            new_divided[i] = list(set(level_divided[i])-set(level_divided[i+1]))
        else:
            new_divided[i] = level_divided[i]




    No_ingre = []
    for key in new_divided:
        No_ingre.append(key)
#



    outputClass = []
    while len(outputClass) < 3:

        recipeNumber = No_ingre.pop(-1)
        recipes = new_divided[recipeNumber]
        if len(recipes) == 0:
            continue
        if len(recipes) >=2:
            Hrecipe_overlap = ing[0:recipeNumber]
            scoreRank = {}
            for recipe in recipes:
                bbc_food = db.bbcHealthy.find_one({"name":recipe})
                ingre1 = bbc_food.get('ingredients')
                Remain_recipe = list((set(ingre1)) - set(Hrecipe_overlap))
                Remain_recipe_withR = {key: Rank[key] for key in Rank.keys() & Remain_recipe}
                sum(Remain_recipe_withR.values())
                scoreRank[recipe] = sum(Remain_recipe_withR.values())
            scoreRank = sorted(scoreRank.items(), key=lambda d:d[1], reverse=True)
            while scoreRank:
                highRank = scoreRank.pop(0)
                outputClass.append((recipeNumber, highRank[0]))
                if len(outputClass) == 3:
                    break

        else:
            if recipes[0] not in [x[1] for x in outputClass]:
                outputClass.append((recipeNumber, recipes[0]))


    ingList = []
    A_class = outputClass.pop(0)
    ingList.append({'A-Class':db.bbcHealthy.find_one({'name': str(A_class[1])})})
    B_class = outputClass.pop(0)
    ingList.append({'B-Class':db.bbcHealthy.find_one({'name': str(B_class[1])})})
    B_class = outputClass.pop(0)
    ingList.append({'B-Class':db.bbcHealthy.find_one({'name': str(B_class[1])})})

    # score_B = sorted(score_B.items(), key=lambda d: d[1], reverse=True)
    #
    # score_B = dict(score_B[0:(3 - level[-2])])
    #
    # # print the result
    # result = {}
    # result['B-Class'] = {"Matching Rate": match_rate_B}
    # result['B-Class'].update(score_B)
    # result['A-Class'] = {"Matching Rate": match_rate_A}
    # result['A-Class'].update(score_A)
    # print(result)
    #
    # ingList = []




    return json_util.dumps(ingList)

