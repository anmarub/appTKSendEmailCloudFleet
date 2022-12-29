# -*- coding: utf-8 -*-
"""
Created on Mon Sep  19 16:45:03 2022

@author: andres.rubiano
"""
import os
import json
import pandas as pd
from datetime import date

class Utilities():
    
    def __init__(self):
        pass
    
    
    @staticmethod    
    def descomprimirObjecto(dataList):
        data_r = {}
        output = []
        for data in dataList:
            for keyLeve1, valueLeve1 in data.items():
                if type(valueLeve1) == dict:
                    for keyLeve2, valueLeve2 in valueLeve1.items():
                        if type(valueLeve2) == dict:
                            for keyLeve3, valueLeve3 in valueLeve2.items():
                                data_r[keyLeve1+"_"+keyLeve2+"_"+keyLeve3]=valueLeve3
                        else:
                            data_r[keyLeve1+"_"+keyLeve2]=valueLeve2
                else:
                    data_r[keyLeve1]=valueLeve1
            output.append(data_r)
            data_r = {}
        return output
    
    @staticmethod
    def saveDataFormtJson(data, typeService: str):
        FILE = f'C:\\Users\\andres.rubiano\\OneDrive\\Project\\pySgcWeb\\CloudFleet\\file\\archivo_{typeService}.json'
        # Append JSON object to output file JSON array
        if os.path.isfile(FILE):
            # File exists
            with open(FILE, encoding='utf-8', mode='a+') as file:
                json.dump(data, file, indent=4)
        else:
            # Create file
            with open(FILE, encoding='utf-8', mode='w') as file:
                json.dump(data, file, indent=4)
    
    @staticmethod
    def deleteKeyListArray(list_data: list, keyDelete: str):
            objNew = []
            for index in range(0, len(list_data)):
                dictData = list_data[index]
                del dictData[f'{keyDelete}']
                objNew.append(dictData)
            return objNew
        
        