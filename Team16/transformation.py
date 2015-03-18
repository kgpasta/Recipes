# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 12:50:45 2015

@author: Kaustubh
"""
import ingredients, weights, copy

dairyAndEgg = ['0100']
spicesAndHerbs = ['0200']
fats = ['0400']
poultry = ['0500']
sauces = ['0600']
sausages = ['0700']
pork = ['1000']
beef = ['1300']
game = ['1700']
seafood = ['1500']
vegetables = ['1100']
grains = ['1800','2000']
meats = poultry + sausages + pork + beef + game
nonVeg = meats + seafood
nonVegan = nonVeg + dairyAndEgg + fats
highCal = sausages + pork + beef + fats + grains + vegetables
highFat = highCal
cuisineFoodGroups = meats + spicesAndHerbs + sauces + grains
veggieSubWords = ["tofu", "potatoes", "beans", "lentil", "eggplant", "mushrooms", "tempeh", "tap water"]
nonVeggieSubWords = ["chicken", "sausage", "pork", "beef", "lamb", "salmon"]
veganSubWords = ["tofu", "potatoes", "tempeh", "beans", "lentil", "eggplant", "mushrooms", "soymilk", "margarine-like", "maple syrup", "tap water"]
nonVeganSubWords = ["chicken", "sausage", "pork", "beef", "lamb", "salmon", "milk", "butter", "honey"]
lowCalSubWords = ["soymilk", "margarine", "margarine-like", "ham", "turkey sausage", "ground turkey", "cauliflower", "tap water"]
lowFatSubWords = ["soymilk", "soy yogurt", "margarine", "margarine-like", "turkey sausage", "ground turkey", "chicken"]
mexicanSubWords = { 
    "grains" : ["flour tortilla", "white rice", "brown rice"],
    "sauces" : ["salsa sauce", "hot sauce"], 
    "spices" : ["garlic", "cayenne spices"], 
    "meats" : ["chicken", "pork", "beef"]}
italianSubWords = {
    "grains" : ["pasta", "garlic bread"],
    "sauces" : ["marinara sauce", "alfredo sauce", "pesto sauce"],
    "spices" : ["oregano", "basil", "rosemary", "thyme"],
    "meats" : ["chicken", "beef", "steak", "italian sausage"]}

def transformVegetarian(recipe, foodTable, weightTable):
    ingredients = recipe["ingredients"]
    recipe["title"] = "Vegetarian " + recipe["title"]
    
    for index,ingredient in enumerate(ingredients):
        if ingredient["foodGroup"] in nonVeg or ingredient["name"].find("broth") > -1 or ingredient["name"].find("stock") > -1:
            newIngredient = veggieSub(ingredient, foodTable)
            weights.convertWeight(ingredient, newIngredient, weightTable)
            ingredients[index] = newIngredient
            
    
def veggieSub(ingredient, foodTable):
    veggieSubs = findSubs(foodTable, veggieSubWords, nonVeg)
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
    
    return createSubstitute(substitute, veggieSubs, foodTable, ingredient)
    
def transformNonVegetarian(recipe, foodTable, weightTable):
    ingredients = recipe["ingredients"]
    recipe["title"] = "Non-Vegetarian " + recipe["title"]
    
    for index,ingredient in enumerate(ingredients):
        for word in veggieSubWords:
            if ingredient["name"].find(word) > -1:
                newIngredient = nonVeggieSub(ingredient, foodTable, word)
                weights.convertWeight(ingredient, newIngredient, weightTable)
                ingredients[index] = newIngredient
                break
            
def nonVeggieSub(ingredient, foodTable, word):
    nonVeggieSubs = findSubs(foodTable, nonVeggieSubWords)
    substitute = None
    if word == "tofu":
        substitute = "chicken"
    elif word == "beans":
        substitute = "sausage"
    elif word == "potatoes":
        substitute = "pork"
    elif word == "lentils":
        substitute = "beef"
    elif word == "mushrooms":
        substitute = "lamb"
    elif word == "tempeh":
        substitute = "salmon"
    
    if substitute == None:
        return ingredient
    
    return createSubstitute(substitute, nonVeggieSubs, foodTable)
    
def transformVegan(recipe, foodTable, weightTable):
    ingredients = recipe["ingredients"]
    recipe["title"] = "Vegan " + recipe["title"]
    
    for index,ingredient in enumerate(ingredients):
        if ingredient["foodGroup"] in nonVegan or ingredient["name"].find("honey") > -1 or ingredient["name"].find("broth") > -1 or ingredient["name"].find("stock") > -1:
            newIngredient = veganSub(ingredient, foodTable)
            weights.convertWeight(ingredient, newIngredient, weightTable)
            ingredients[index] = newIngredient
            
def veganSub(ingredient,foodTable):
    veganSubs = findSubs(foodTable, veganSubWords, nonVegan)
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
    
def transformNonVegan(recipe, foodTable, weightTable):
    ingredients = recipe["ingredients"]
    recipe["title"] = "Non-Vegan " + recipe["title"]
    
    for index,ingredient in enumerate(ingredients):
        for word in veganSubWords:
            if ingredient["name"].find(word) > -1:
                newIngredient = nonVeganSub(ingredient, foodTable, word)
                weights.convertWeight(ingredient, newIngredient, weightTable)
                ingredients[index] = newIngredient
                break
            
def nonVeganSub(ingredient, foodTable, word):
    nonVeganSubs = findSubs(foodTable, nonVeganSubWords)
    substitute = None
    if word == "tofu":
        substitute = "chicken"
    elif word == "beans":
        substitute = "sausage"
    elif word == "potatoes":
        substitute = "pork"
    elif word == "lentils":
        substitute = "beef"
    elif word == "mushrooms":
        substitute = "lamb"
    elif word == "tempeh":
        substitute = "salmon"
    elif word == "soymilk":
        substitute = "milk"
    elif word == "maple syrup":
        substitute = "honey"
    elif word == "margarine-like":
        substitute = "butter"
    
    if substitute == None:
        return ingredient
    
    return createSubstitute(substitute, nonVeganSubs, foodTable)
    
def transformCuisine(cuisine, recipe, foodTable, weightTable):
    ingredients = recipe["ingredients"]
    recipe["title"] =  cuisine + " " + recipe["title"]
            
    subWords = None
    if cuisine == "Mexican":
        subWords = copy.deepcopy(mexicanSubWords)
    elif cuisine == "Italian":
        subWords = copy.deepcopy(italianSubWords)
        
    for index,ingredient in enumerate(ingredients):
        if ingredient["foodGroup"] in cuisineFoodGroups:
            newIngredient = cuisineSub(ingredient, foodTable, subWords)
            weights.convertWeight(ingredient, newIngredient, weightTable)
            ingredients[index] = newIngredient

def cuisineSub(ingredient, foodTable, subTable):
    subList = []
    for key in subTable.keys():
        subList = subList + subTable[key]
    subs = findSubs(foodTable, subList)
    substitute = ""
    error = True
    if ingredient["foodGroup"] in game:
        if len(subTable["meats"]) > 0:
            substitute = subTable["meats"].pop(0)
            error = False
    elif ingredient["foodGroup"] in spicesAndHerbs:
        if len(subTable["spices"]) > 0:
            substitute = subTable["spices"].pop(0)
            error = False
    elif ingredient["foodGroup"] in sauces:
        if len(subTable["sauces"]) > 0:
            substitute = subTable["grains"].pop(0)
            error = False
    elif ingredient["foodGroup"] in grains:
        if len(subTable["grains"]) > 0:
            substitute = subTable["grains"].pop(0)
            error = False
    
    if error:
        return ingredient
        
    return createSubstitute(substitute, subs, foodTable)    

def transformLowCal(recipe, foodTable, weightTable):
    ingredients = recipe["ingredients"]
    recipe["title"] = "Lower calorie alternative to " + recipe["title"]
    
    for index,ingredient in enumerate(ingredients):
        if ingredient["foodGroup"] in highCal:
            newIngredient = lowCalSub(ingredient, foodTable)
            weights.convertWeight(ingredient, newIngredient, weightTable)
            ingredients[index] = newIngredient
            
def lowCalSub(ingredient,foodTable):
    lowCalSubs = findSubs(foodTable, lowCalSubWords, highCal)
    substitute = ""
    if ingredient["foodGroup"] in sausages:
        substitute = "turkey sausage"
    elif ingredient["foodGroup"] in pork:
        substitute = "ham"
    elif ingredient["foodGroup"] in beef:
        substitute = "ground turkey"
    elif ingredient["foodGroup"] in dairyAndEgg:
        if ingredient["name"].find("yogurt") > -1:
            substitute = "soy yogurt"
        else:
            substitute = "soymilk"
    elif ingredient["foodGroup"] in fats:
        if ingredient["name"].find("butter") > -1:
            substitute = "margarine"
        elif ingredient["name"].find("margarine") > -1:
            substitute = "margarine-like"
    elif ingredient["foodGroup"] in grains:
        if ingredient["name"].find("rice") > -1:
            substitute = "brown rice"
        elif ingredient["name"].find("bread") > -1:
			substitute = "english muffins"
    elif ingredient["foodGroup"] in vegetables:
        if ingredient["name"].find("potatoes") > -1:
            substitute = "cauliflower"
    
    return createSubstitute(substitute, lowCalSubs, foodTable, ingredient)

def transformLowFat(recipe, foodTable, weightTable):
    ingredients = recipe["ingredients"]
    recipe["title"] = "Lower fat alternative to " + recipe["title"]
    
    for index,ingredient in enumerate(ingredients):
        if ingredient["foodGroup"] in highFat:
            newIngredient = lowFatSub(ingredient, foodTable)
            weights.convertWeight(ingredient, newIngredient, weightTable)
            ingredients[index] = newIngredient
            
def lowFatSub(ingredient,foodTable):
    lowFatSubs = findSubs(foodTable, lowFatSubWords, highFat)
    substitute = ""
    if ingredient["foodGroup"] in sausages:
        substitute = "turkey sausage"
    elif ingredient["foodGroup"] in pork:
        substitute = "chicken"
    elif ingredient["foodGroup"] in beef:
        substitute = "ground turkey"
    elif ingredient["foodGroup"] in dairyAndEgg:
        if ingredient["name"].find("yogurt") > -1:
            substitute = "soy yogurt"
        else:
            substitute = "soymilk"
    elif ingredient["foodGroup"] in fats:
        if ingredient["name"].find("butter") > -1:
            substitute = "margarine"
        elif ingredient["name"].find("margarine") > -1:
            substitute = "margarine-like"
    
    return createSubstitute(substitute, lowFatSubs, foodTable, ingredient)

def findSubs(foodTable, subList, restrictions = []):
    subs = []
    for key in foodTable:
        food = foodTable[key]
        if food["foodGroup"] not in restrictions:
            for word in subList:
                match = ingredients.arrayMatch(word,food)
                if match[0] > 2:
                    subs.append(food)
                    
    return subs
        
def createSubstitute(substitute, substituteList, foodTable, ingredient):
    newIngredient = {}
    matchArray = {}
    substitute = substitute + ' '.join(ingredient["preparation"]) + ' '.join(ingredient["prep-description"])
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
        
    newIngredient["preparation"] = ingredient["preparation"]
    newIngredient["prep-description"] = ingredient["prep-description"]
    newIngredient["descriptor"] = ""
        
    return newIngredient
            
