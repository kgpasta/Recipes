# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:58:15 2015

@author: Kaustubh
"""

def convertWeight(ingredient, newIngredient, weightTable):
    oldID = ingredient["ID"]
    oldAmount = float(ingredient["amount"])
    oldMeasurement = ingredient["measurement"]
    oldWeights = weightTable[oldID]
    
    grams = -1
    
    for entry in oldWeights:
        if matchMeasure(oldMeasurement, entry["unit"]):
            factor = oldAmount / float(entry["amount"])
            grams = float(entry["grams"]) * factor
            break
        
    if grams == -1:
        factor = oldAmount / float(oldWeights[0]["amount"])
        grams = float(oldWeights[0]["grams"]) * factor
        
    newID = newIngredient["ID"]
    newWeights = weightTable[newID]

    newIngredient["amount"] = -1    
    
    for entry in newWeights:
        if matchMeasure(oldMeasurement, entry["unit"]):
            factor = grams / float(entry["grams"])
            newIngredient["amount"] = float(entry["amount"]) * factor
            newIngredient["measurement"] = entry["unit"]
            
    if newIngredient["amount"] == -1:
        factor = grams / float(newWeights[0]["grams"])
        newIngredient["amount"] = roundToMeasure(float(newWeights[0]["amount"]) * factor)
        newIngredient["measurement"] = newWeights[0]["unit"]
        
def matchMeasure(word1, word2):
    if word1 == word2:
        return True
    
    return False
    
def roundToMeasure(number):
    return round(number * 4) / 4
    
    