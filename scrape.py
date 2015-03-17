from urllib2 import urlopen
from bs4 import BeautifulSoup
import nltk
import sys
import re

def get_recipe(url = 'http://allrecipes.com/Recipe/Curried-Honey-Mustard-Chicken/Detail.aspx?soid=recs_recipe_5'):
    if len(sys.argv) > 1:
        url = sys.argv[1]

    recipe_page = urlopen(url)

    recipe = {}

    soup = BeautifulSoup(recipe_page.read())
    recipe["title"] = soup.find(id = "itemTitle").string
    recipe["servings"] = soup.find(id="lblYield").string
    recipe["time"] = re.sub(' +', ' ', soup.find_all(class_ = "time")[0].text)

    #print soup.findAll(itemprop = "ingredients")
    ingredients_span = soup.findAll(itemprop = "ingredients")
    ingredients = []
    for ingredient in ingredients_span:
        if (ingredient.find(id = "lblIngName").text is not None):
            name = ingredient.find(id = "lblIngName").text
        else:
            name = " "
        if (ingredient.find(id = "lblIngAmount") is not None):
            amountMeasure = ingredient.find(id = "lblIngAmount").text.split(" ")
            amount = amountMeasure[0]
            if len(amountMeasure) == 2:
                measurement = amountMeasure[1]
            else:
                measurement = "piece"
        else:
            amount = " "
            measurement = " "
        ingredients.append({"name": name, "amount": amount, "measurement": measurement})
    recipe["ingredients"] = ingredients
    #print recipe
    return recipe
get_recipe()
