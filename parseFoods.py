# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 22:18:33 2015

@author: Kaustubh
"""

def parseFoods():
    foodFile = open("KnowledgeBase/FOOD_DES.txt","r")
    foods = []
    
    for line in foodFile:
        line = line.replace("~","")
        lineArray = line.split("^")
        food = {}
        food['ID'] = lineArray[0]
        food['foodGroup'] = lineArray[1]
        food['description'] = lineArray[2]
        foods.append(food)


    return foods
        
        
def parseFoodGroups():
    foodGroupFile = open("KnowledgeBase/FD_GROUP.txt","r")
    foodGroups = []
    
    for line in foodGroupFile:
        line = line.replace("~","")
        lineArray = line.split("^")
        foodGroup = {}
        foodGroup['ID'] = lineArray[0]
        foodGroup['description'] = lineArray[1].replace("\n","")
        foodGroups.append(foodGroup)
        
    return foodGroups
    
def parseWeights():
    weightFile = open("KnowledgeBase/WEIGHT.txt", "r")
    weights = []
    
    for line in weightFile:
        line = line.replace("~","")
        lineArray = line.split("^")
        weight = {}
        weight["ID"] = lineArray[0]
        weight["amount"] = lineArray[2]
        weight["unit"] = lineArray[3]
        weight["grams"] = lineArray[4].replace("\n","")
        weights.append(weight)
        
    print weights[0]
    
parseWeights()
        
