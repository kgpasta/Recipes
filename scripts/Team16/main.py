# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 22:56:28 2015

@author: Kaustubh
"""
import scrape, parseFoods, ingredients, transformation
import sys

def main(mutation = "vegetarian", url = 'http://allrecipes.com/Recipe/Easy-Garlic-Broiled-Chicken/'):
    if len(sys.argv) > 1:
        mutation = sys.argv[1]
    if len(sys.argv) > 2:
        url = sys.argv[2]


    recipe = scrape.get_recipe(url) 
    foodTable = parseFoods.parseFoods()
    foodGroupTable = parseFoods.parseFoodGroups()
    weightTable = parseFoods.parseWeights()
    stoplist = parseFoods.createStopList()
    
    ingredients.identifyIngredients(recipe,foodTable,stoplist)
    
    if mutation == "vegetarian":
        transformation.transformVegetarian(recipe, foodTable, weightTable)
    if mutation == "normal":
        transformation.transformNonVegetarian(recipe, foodTable, weightTable)
    if mutation == "mexican":
        transformation.transformCuisine("Mexican", recipe, foodTable, weightTable)
    if mutation == "italian":
        transformation.transformCuisine("Italian", recipe, foodTable, weightTable)
    if mutation == "vegan":
        transformation.transformVegan(recipe, foodTable, weightTable)
    if mutation == "nonvegan":
        transformation.transformNonVegan(recipe,foodTable, weightTable)
    if mutation == "lowcal":
        transformation.transformLowCal(recipe, foodTable, weightTable)
    if mutation == "lowfat":
        transformation.transformLowFat(recipe, foodTable, weightTable)
    
    
    
    return recipe
    
    
main()