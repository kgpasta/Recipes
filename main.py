# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 22:56:28 2015

@author: Kaustubh
"""
import scrape, parseFoods, ingredients, transformation

def main():
    recipe = scrape.get_recipe()
    
    foodTable = parseFoods.parseFoods()
    foodGroupTable = parseFoods.parseFoodGroups()
    weightTable = parseFoods.parseWeights()
    stoplist = parseFoods.createStopList()
    
    ingredients.identifyIngredients(recipe,foodTable,stoplist)
    
    #transformation.transformVegetarian(recipe, foodTable, weightTable, stoplist)    
    transformation.transformVegan(recipe, foodTable, weightTable, stoplist)
    
    print recipe
    
    
main()