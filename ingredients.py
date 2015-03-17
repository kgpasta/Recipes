# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 23:00:08 2015

@author: Kaustubh
"""
def identifyIngredients(recipe,foodTable,stoplist):
    for ingredient in recipe["ingredients"]:
        matchArray = {}
        for key in foodTable:
            if "description" in foodTable[key]:
                match = arrayMatch(ingredient["name"],foodTable[key], stoplist)
                if match[0] > 0:
                    matchArray[match[2]] = match[0]
        
        if(len(matchArray) > 0):
            ingredient["ID"] = max(matchArray.iterkeys(), key=lambda(x): matchArray[x])
            ingredient["foodGroup"] = foodTable[ingredient["ID"]]["foodGroup"]
        else:
            ingredient["ID"] = "N/A"
            ingredient["foodGroup"] = "N/A"
        
        


def arrayMatch(one,two,stoplist = []):
    oneArr = one.lower().replace(',','').split()
    description = two["description"]
    ID = two["ID"]
    twoArr = description.lower().split(", ")
    
    for word in twoArr:
        if 'or' in word.split():
            twoArr = twoArr + word.split()
            twoArr.remove(word)
    
    matches = 0
    for word in oneArr:
        for index, word2 in enumerate(twoArr):
            if matchWord(word, word2) and word not in stoplist:
                if(index == 0):
                    matches = matches + 3
                else:
                    matches = matches + 1
    
    return [matches,two, ID]
    
def matchWord(word1, word2):
    if(word1 == word2):
        return True
    elif (word1 + "s") == word2:
        return True
        
    return False