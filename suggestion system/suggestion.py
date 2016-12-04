import pymongo
from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
db=client.test
def get_recipe(recipe_name,recipe_number):
    bbc_food = db.bbc.find_one({'name':recipe_name}) # find the document of the recipe
    ingre = bbc_food.get('ingredients') #obtain the ingredients of the recipe
    Rank=db.Rank.find_one()

    I1 = { key:Rank[key] for key in Rank.keys() & ingre} #filt the ingredient that does not include the recipe

    I2 = sorted(I1.items(), key=lambda d: d[1], reverse = True) #order the ingredient as rank

    ing =[]
    for k, v in I2:
        ing.append(k) #transform the type of ingredient to list
    print(ing)
    a=ing[0]
    hrecipe1 = db.bbcHealthy.find({'ingredients':{"$regex": ing[0], "$options": "i"}}) #query the recipes that include the first ingredient

    Hrecipe1 = []
    Hrecipe2 = []
    for i in hrecipe1:
        Hrecipe1.append(i['name'])   #tranform the type of receipe to list
    print(len(Hrecipe1))



    for num in range(1,len(ing)):
        if len(Hrecipe1)>=recipe_number:

            for x in db.bbcHealthy.find({'ingredients':{"$regex": ing[num], "$options": "i"}}):
                Hrecipe2.append(x['name'])

            set1=set(Hrecipe1)
            set2=set(Hrecipe2)
            Hrecipe1 = (list(set1 & set2))
            #select the recipe whcih have the same name betweent the two group

            print(len(Hrecipe1))
            del Hrecipe2[:] #clear the list
        else:
            break
    return print(Hrecipe1)



get_recipe('Lime and chipotle black bean tacos',9) #test

