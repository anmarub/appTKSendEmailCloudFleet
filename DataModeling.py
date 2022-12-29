import pandas as pd
import numpy as np


class DataModeling():
    
    def __init__(self):
        pass

    @staticmethod
    def detailedDailyReport(pathInventoryFleet: str, pathCheckList: str):
        # lectura de archivo por pandas
        fileExcel = pd.read_excel(pathInventoryFleet, sheet_name='Inventario Vehiculos')
        apiCloudFleet = pd.read_json(pathCheckList)
        # Conversion de archivos a Dataframes para modelamiento con pandas
        dfExcel = pd.DataFrame(fileExcel)
        dfJson = pd.DataFrame(apiCloudFleet)
        # Llamo las columnas que necesito
        filterField = dfExcel[["ID", "División", "Región", "CO", "Administracion"]]
        # Filtro de archivo de excel por segmentacion tipo administracion
        filterCars = filterField.query("Administracion=='1.PROPIO' or Administracion=='2.RENTING'")
        # elimino del archivo json las placas duplicadas y dejo la ultima registrada con el parametro keep
        mergeChecklistToCars = dfJson.drop_duplicates(subset=['vehicle_code'], keep='last')
        #realizo la union de los dos dataframen
        compare = filterCars.merge(mergeChecklistToCars, left_on='ID', right_on='vehicle_code', how='left')
        #Selecciono los campos de la tabla del infome
        reduceTable = compare[['ID', 'División', 'Región', 'CO', 'Administracion', 'number', 'checklistDate',
                                'status_name', 'startedAt', 'endedAt','durationInMinutes','type_name','odometer',
                                'driver_name','statistics_qtyVariablesApproved','statistics_qtyVariablesRejected',
                                'statistics_qtyVariablesCritical','statistics_qtyTotalVariables','comment']]
        #exporta el informe a excel
        reduceTable.to_excel('C:\\Users\\andres.rubiano\\OneDrive\\Project\\pySgcWeb\\CloudFleet\\file\\Informe_Checklist.xlsx', index=False)
        return reduceTable
    
    @staticmethod
    def groupByPendingDivision(detailsData: pd.DataFrame):
        #filtra las placas sin Checklist
        filtersNotNulls = detailsData[detailsData.number.notnull()]
        filtersIsNulls = detailsData[detailsData.number.isnull()]
        #crea un resumen por grupo checklist ok
        groupNotNull = pd.DataFrame({'count' : filtersNotNulls.groupby( ["Región"] ).size()}).reset_index()
        groupNotNull.rename(columns={'count': 'Cant Ejecutados'}, inplace=True)
        #crea un resumen por grupo checklist pendientes?
        groupByIsNullRegion = pd.DataFrame({'count' : filtersIsNulls.groupby( [ "División", "Región"] ).size()}).reset_index()
        groupByIsNullRegion.rename(columns={'count': 'Cant Veh Sin Checklist'}, inplace=True)
        mergeTables = groupNotNull.merge(groupByIsNullRegion, left_on='Región', right_on='Región', how='left')
        tableReturn = mergeTables[['División', 'Región', 'Cant Ejecutados', 'Cant Veh Sin Checklist']]
        return tableReturn
    
    @staticmethod
    def checklistStatusByDivision(detailsData: pd.DataFrame):
        #filtra las placas sin Checklist
        filtersNulls = detailsData[detailsData.number.notnull()]
        tableCountStatus = pd.pivot_table(
                            filtersNulls, 
                            index=['División', 'Región'],
                            columns=['status_name'],
                            aggfunc={'number': 'count'})
        tableCountStatus.columns = tableCountStatus.columns.droplevel(0)
        tableCountStatus.columns.name = None
        tableCountStatus = tableCountStatus.reset_index()
        return tableCountStatus