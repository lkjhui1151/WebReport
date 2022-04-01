from dataclasses import dataclass
from MySQLdb import DBAPISet
import mysql.connector
import pandas as pd
from importlib.resources import contents
from multiprocessing.sharedctypes import Value
from operator import index
from tokenize import group
from turtle import home
from xmlrpc.server import list_public_methods
from docxtpl import *
from numpy import append, empty
from collections import OrderedDict

mydb = mysql.connector.connect(
    host="10.11.101.32",
    user="admin01@INETMS",
    password="P@ssw0rd@INETMS",
    database="inetms_autoreport"
)

def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
def create_index(list,DB):
    temp_index = 1 
    for i in DB:
        i['no'] = temp_index
        list.append(i)
        temp_index+=1
    return(list)

path = 'D:/INET-MS/Auto report/GitHub/WebReport/code_krit/report_SOC/'
start_date ='2022-03-01' 
end_date = '2022-04-01'

mycursor = mydb.cursor()
cus_name= "xspringam"

sql = "select category,name_en,detail_th,priority from vulnerability"
mycursor.execute(sql)
vulnerability_DB = dictfetchall(mycursor)

sql = "select name,address,remark,type,name_th from device join company_list ON device.company_id = company_list.id join device_type ON device_type.id = device.device_id where company_list.initials = \""+cus_name+"\""
mycursor.execute(sql)
device_DB = dictfetchall(mycursor)

sql = "select AVG(value) from capa_daily_log join company_list ON company_list.id = capa_daily_log.company_id where company_list.initials = \""+cus_name+"\" and capa_daily_log.date between \""+start_date+"\" and \""+end_date+"\""
mycursor.execute(sql)
capa_DB = dictfetchall(mycursor)

device  =   []
vulnerability = []
create_index(device,device_DB)
create_index(vulnerability,vulnerability_DB)

contents={}
contents['name_capany'] =   device_DB[0]['name_th']
contents['inet_create'] =   'บริษัท อินเทอร์เน็ตประเทศไทย จำกัด (มหาชน)'
contents['capa']    =   '{:.4f}'.format(float(capa_DB[0]['AVG(value)'])) 
contents['vulnerability']   =   vulnerability
contents['device']  =     device

doc = DocxTemplate(path+"templateSOC.docx")

doc.render(contents)
doc.save(path+"SOC.docx")
# os.system(path+"SOC.docx")