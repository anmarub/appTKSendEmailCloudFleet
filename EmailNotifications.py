import win32com.client as win32
from datetime import datetime
import pandas as pd
import os
import numpy as np


class EmailNotifications:
    
    def __init__(self):
        pass
    
    @staticmethod
    def emailCheckList(pendingDetailByDivision: pd.DataFrame, consolidatedByStateAndDivision: pd.DataFrame):
        consolidatedByStateAndDivision.Aprobado.round()
        pendingDetailByDivision = pendingDetailByDivision.to_html(index=False)
        consolidatedByStateAndDivision = consolidatedByStateAndDivision.to_html(index=False)
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.Subject = 'Inspecciones no realizadas ' + datetime.now().strftime('%#d %b %Y %H:%M')
        #mail.To = "andres.rubiano@empresasgasco.co"
        mail.To = "TransportesNacional@empresasgasco.co"
        mail.CC = "mauricio.hernandez@empresasgasco.co"
        
        attachment = mail.Attachments.Add(os.getcwd() + "\\img\\Firma.png")
        attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "firma_img")

        mail.HTMLBody = r"""
        <p><span style="font-size:11pt"><span style="font-family:Calibri,sans-serif">Buen d&iacute;a</span></span></p>
        <p><span style="font-size:11pt"><span style="font-family:Calibri,sans-serif">Equipo Transportes, a continuaci&oacute;n, 
        relaciono estatus de la ejecuci&oacute;n del chequeo preoperacional del d&iacute;a <strong>""" +datetime.now().strftime('%#d %b %Y %H:%M')+ """</strong>, 
        los datos relacionados son los contenidos en la plataforma CloudFleet. adjunto encontrara el detalle de la 
        informaci&oacute;n para su respectiva validaci&oacute;n:</span></span></p>
        <p><strong><span style="font-size:13pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:#2f5496">Consolidado Divisi&oacute;n Ejecuci&oacute;n Check List</span></span></span></strong></p>
            """ +pendingDetailByDivision+ """
        <br><br>
        <h1><strong><span style="font-size:13pt"><span style="font-family:&quot;Calibri Light&quot;,sans-serif"><span style="color:#2f5496">Consolidado Estado Check List Realizado</span></span></span></strong></h1>
            """ +consolidatedByStateAndDivision+ """
        <p><span style="font-size:11pt"><span style="font-family:Calibri,sans-serif">Cualquier informaci&oacute;n adicional con gusto ser&aacute; atendida</span></span></p>
        <p><span style="font-size:11.0pt"><span style="font-family:&quot;Calibri&quot;,sans-serif">Cordialmente, </span></span></p>
        <br><br>
        <img src="cid:firma_img"><br><br>
        """
        mail.Attachments.Add(os.getcwd() + "\\file\\Informe_Checklist.xlsx")
        mail.Send()
