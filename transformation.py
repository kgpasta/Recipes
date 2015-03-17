# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:50:45 2015

@author: Kaustubh
"""
import ingredients, weights

poultry = ['0500']
sausages = ['0700']
pork = ['1000']
beef = ['1300']
game = ['1700']
meats = poultry + sausages + pork + beef + game
seafood = ['1500']
nonVeg = meats + seafood
veggieSubWords = ["tofu", "seitan", "potatoes", "beet", "cauliflower", "beans", "lentil", "eggplant", "mushrooms", "tempeh"]

def transformVegetarian(recipe, foodTable, weightTable, veggieSubs, stoplist):
    ingredients = recipe["ingredients"]
    recipe["title"] = "Vegetarian " + recipe["title"]
    
    for index,ingredient in enumerate(ingredients):
        if ingredient["foodGroup"] in nonVeg:
            newIngredient = veggieSub(ingredient, veggieSubs, foodTable)
            weights.convertWeight(ingredient, newIngredient, weightTable)
            ingredients[index] = newIngredient
            
    
def veggieSub(ingredient, veggieSubs, foodTable):
    newIngredient = {}
    substitute = ""
    if ingredient["foodGroup"] in poultry:
        substitute = "tofu"
    elif ingredient["foodGroup"] in sausages:
        substitute = "beans"
    elif ingredient["foodGroup"] in pork:
        substitute = "mushrooms"
    elif ingredient["foodGroup"] in game:
        substitute = "mushrooms"
    else:
        substitute = "tempeh"
    
    matchArray = {}
    for veggie in veggieSubs:
        match = ingredients.arrayMatch(substitute, veggie)
        if match[0] > 0:
            matchArray[match[2]] = match[0]
        
    if(len(matchArray) > 0):
        ID = max(matchArray.iterkeys(), key=lambda(x): matchArray[x])
        newIngredient["ID"] = ID
        newIngredient["name"] = foodTable[ID]["description"]
        newIngredient["foodGroup"] = foodTable[ID]["foodGroup"]
    
    return newIngredient
            
def findVeggieSubs(foodTable):
    veggieSubs = []
    for key in foodTable:
        food = foodTable[key]
        if food["foodGroup"] not in nonVeg:
            foodArr = food["description"].lower().replace(",","").split()
            for word in veggieSubWords:
                if(ingredients.matchWord(foodArr[0],word)):
                    veggieSubs.append(food)
                    
    return veggieSubs
        
            