# Import Required Library
from tkinter import *
from tkcalendar import Calendar
from datetime import date
from datetime import date
import os
import environments
import Utilities as ut
import GetCheckListCF as gc
import DataModeling as dm
import EmailNotifications as en
from os import remove
from os import path

objFin = []
METODO = 'GET'
PAYLOAD = ''

URL = os.environ['API_CHECKLIST']

HEADER = {
    'Authorization': os.environ['KEY_AUTHORIZATION'],
    'Content-Type': 'application/json; charset=utf-8'
}

# Ubicacion de los Archivos
pathInventoryFleet = 'C:\\Users\\andres.rubiano\\OneDrive\\Project\\pySgcWeb\\CloudFleet\\file\\inventario.xlsx'
pathCheckList = 'C:\\Users\\andres.rubiano\\OneDrive\\Project\\pySgcWeb\\CloudFleet\\file\\archivo_prueba.json'

if path.exists('C:\\Users\\andres.rubiano\\OneDrive\\Project\\pySgcWeb\\CloudFleet\\file\\archivo_prueba.json'):
    remove('C:\\Users\\andres.rubiano\\OneDrive\\Project\\pySgcWeb\\CloudFleet\\file\\archivo_prueba.json')

if path.exists('C:\\Users\\andres.rubiano\\OneDrive\\Project\\pySgcWeb\\CloudFleet\\file\\Informe_Checklist.xlsx'):
    remove('C:\\Users\\andres.rubiano\\OneDrive\\Project\\pySgcWeb\\CloudFleet\\file\\Informe_Checklist.xlsx')

# Create Object
root = Tk()
root.title('Generar reporte Checklist')

# Set dimentions
root.geometry("400x400")

today = date.today()
 
# Add Calendar
cal = Calendar(root, selectmode = 'day', locale='es_CO', date_pattern='yyyy-MM-dd',
               year = today.year, month = today.month,
               day = today.day)
cal.pack(pady = 20)
 
def grad_date():
    date_ini = cal.get_date() + 'T00:00:01Z'
    date_end = cal.get_date() + 'T23:59:59Z'
    # Obtener informacion de la Api
    i = gc.getCheckListCF.getCheckListForDay(METODO, URL, PAYLOAD, HEADER, date_ini, date_end)
    # Descomprimir Json recibidos
    x = ut.Utilities.descomprimirObjecto(i)
    # Eliminar la key del diccionario -> Variable
    y = ut.Utilities.deleteKeyListArray(x, 'variables')
    # Serializar informacion en un JSON
    ut.Utilities.saveDataFormtJson(y, 'prueba')
    # Method analizar informacion
    j = dm.DataModeling.detailedDailyReport(pathInventoryFleet, pathCheckList)
    a = dm.DataModeling.groupByPendingDivision(j)
    b = dm.DataModeling.checklistStatusByDivision(j)
    # Enviar Notificacion
    en.EmailNotifications.emailCheckList(a, b)
    date.config(text = "Informe Checklist Enviado Dia: " + cal.get_date())

# Add Button and Label
Button(root, text = "Generar Informe",
       command = grad_date).pack(pady = 20)
 
date = Label(root, text = "")
date.pack(pady = 20)
 
# Execute Tkinter
root.mainloop()