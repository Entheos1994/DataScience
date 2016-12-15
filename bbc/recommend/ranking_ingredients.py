import json

#ranking ingredient using only bbchealthy dataset
def ranked_result_of_ingredient():
    with open('/Users/Blair/Documents/workspace/pycharm/DataScience/datasets/bbcHealthy.json', 'r') as stream:
        healthy_food = json.load(stream)
    # print(healthy_food)
    list = []
    for item in healthy_food:
        list.extend(item['ingredients'])
    print(list)
    d = {}
    for item in list:
        d[item] = list.count(item)
    print(d)
    return d
#ranked_result_of_ingredient()

def write_ranking_result():
    json.dump(ranked_result_of_ingredient(), open('/Users/Blair/Documents/workspace/pycharm/DataScience/datasets/ingredients_ranking_healthybbc.json','w'))

#write_ranking_result()

#ranking ingredient only use goodfood
def ranked_result_of_ingredient_goodfood():
    with open('/Users/Blair/Documents/workspace/pycharm/DataScience/datasets/distinct/bbcgoodfoodnew.json', 'r') as stream:
        good_food = json.load(stream)
    # print(healthy_food)
    list = []
    for item in good_food:
        list.extend(item['ingredients'])
    print(list)
    d = {}
    for item in list:
        d[item] = list.count(item)
    print(d)
    return d
#ranked_result_of_ingredient_goodfood()

def write_ranking_result_goodfood():
    json.dump(ranked_result_of_ingredient_goodfood(), open('/Users/Blair/Documents/workspace/pycharm/DataScience/datasets/ingredients_ranking_bbcgoodfood.json','w'))

#write_ranking_result_goodfood()


#ranking ingredient using both goodfood and healthy food

def ranked_result_of_ingredient_overall():
    with open('datasets/distinct/bbcgoodfoodnew.json', 'r') as stream:
        good_food = json.load(stream)
    # print(healthy_food)
    list = []
    for item in good_food:
        list.extend(item['ingredients'])
    print(list)
    with open('datasets/distinct/bbcHealthydistinct.json', 'r') as stream1:
        healthy_food = json.load(stream1)
        # print(healthy_food)

    for item in healthy_food:
        list.extend(item['ingredients'])
    print(list)
    d = {}
    for item in list:
        d[item] = list.count(item)
    print(d)

    return d


def write_ranking_result_overall():
    json.dump(ranked_result_of_ingredient_goodfood(), open('datasets/ingredients_ranking_overall.json','w'))


#rank both bbcHealthy dataset and bbcgoodfood dataset
ranked_result_of_ingredient_overall()
write_ranking_result_overall()