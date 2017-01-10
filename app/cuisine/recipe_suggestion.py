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




    #bbc_food = db.bbc.find_one({'name':recipe_name}) # find the document of the recipe
    ingre = bbc_food.get('ingredients') #obtain the ingredients of the recipe
    Rank=db.Rank.find_one()

    I1 = { key:Rank[key] for key in Rank.keys() & ingre} #filt the ingredient that does not include the recipe

    I2 = sorted(I1.items(), key=lambda d: d[1], reverse = True) #order the ingredient as rank

    ing =[]
    for k, v in I2:
        ing.append(k) #transform the type of ingredient to list
    print(ing) # the ingredient of the recipe
    a=ing[0]
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
    #  delete the ingre which is the same as different level
    for i in range(2,len(level_divided)):
        print(len(level_divided))
        #list(set(level_divided[i])-set(level_divided[len(level_divided)]))
        level_divided[i] = list(set(level_divided[i])-set(level_divided[len(level_divided)]))
        if level_divided[i] == []:
            del level_divided[i]


    for key in level_divided:
        No_ingre.append(key)
    print(No_ingre)

    #print(level_divided) # the recipe name in each class
    print(level)  #numbrecipe the overlaper of

    No_Hrecipe_overlap = len(level)-1 # the level of overlap

    match_rate_A = No_ingre[-2]/len(ing)
    match_rate_B = No_ingre[-3]/len(ing)
    Hrecipe_overlap = ing[0:No_ingre[-2]-1]
    Hrecipe_overlapB = ing[0:No_ingre[-3] - 1]
    R_name_A = (level_divided[No_ingre[-2]])  #Recipe names in A class
    R_name_B = (level_divided[No_ingre[-3]]) #recipe name in B class

    score_A = {}
    score_B = {}
    score = {}
    if len(R_name_A)>=3:
        for i in R_name_A:

            bbc_food = db.bbcHealthy.find_one({'name': i})  # find the document of the recipe

            ingre1 = bbc_food.get('ingredients')  # obtain the ingredients of the recipe

            Remain_recipe = list((set(ingre1))-set(Hrecipe_overlap)) # the ingredient which do not include the health recipe

            Remain_recipe_withR = {key: Rank[key] for key in Rank.keys() & Remain_recipe}
            sum(Remain_recipe_withR.values())

            score_A[i]= sum(Remain_recipe_withR.values())
        score_A = sorted(score_A.items(), key=lambda d: d[1], reverse=True)
        score_A = dict(score_A[0:3])
        result = {}
        result['A-Class'] = {"Matching Rate":match_rate_A}
        result['A-Class'].update(score_A)
        print(result)
        for key in score_A:
                         print (db.bbcHealthy.find_one({'name':key}))


    else:
        for i in R_name_A:

            bbc_food = db.bbcHealthy.find_one({'name': i})  # find the document of the recipe

            ingre1 = bbc_food.get('ingredients')  # obtain the ingredients of the recipe

            Remain_recipe = list((set(ingre1))-set(Hrecipe_overlap)) # the ingredient which do not include the health recipe

            Remain_recipe_withR = {key: Rank[key] for key in Rank.keys() & Remain_recipe}

            # print(sum(Remain_recipe_withR.values()))

            score_A[i]= sum(Remain_recipe_withR.values())
        score_A = sorted(score_A.items(), key=lambda d: d[1], reverse=True)
        score_A = dict(score_A)



        for i in R_name_B:
            bbc_food = db.bbcHealthy.find_one({'name': i})  # find the document of the recipe

            ingre1 = bbc_food.get('ingredients')  # obtain the ingredients of the recipe

            Remain_recipe = list((set(ingre1)) - set(Hrecipe_overlapB))  # the ingredient which do not include the health recipe
            # print(Remain_recipe)
            Remain_recipe_withR = {key: Rank[key] for key in Rank.keys() & Remain_recipe}
            #print(sum(Remain_recipe_withR.values()))

            score_B[i] = sum(Remain_recipe_withR.values())

        score_B = sorted(score_B.items(), key=lambda d: d[1], reverse=True)

        score_B= dict(score_B[0:(3-level[-2])])

        #print the result
        result = {}
        result['B-Class'] = {"Matching Rate":match_rate_B}
        result['B-Class'].update(score_B)
        result['A-Class'] = {"Matching Rate":match_rate_A}
        result['A-Class'].update(score_A)
        print(result)

        ingList = []

        for key in score_A:
            ingList.append({'A-Class': db.bbcHealthy.find_one({'name': key})})
        for key in score_B:
            ingList.append({'B-Class': db.bbcHealthy.find_one({'name': key})})

        ingList.append(result)
        return json_util.dumps(ingList)