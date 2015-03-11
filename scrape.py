from urllib2 import urlopen
from bs4 import BeautifulSoup
import nltk
import sys
import re

def get_recipe(url = 'http://allrecipes.com/Recipe/Healthier-Oven-Roasted-Potatoes/Detail.aspx?evt19=1&referringHubId=84'):
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
            amount = ingredient.find(id = "lblIngAmount").text
        else:
            amount = " "
        ingredients.append({"name": name, "amount": amount})
    recipe["ingredients"] = ingredients
    print recipe
get_recipe()
