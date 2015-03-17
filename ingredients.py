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
                match = arrayMatch(stoplist, ingredient["name"],foodTable[key]["description"],foodTable[key]["ID"])
                if match[0] > 0:
                    matchArray[match[1]] = match[0]
        
        if(len(matchArray) > 0):
            ingredient["ID"] = max(matchArray.iterkeys(), key=lambda(x): matchArray[x])
        else:
            ingredient["ID"] = "Not found"
        
        print ingredient["ID"]
        
        
        


def arrayMatch(stoplist,one,two,ID):
    oneArr = one.lower().replace(',','').split()
    twoArr = two.lower().split(", ")
    
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
    
    return [matches,two]
    
def matchWord(word1, word2):
    if(word1 == word2):
        return True
    elif (word1 + "s") == word2:
        return True
        
    return False