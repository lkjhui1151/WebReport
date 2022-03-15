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
import re


path="D:/INET-MS/Auto report/GitHub/WebReport/code_krit/burp/"
inputXML="Burp Scan file.xml"
inputCSV="Burp Scan file.CSV"

doc = DocxTemplate(path+"template_burp.docx")

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

csvFilePath = path+inputCSV
jsonFilePath = path+'data.json'
makeJson(csvFilePath, jsonFilePath)

DataJSON = pandas.read_json(jsonFilePath)

ip=[]
url=[]
host_id=[]

for i in DataJSON:
    ip.append(DataJSON[i]["host/_ip"]) 
    host_id.append(DataJSON[i]["type"])

ip=list(dict.fromkeys(ip))
ip = sorted(ip, key=lambda d: (tuple(map(int, d.split('.')))))
host_id=list(dict.fromkeys(host_id))


groupID = {}
vulnerability_url=[]
for i in DataJSON:
    if DataJSON[i]['severity'] != 'Information':
        if DataJSON[i]['type'] in groupID:
            groupID[DataJSON[i]['type']] += 1
        else:
            groupID[DataJSON[i]['type']] = 1

def cleanCode(x) : 
    x= re.sub('</?[a-z]*>',"",x)
    return (x)


for j in host_id:

    countCheck  = 0
    list_url    = []
    subContent  = {}
    for i in DataJSON:
        if DataJSON[i]['severity'] != 'Information':
            if DataJSON[i]['type'] == j:
                list_url.append(DataJSON[i]['host/__text']+DataJSON[i]["location"])

                countCheck += 1
                if countCheck == groupID[DataJSON[i]['type']]:
                    list_url=list(dict.fromkeys(list_url))
                    url = ""
                    for x in list_url:
                        if url == "":
                            url = x
                        else :
                            url = url + '\n' + x  

                    list_ref = re.findall(r'(http\S+)\"',DataJSON[i]['references'])
                    ref = ""
                    for temp in list_ref:
                        if ref == "":
                            ref = temp
                        else:
                            ref = ref + "\n" + temp

                    if len(DataJSON[i]['host/__text'].split(":")) == 3:
                        subContent["port"] = DataJSON[i]['host/__text'].split(":")[2].split('/')[0]
                    elif DataJSON[i]['host/__text'].split(":")[0] == "https" :
                        subContent["port"] = "443"
                    elif DataJSON[i]['host/__text'].split(":")[0] == "http" :
                        subContent["port"] = "80"
                    else:
                        subContent["port"] ="N/A"
                    subContent["host"] = url
                    subContent["name"] = DataJSON[i]['name']
                    subContent["description"] = cleanCode(DataJSON[i]['issueBackground'])
                    subContent["solution"] = cleanCode(DataJSON[i]['remediationBackground'])
                    # if DataJSON[i]['references']=="":
                    #     subContent["remark"] = " - "
                    # else:
                    subContent["remark"] = ref
                
                    if DataJSON[i]['severity'] == "Critical":
                        subContent["color"] = "#7030A0"
                        subContent["severity"] = 1
                    elif DataJSON[i]['severity'] == "High":
                        subContent["color"] = "#FF0000"
                        subContent["severity"] = 2
                    elif DataJSON[i]['severity'] == "Medium":
                        subContent["color"] = "#FFC000"
                        subContent["severity"] = 3
                    elif DataJSON[i]['severity'] == "Low":
                        subContent["color"] = "#FFFF00"
                        subContent["severity"] = 4
                    vulnerability_url.append(subContent)

def runIndex(e):
    return e['severity']
vulnerability_url.sort(key=runIndex, reverse=False)
for i in range(len(vulnerability_url)):
    vulnerability_url[i]['no'] = i+1 
    if vulnerability_url[i]['severity'] == 1:
        vulnerability_url[i]['severity'] = "Critical"
    if vulnerability_url[i]['severity'] == 2:
        vulnerability_url[i]['severity'] = "High"
    if vulnerability_url[i]['severity'] == 3:
        vulnerability_url[i]['severity'] = "Medium"
    if vulnerability_url[i]['severity'] == 4:
        vulnerability_url[i]['severity'] = "Low"
# print(vulnerability_url)
with open(path+'dataout.json', 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(vulnerability_url, indent=4))

# # ==========================================================================================================
contents={}
contents['vulnerability_url']=vulnerability_url


doc.render(contents)
doc.save(path+"generated_burp.docx")
# # os.system("generated_burp.docx")

