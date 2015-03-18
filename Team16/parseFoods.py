# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 22:18:33 2015

@author: Kaustubh
"""

def parseFoods():
    foodFile = open("../KnowledgeBase/FOOD_DES.txt","r")
    foods = {}
    
    for line in foodFile:
        line = line.replace("~","")
        lineArray = line.split("^")
        food = {}
        food['ID'] = lineArray[0]
        food['foodGroup'] = lineArray[1]
        food['description'] = lineArray[2]
        foods[lineArray[0]] = food

    return foods
        
        
def parseFoodGroups():
    foodGroupFile = open("../KnowledgeBase/FD_GROUP.txt","r")
    foodGroups = {}
    
    for line in foodGroupFile:
        line = line.replace("~","")
        lineArray = line.split("^")
        foodGroup = {}
        foodGroup['ID'] = lineArray[0]
        foodGroup['description'] = lineArray[1].replace("\n","")
        foodGroups[lineArray[0]] = foodGroup
        
    return foodGroups
    
def parseWeights():
    weightFile = open("../KnowledgeBase/WEIGHT.txt", "r")
    weights = {}
    
    for line in weightFile:
        line = line.replace("~","")
        lineArray = line.split("^")
        weight = {}
        weight["ID"] = lineArray[0]
        weight["amount"] = lineArray[2]
        weight["unit"] = lineArray[3]
        weight["grams"] = lineArray[4].replace("\n","")
        if lineArray[0] in weights.keys():
            weights[lineArray[0]].append(weight)
        else:
            weights[lineArray[0]] = [weight]
        
    return weights
    
def createStopList():
    stoplistFile = open("stoplist.txt", "r")
    stoplist = []
    
    for line in stoplistFile:
        stoplist.append(line.strip())
        
    return stoplist
        
