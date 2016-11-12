from bs4 import BeautifulSoup, NavigableString
import urllib2
import re

def replace(c):
    if not isinstance(c,NavigableString):
        if c.has_attr('href'):
            return c.contents[0]
        #insert DROPITEM
    return c

url = 'http://www.bbc.co.uk/food/recipes/black_bean_and_smoke_29105'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read(),"lxml")

# EXTRACT INGREDIENTS
ingredients = soup.find_all("li", {"class": "recipe-ingredients__list-item"})
res = ''.join(map(replace, ingredients[0]))
print res

# EXTRACT METHOD
meth = soup.find_all("p", {"class": "recipe-method__list-item-text"})
method = {}
counter = 0
for step in meth:
    method[ str(counter) ] = step.text
    counter += 1
print method
