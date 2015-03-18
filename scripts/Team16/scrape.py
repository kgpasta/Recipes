from urllib2 import urlopen
import urllib2
from bs4 import BeautifulSoup
import nltk
import sys
import re


def get_recipe(url = 'http://allrecipes.com/Recipe/Easy-Garlic-Broiled-Chicken/'):

    if len(sys.argv) > 1:
        url = sys.argv[1]


    wiki = "http://en.wikipedia.org/wiki/List_of_food_preparation_utensils"
    header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
    req = urllib2.Request(wiki,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)
     
    
    cooking_tools = [] 
    table = soup.find("table", { "class" : "wikitable plainrowheaders" })
    for row in table.findAll("tr"):
        cells = row.findAll("th")
        cooking_tools.append(str(cells[0].findAll(text=True)[0]).lower())

    #print cooking_tools

    # wiki = "http://en.wikipedia.org/wiki/List_of_cooking_techniques"
    # header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
    # req = urllib2.Request(wiki,headers=header)
    # page = urllib2.urlopen(req)
    # soup = BeautifulSoup(page)
     
    
    # cooking_methods = [] 
    # links = soup.find_all('a')
    # for link in links:
    #     cooking_methods.append((link.text).encode('utf-8').lower())
    #print cooking_methods
    # for row in table.findAll("tr"):
    #     cells = row.findAll("th")
    #     cooking_tools.append(str(cells[0].findAll(text=True)[0]).lower())

    #cooking_tools = ['spoon', 'cup', 'bowl', 'cutting board', 'knife', 'peeler', 'colander', 'strainer', 'grater', 'can opener', 'saucepan', 'frying pan', 'pan', 'baking dish', 'blender', 'spatula', 'tongs', 'garlic press', 'ladle', 'ricer', 'pot holder', 'rolling pin', 'scissors', 'whisk', 'skillet', 'wok', 'baking sheet', 'casserole dish', 'pot', 'slow cooker']
    cooking_methods = ['peel', 'grate', 'cut', 'slice', 'simmer', 'pour', 'chop', 'blend', 'brown', 'carmelise', 'beat', 'dice', 'melt', 'poach', 'toss', 'roast', 'broil', 'roast', 'grill', 'sieve', 'knead', 'break', 'boil', 'crack', 'fry', 'scramble', 'stir', 'add', 'bake', 'saute',]
    primary_cooking_methods = ["bake", "fry", "broil", "roast", "grill"]

    recipe_page = urlopen(url)
    recipe = {}

    soup = BeautifulSoup(recipe_page.read())
    recipe["title"] = str(soup.find(id="itemTitle").string)
    recipe["servings"] = str(soup.find(id="lblYield").string)
    # recipe["time"] = soup.find(class_="emp-orange").string 
    # recipe["time"]
    recipe["time"] = re.sub(' +', ' ', soup.find_all(class_="time")[0].text.encode('utf-8'))
    #print recipe["time"]

    ingredients_span = soup.find_all(itemprop="ingredients")
    ingredients = []
    for ingredient in ingredients_span:
        if (ingredient.find(id="lblIngName").text is not None):
            name = ingredient.find(id="lblIngName").text
            preparation = re.findall('(?:[A-z]*ed)', name)
            prepdescription = re.findall('(?:[A-z]*ly)', name)
            
        else:
            name = " "
        if (ingredient.find(id="lblIngAmount") is not None):
            amountMeasure = ingredient.find(id="lblIngAmount").text.split(" ")
            amount = amountMeasure[0]
            if len(amountMeasure) == 2:
                measurement = amountMeasure[1]
            else:
                measurement = "piece"
        else:
            amount = " "
            measurement = " "
        ingredients.append({"name": (name), "quantity": str(amount), "measurement": str(measurement), "preparation" : (preparation), "prep-description": (prepdescription), "descriptor": ""})

    recipe["ingredients"] = ingredients

    directions_div = soup.find(class_ = 'directions')
    directions = directions_div.find_all('li')
    steps_string = ''

    for step in directions:
        steps_string += (' ' + step.span.text)

    recipe["cooking tools"] = []   
    recipe["cooking methods"] = []

    for tool in cooking_tools:   
        if tool in steps_string:
            recipe["cooking tools"].append(tool)

    for method in cooking_methods:
        if method in steps_string:
            recipe["cooking methods"].append(method)
    

    recipe["primary cooking method"] = "Combined"       
    for method in recipe["cooking methods"]:
        if method in primary_cooking_methods:
            recipe["primary cooking method"] = method




    #print recipe["tools"]
    #print recipe["methods"]
    #print recipe

    return recipe
#get_recipe()
