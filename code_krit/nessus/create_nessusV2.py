import csv
from importlib.resources import contents
import json
from multiprocessing.sharedctypes import Value
from operator import index
from tokenize import group
from turtle import home
from xmlrpc.server import list_public_methods
from docxtpl import *
from numpy import append, empty
import pandas
import os
from collections import OrderedDict

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

csvFilePath = r'D:/INET-MS/Auto report/GitHub/WebReport/code_krit/nessus/All Dell cloud.csv'
jsonFilePath = r'D:/INET-MS/Auto report/GitHub/WebReport/code_krit/nessus/data.json'
makeJson(csvFilePath, jsonFilePath)


DataJSON = pandas.read_json(jsonFilePath)
ip=[DataJSON[i]["Host"] for i in DataJSON]
ip=list(dict.fromkeys(ip))
ip = sorted(ip, key=lambda d: (tuple(map(int, d.split('.')))))
# --------------------------------------make data ip port------------------------------------------------------------
# dict_ip_portopen = {}
# for i in ip:
#     dict_ip_portopen[i] = {'TCP':[],'UDP':[]}

# for i in DataJSON:
#     if DataJSON[i]["Protocol"]=='tcp':
#         dict_ip_portopen[DataJSON[i]["Host"]]['TCP'].append(DataJSON[i]["Port"])
#     elif  DataJSON[i]["Protocol"]=='udp':
#         dict_ip_portopen[DataJSON[i]["Host"]]['UDP'].append(DataJSON[i]["Port"])

# for key,value in dict_ip_portopen.items():
#     temp=""
#     for i in value:
#         value[i]=list(dict.fromkeys(value[i]))
#         value[i] = sorted(value[i], key=lambda d: (tuple(map(int, d.split('.')))))
#         if '0' in value[i]:
#             value[i].remove('0')

#         for index in range(len(value[i])):
#             if index == 0:
#                 if i =='UDP':
#                     if temp != "":
#                         temp=temp+'\n'+i+' : '+value[i][index]
#                     else:
#                         temp = i+' : '+value[i][index]
#                 else:
#                     temp = i+' : '+value[i][index]
#             else : 
#                 temp = temp+', '+value[i][index]
#     dict_ip_portopen[key]['port']=temp
# list_all_ip_port=[]
# index=1 
# for key,value in dict_ip_portopen.items():
#     ip_port_={}
#     ip_port_['No']=index
#     ip_port_['host']= key
#     ip_port_['port']=value['port']
#     list_all_ip_port.append(ip_port_)
#     index+=1
# -----------------------------------------------------------------------------------------------------------------------------
# ==============================================-make data detail==============================================================
dict_port_ip= {}
vulnerability=[]
subContent = {}
countCheck = 0
GroupName = {}


# ======================================NEW=====================================
def clear_list_dict_dup(list_dup):
    seen = set()
    new_l = []
    for d in list_dup:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)
    return new_l

list_name_detail_nessus=[]
list_ip_id_port= []

for i in DataJSON:
    subContentName = {}
    subContentIP = {}
    if DataJSON[i]['Risk'] != "None":
# --------------------------------------------------------------?
        subContentName["id"] = DataJSON[i]['Plugin ID']
        subContentName["name"] = DataJSON[i]['Name']
        subContentName["description"] = DataJSON[i]['Description']
        subContentName["solution"] = DataJSON[i]['Solution']
        if DataJSON[i]['See Also']=="":
            subContentName["remark"] = " - "
        else:
            subContentName["remark"] = DataJSON[i]['See Also']
        if DataJSON[i]['Risk'] == "Critical":
            subContentName["color"] = "#7030A0"
            subContentName["risk"] = 1
        elif DataJSON[i]['Risk'] == "High":
            subContentName["color"] = "#FF0000"
            subContentName["risk"] = 2
        elif DataJSON[i]['Risk'] == "Medium":
            subContentName["color"] = "#FFC000"
            subContentName["risk"] = 3
        elif DataJSON[i]['Risk'] == "Low":
            subContentName["color"] = "#FFFF00"
            subContentName["risk"] = 4
        list_name_detail_nessus.append(subContentName)
# ============================================================?
        subContentIP["ip"] = DataJSON[i]['Host']
        subContentIP["id"] = DataJSON[i]['Plugin ID']
        subContentIP["port"] = DataJSON[i]['Port']
        subContentIP["prot"] = DataJSON[i]['Protocol']
        list_ip_id_port.append(subContentIP)
# ================================================================?
# ----------------------------------------------------------------?
list_ip_id_port = clear_list_dict_dup(list_ip_id_port)
list_name_detail_nessus= clear_list_dict_dup(list_name_detail_nessus)
port = ""
list_ip=[]
dict_ip={}
for j in ip:
    list_ip=[]
    dict_id={}
    for i in list_ip_id_port:
        if i['ip'] in j:
            if i['id'] in dict_id:
                port = port+"\n"+i['prot']+': '+i['port']
            else:
                port = ""
                port = i['prot']+': '+i['port']
            dict_id[i['id']] = port
    dict_ip[j]=dict_id

vulnerability_nes2=[]
for i,j in dict_ip.items():
    dict_content    =   {}
    dict_content['ip']  = i
    list_detail=[]
    for x,y in j.items():
        for a in list_name_detail_nessus:
            if  x   ==  a['id']:
                dict_content["id"]          = a["id"]
                dict_content["name"]        = a["name"]
                dict_content["port"]        = y
                dict_content["description"] = a["description"]
                dict_content["solution"]    = a["solution"]
                dict_content["remark"]      = a["remark"]
                dict_content["risk"]        = a["risk"]
                dict_content["color"]       = a["color"]
                list_detail.append(dict_content)
    dict_content['detail']= list_detail
    vulnerability_nes2.append(dict_content)

contents={}
contents['vulnerability_nes2']=vulnerability_nes2
with open('D:\INET-MS\Auto report\GitHub\WebReport\code_krit\\nessus\dataout.json', 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(contents, indent=4))

# print(vulnerability_nes2)
# vulnerability.sort(key=runIndex, reverse=False)
# for i in range(len(vulnerability)):
#     vulnerability[i]['no'] = i+1 
#     if vulnerability[i]['risk'] == 1:
#         vulnerability[i]['risk'] = "Critical"
#     if vulnerability[i]['risk'] == 2:
#         vulnerability[i]['risk'] = "High"
#     if vulnerability[i]['risk'] == 3:
#         vulnerability[i]['risk'] = "Medium"
#     if vulnerability[i]['risk'] == 4:
#         vulnerability[i]['risk'] = "Low"

# # ==========================================================================================================
contents={}
contents['vulnerability_nes2']=vulnerability_nes2

# print(contents)

# doc.render(contents)
# doc.save("generated_nessus.docx")
# os.system("generated_nessus.docx")

