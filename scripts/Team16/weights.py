# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:58:15 2015

@author: Kaustubh
"""
import fractions

def convertWeight(ingredient, newIngredient, weightTable):
    if "ID" not in newIngredient:
        newIngredient["ID"] = "00000"
        newIngredient["quantity"] = 1
        newIngredient["measurement"] = "piece"
        return    
    
    oldID = ingredient["ID"]
    if ingredient["quantity"].find("/") > -1:
        oldquantity = float(fractions.Fraction(ingredient["quantity"]))
    else:  
        oldquantity = float(ingredient["quantity"])
    oldMeasurement = ingredient["measurement"]
    if oldID in weightTable:
        oldWeights = weightTable[oldID]
    else:
        newIngredient["ID"] = "00000"
        newIngredient["quantity"] = 1
        newIngredient["measurement"] = "piece"
        return   
    
    grams = -1
    
    for entry in oldWeights:
        if matchMeasure(oldMeasurement, entry["unit"]):
            factor = oldquantity / float(entry["quantity"])
            grams = float(entry["grams"]) * factor
            break
        
    if grams == -1:
        factor = oldquantity / float(oldWeights[0]["quantity"])
        grams = float(oldWeights[0]["grams"]) * factor
        
    newID = newIngredient["ID"]
    if newID in weightTable:
        newWeights = weightTable[newID]
    else:
        newIngredient["ID"] = "00000"
        newIngredient["quantity"] = 1
        newIngredient["measurement"] = "piece"
        return   

    newIngredient["quantity"] = -1    
    
    for entry in newWeights:
        if matchMeasure(oldMeasurement, entry["unit"]):
            factor = grams / float(entry["grams"])
            newIngredient["quantity"] = roundToMeasure(float(entry["quantity"]) * factor)
            newIngredient["measurement"] = entry["unit"]
            break
            
    if newIngredient["quantity"] == -1:
        factor = grams / float(newWeights[0]["grams"])
        newIngredient["quantity"] = roundToMeasure(float(newWeights[0]["quantity"]) * factor)
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
    
    