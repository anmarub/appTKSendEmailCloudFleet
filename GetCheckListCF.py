import requests
import json
import time
from datetime import date
import numpy as np
import pandas as pd
import os
import environments
import Utilities as ut


class getCheckListCF():
    
    def __init__(self):
        pass
    
    @staticmethod
    def getCheckListForDay(metodo: str, url: str, payload: str, header: dict, fecha_Ini: str, fecha_Fin: str):
        OUTPUT = []
        try:
            url = f'{url}createdAtFrom={fecha_Ini}&createdAtTo={fecha_Fin}'
            response = requests.request(metodo, url, data=payload, headers=header)

            if response.status_code == 200:    
                data = json.loads(response.text)
                
                for i in range(0, len(data)):
                    df = data[i]
                    OUTPUT.append(data[i])

                while 'X-NextPage' in response.headers:              
                    print(response.headers['X-NextPage'])
                    url = response.headers['X-NextPage']
                    time.sleep(2.1)
                    response = requests.request(metodo, url, data=payload, headers=header)
                    data = json.loads(response.text)
                    
                    for i in range(0, len(data)):
                        OUTPUT.append(data[i])
            else:
                print(f'codigo error: {response.status_code}')
            return OUTPUT
        except Exception as e:
            print(f'Se ha registrado una excepción en la Api: {e}')
