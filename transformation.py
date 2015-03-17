# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:50:45 2015

@author: Kaustubh
"""
import ingredients, weights

dairyAndEgg = ['0100']
fats = ['0400']
poultry = ['0500']
sausages = ['0700']
pork = ['1000']
beef = ['1300']
game = ['1700']
meats = poultry + sausages + pork + beef + game
seafood = ['1500']
nonVeg = meats + seafood
nonVegan = nonVeg + dairyAndEgg + fats
veggieSubWords = ["tofu", "potatoes", "beans", "lentil", "eggplant", "mushrooms", "tempeh", "tap water"]
veganSubWords = ["tofu", "tempeh", "beans", "lentil", "eggplant", "mushrooms", "soymilk", "margarine-like", "maple syrup", "tap water"]

def transformVegetarian(recipe, foodTable, weightTable, stoplist):
    ingredients = recipe["ingredients"]
    recipe["title"] = "Vegetarian " + recipe["title"]
    
    for index,ingredient in enumerate(ingredients):
        if ingredient["foodGroup"] in nonVeg or ingredient["name"].find("broth") > -1:
            newIngredient = veggieSub(ingredient, foodTable)
            weights.convertWeight(ingredient, newIngredient, weightTable)
            ingredients[index] = newIngredient
            
    
def veggieSub(ingredient, foodTable):
    veggieSubs = findSubs(foodTable, nonVeg, veggieSubWords)
    substitute = ""
    if ingredient["foodGroup"] in poultry:
        substitute = "tofu"
    elif ingredient["foodGroup"] in sausages:
        substitute = "beans"
    elif ingredient["foodGroup"] in pork:
        substitute = "potatoes"
    elif ingredient["foodGroup"] in beef:
        substitute = "lentils"
    elif ingredient["foodGroup"] in game:
        substitute = "mushrooms"
    elif ingredient["foodGroup"] in seafood:
        substitute = "tempeh"
    else:
        substitute = "tap water"
    
    return createSubstitute(substitute, veggieSubs, foodTable)
    
def transformVegan(recipe, foodTable, weightTable, stoplist):
    ingredients = recipe["ingredients"]
    recipe["title"] = "Vegan " + recipe["title"]
    
    for index,ingredient in enumerate(ingredients):
        if ingredient["foodGroup"] in nonVegan or ingredient["name"].find("honey") > -1 or ingredient["name"].find("broth") > -1:
            newIngredient = veganSub(ingredient, foodTable)
            weights.convertWeight(ingredient, newIngredient, weightTable)
            ingredients[index] = newIngredient
            
def veganSub(ingredient,foodTable):
    veganSubs = findSubs(foodTable, nonVegan, veganSubWords)
    substitute = ""
    if ingredient["foodGroup"] in poultry:
        substitute = "tofu"
    elif ingredient["foodGroup"] in sausages:
        substitute = "beans"
    elif ingredient["foodGroup"] in pork:
        substitute = "potatoes"
    elif ingredient["foodGroup"] in beef:
        substitute = "lentils"
    elif ingredient["foodGroup"] in game:
        substitute = "mushrooms"
    elif ingredient["foodGroup"] in dairyAndEgg:
        if ingredient["name"].find("egg") > -1:
            substitute = "tofu"
        elif ingredient["name"].find("yogurt") > -1:
            substitute = "soy yogurt"
        else:
            substitute = "soymilk"
    elif ingredient["foodGroup"] in fats:
        substitute = "margarine-like"
    else:
        if ingredient["name"].find("honey") > -1:
            substitute = "maple syrup"
        else: 
            substitute = "tap water"
    
    return createSubstitute(substitute, veganSubs, foodTable)
            
def findSubs(foodTable,restrictions, subList):
    subs = []
    for key in foodTable:
        food = foodTable[key]
        if food["foodGroup"] not in restrictions:
            for word in subList:
                match = ingredients.arrayMatch(word,food)
                if match[0] > 2:
                    subs.append(food)
                    
    return subs
        
def createSubstitute(substitute, substituteList, foodTable):
    newIngredient = {}
    matchArray = {}
    for sub in substituteList:
        match = ingredients.arrayMatch(substitute, sub)
        if match[0] > 0:
            matchArray[match[2]] = match[0]
        
    if(len(matchArray) > 0):
        ID = max(matchArray.iterkeys(), key=lambda(x): matchArray[x])
        newIngredient["ID"] = ID
        newIngredient["name"] = foodTable[ID]["description"]
        newIngredient["foodGroup"] = foodTable[ID]["foodGroup"]
    else:
        newIngredient["name"] = substitute
        
    return newIngredient
            