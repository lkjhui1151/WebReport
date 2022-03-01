import csv
from importlib.resources import contents
import json
from multiprocessing.sharedctypes import Value
from operator import index
from tokenize import group
from turtle import home
from xmlrpc.server import list_public_methods
from docxtpl import *
from numpy import empty
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
dict_ip_portopen = {}
for i in ip:
    dict_ip_portopen[i] = {'TCP':[],'UDP':[]}

for i in DataJSON:
    if DataJSON[i]["Protocol"]=='tcp':
        dict_ip_portopen[DataJSON[i]["Host"]]['TCP'].append(DataJSON[i]["Port"])
    elif  DataJSON[i]["Protocol"]=='udp':
        dict_ip_portopen[DataJSON[i]["Host"]]['UDP'].append(DataJSON[i]["Port"])

for key,value in dict_ip_portopen.items():
    temp=""
    for i in value:
        value[i]=list(dict.fromkeys(value[i]))
        value[i] = sorted(value[i], key=lambda d: (tuple(map(int, d.split('.')))))
        if '0' in value[i]:
            value[i].remove('0')

        for index in range(len(value[i])):
            if index == 0:
                if i =='UDP':
                    if temp != "":
                        temp=temp+'\n'+i+' : '+value[i][index]
                    else:
                        temp = i+' : '+value[i][index]
                else:
                    temp = i+' : '+value[i][index]
            else : 
                temp = temp+', '+value[i][index]
    dict_ip_portopen[key]['port']=temp
list_all_ip_port=[]
index=1 
for key,value in dict_ip_portopen.items():
    ip_port_={}
    ip_port_['No']=index
    ip_port_['host']= key
    ip_port_['port']=value['port']
    list_all_ip_port.append(ip_port_)
    index+=1
# -----------------------------------------------------------------------------------------------------------------------------
# ==============================================-make data detail==============================================================
name = [DataJSON[i]["Name"] for i in DataJSON if DataJSON[i]["Risk"] != "None"]
name = list(dict.fromkeys(name))
dict_port_ip= {}
vulnerability=[]
subContent = {}
countCheck = 0
GroupName = {}

for i in DataJSON:
    if DataJSON[i]['Risk'] != 'None':
        if DataJSON[i]['Name'] in GroupName:
            GroupName[DataJSON[i]['Name']] += 1
        else:
            GroupName[DataJSON[i]['Name']] = 1

for j in name:
    dict_port_ip= {}
    port_udp = []
    port_tcp = []
    for i in DataJSON:
        
        if DataJSON[i]['Risk'] != "None":
            if DataJSON[i]['Name'] == j:

                if DataJSON[i]['Protocol'] == 'tcp':
                    port_tcp.append(DataJSON[i]['Port'])
                elif DataJSON[i]['Protocol'] == 'udp':
                    port_udp.append(DataJSON[i]['Port'])    

                if DataJSON[i]['Host'] in dict_port_ip:
                    dict_port_ip[DataJSON[i]['Host']].append(DataJSON[i]['Port'])
                else:
                    dict_port_ip[DataJSON[i]['Host']]=[DataJSON[i]['Port']]
                countCheck += 1
                if countCheck == GroupName[DataJSON[i]['Name']]:
 
                    port_tcp = list(dict.fromkeys(port_tcp))
                    port_tcp=sorted(port_tcp, key = lambda x: int(x))
                    port_udp = list(dict.fromkeys(port_udp))
                    port_udp=sorted(port_udp, key = lambda x: int(x))
                    
                    port= ""
                    for index in range(len(port_tcp)):
                        if index == 0:
                            port = 'TCP: '+port_tcp[index]
                        else:
                            port = port + ', ' +port_tcp[index]
                    for index in range(len(port_udp)):
                        if index == 0:
                            if port =="":
                                port = 'UDP: '+port_udp[index]
                            else:
                                port = port + '\n UDP: '+port_udp[index]
                        else:
                            port = port + ', ' +port_udp[index]

                    ip = ""
                    list_ip=sorted(dict_port_ip, key=lambda d: (tuple(map(int, d.split('.')))))
                    dict_port_ip=dict(OrderedDict([(a , dict_port_ip[a])for a in list_ip]))
                    
                    for key ,value in dict_port_ip.items():
                        value = list(dict.fromkeys(value))
                        value = sorted(value, key = lambda d: int(d))
                        if ip=="":
                            pass
                        else:
                            ip = ip +', '
                        ip = ip + key + '('
                        for index in range(len(value)):
                            if index == 0:
                                ip = ip + value[index]
                            else:
                                ip = ip +', '+ value[index]
                        ip = ip +')'  
                    subContent["host"] = ip
                    subContent["port"] = port 
                    subContent["name"] = DataJSON[i]['Name']
                    subContent["description"] = DataJSON[i]['Description']
                    subContent["solution"] = DataJSON[i]['Solution']
                    if DataJSON[i]['See Also']=="":
                        subContent["remark"] = " - "
                    else:
                        subContent["remark"] = DataJSON[i]['See Also']
                    
                    if DataJSON[i]['Risk'] == "Critical":
                        subContent["color"] = "#7030A0"
                        subContent["risk"] = 1
                    elif DataJSON[i]['Risk'] == "High":
                        subContent["color"] = "#FF0000"
                        subContent["risk"] = 2
                    elif DataJSON[i]['Risk'] == "Medium":
                        subContent["color"] = "#FFC000"
                        subContent["risk"] = 3
                    elif DataJSON[i]['Risk'] == "Low":
                        subContent["color"] = "#FFFF00"
                        subContent["risk"] = 4
                    vulnerability.append(subContent)
                    subContent = {}
                    countCheck = 0
def runIndex(e):
    return e['risk']
vulnerability.sort(key=runIndex, reverse=False)
for i in range(len(vulnerability)):
    vulnerability[i]['no'] = i+1 
    if vulnerability[i]['risk'] == 1:
        vulnerability[i]['risk'] = "Critical"
    if vulnerability[i]['risk'] == 2:
        vulnerability[i]['risk'] = "High"
    if vulnerability[i]['risk'] == 3:
        vulnerability[i]['risk'] = "Medium"
    if vulnerability[i]['risk'] == 4:
        vulnerability[i]['risk'] = "Low"

# ==========================================================================================================
contents={}
contents['contents_ip']=list_all_ip_port
contents['vulnerability']=vulnerability


doc.render(contents)
doc.save("generated_nessus.docx")
os.system("generated_nessus.docx")

