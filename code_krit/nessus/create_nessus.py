import csv
from importlib.resources import contents
import json
from operator import index
from tokenize import group
from turtle import home
from docxtpl import *
import pandas
import os

doc = DocxTemplate("D:/INET-MS/Auto report/GitHub/WebReport/code_krit/nessus//template_nessus.docx")

def makeJson(csvFilePath, jsonFilePath):
    data = {}
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        key_id = 0
        for rows in csvReader:
            key = key_id
            data[key] = rows
            key_id += 1
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

# DataJson = open(
#     "./data.json", "w")
# DataJson.close()
csvFilePath = r'D:/INET-MS/Auto report/GitHub/WebReport/code_krit/nessus/data_dump.csv'
jsonFilePath = r'D:/INET-MS/Auto report/GitHub/WebReport/code_krit/nessus/data.json'
makeJson(csvFilePath, jsonFilePath)

DataJSON = pandas.read_json(jsonFilePath)
ip=[DataJSON[i]["Host"] for i in DataJSON]
ip=list(dict.fromkeys(ip))
ip = sorted(ip, key=lambda d: (tuple(map(int, d.split('.')))))
# --------------------------------------make data------------------------------------------------------------
dict_ip_portopen = {}
for i in ip:
    dict_ip_portopen[i] = {'TCP':[],'UDP':[]}

for i in DataJSON:
    if DataJSON[i]["Protocol"]=='tcp':
        dict_ip_portopen[DataJSON[i]["Host"]]['TCP'].append(DataJSON[i]["Port"])
    elif  DataJSON[i]["Protocol"]=='udp':
        dict_ip_portopen[DataJSON[i]["Host"]]['UDP'].append(DataJSON[i]["Port"])

for key,value in dict_ip_portopen.items():
    for i in value:
        value[i]=list(dict.fromkeys(value[i]))
        value[i] = sorted(value[i], key=lambda d: (tuple(map(int, d.split('.')))))
        if '0' in value[i]:
            value[i].remove('0')
        temp=""
        for port_ in value[i]:
            if temp == "":
                temp = i+' : '+port_ 
            else : 
                temp = temp+', '+port_; 

        dict_ip_portopen[key][i]=temp
    
# print(dict_ip_portopen)
list_all_ip_port=[]
index=1 
for key,value in dict_ip_portopen.items():
    ip_port_={}
    ip_port_['No']=index
    ip_port_['host']= key
    ip_port_['TCP']=value['TCP']
    ip_port_['UDP']=value['UDP'] 
    list_all_ip_port.append(ip_port_)
    index+=1
    # print(ip_port_)
# -----------------------------------------------------------------------------------------------------------
contents={}
contents['contents_ip']=list_all_ip_port
# print(contents)


doc.render(contents)
doc.save("generated_nessus.docx")
os.system("generated_nessus.docx")

