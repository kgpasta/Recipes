# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:58:15 2015

@author: Kaustubh
"""
import fractions

def convertWeight(ingredient, newIngredient, weightTable):
    if "ID" not in newIngredient:
        newIngredient["ID"] = "00000"
        newIngredient["amount"] = 1
        newIngredient["measurement"] = "piece"
        return    
    
    oldID = ingredient["ID"]
    if ingredient["amount"].find("/") > -1:
        oldAmount = float(fractions.Fraction(ingredient["amount"]))
    else:  
        oldAmount = float(ingredient["amount"])
    oldMeasurement = ingredient["measurement"]
    if oldID in weightTable:
        oldWeights = weightTable[oldID]
    else:
        newIngredient["ID"] = "00000"
        newIngredient["amount"] = 1
        newIngredient["measurement"] = "piece"
        return   
    
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
    if newID in weightTable:
        newWeights = weightTable[newID]
    else:
        newIngredient["ID"] = "00000"
        newIngredient["amount"] = 1
        newIngredient["measurement"] = "piece"
        return   

    newIngredient["amount"] = -1    
    
    for entry in newWeights:
        if matchMeasure(oldMeasurement, entry["unit"]):
            factor = grams / float(entry["grams"])
            newIngredient["amount"] = roundToMeasure(float(entry["amount"]) * factor)
            newIngredient["measurement"] = entry["unit"]
            break
            
    if newIngredient["amount"] == -1:
        factor = grams / float(newWeights[0]["grams"])
        newIngredient["amount"] = roundToMeasure(float(newWeights[0]["amount"]) * factor)
        newIngredient["measurement"] = newWeights[0]["unit"]
        
def matchMeasure(word1, word2):
    word1.replace("tsp", "teaspoon")
    word1.replace("tbsp", "tablespoon")
    word1.replace("oz", "ounces")
    word1.replace("fl", "fluid")
    word2.replace("tsp", "teaspoon")
    word2.replace("tbsp", "tablespoon")
    word2.replace("oz", "ounces")
    word2.replace("fl", "fluid")
    
    if word1 == word2:
        return True
    elif (word1 + "s") == word2:
        return True
    
    return False
    
def roundToMeasure(number):
    return round(number * 4) / 4
    
    