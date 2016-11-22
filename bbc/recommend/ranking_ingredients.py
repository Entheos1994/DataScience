import json


def ranked_result_of_ingredient():
    recipes = []
    for line in open('bbcHealthy.json'):
        recipe = json.loads(line)
        recipes.append(recipe)
    print(recipes)

    list = []
    for item in recipes:
        list.extend(item['ingredients'])
    print(list)
    d = {}
    for item in list:
        d[item] = list.count(item)
    print(d)
    return d


def write_ranking_result():
    json.dump(ranked_result_of_ingredient(), open('ingredients_ranking.json','w'))

write_ranking_result()