import csv
from importlib.resources import contents
import json
from turtle import home
from docxtpl import *
import pandas
import os

doc = DocxTemplate("D:/github/WebReport/krit/template.docx")


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


DataJson = open(
    "D:/github/WebReport/krit/dataFile.json", "w")
DataJson.close()

csvFilePath = r'D:/github/WebReport/krit/merge-Cloud-Flexpod.csv'
jsonFilePath = r'D:/github/WebReport/krit/dataFile.json'
makeJson(csvFilePath, jsonFilePath)


DataJSON = pandas.read_json(jsonFilePath)

Ip = [DataJSON[i]["Host"] for i in DataJSON]
Ip = list(dict.fromkeys(Ip))
# print(Ip)

list_ip = []
for i in Ip:
    ip_splite = (i.split('.'))
    ip_subclass = ip_splite[0]+'.'+ip_splite[1]+'.'+ip_splite[2]+".xxx"
    if ip_subclass not in list_ip:
        list_ip.append(ip_subclass)

list_ip = list(dict.fromkeys(list_ip))

Content_risk = {}
range_Ip = []
for i in Ip:
    Content_risk["host"] = i
    Content_risk["Critical"] = 0
    Content_risk["High"] = 0
    Content_risk["Medium"] = 0
    Content_risk["Low"] = 0
    Content_risk["Sum"] = 0
    range_Ip.append(Content_risk)
    Content_risk = {}


for i in DataJSON:
    if DataJSON[i]['Host'] != 'None':
        for j in range_Ip:
            if j['host'] == DataJSON[i]['Host']:
                if DataJSON[i]['Risk'] == 'Critical':
                    j['Critical'] += 1
                    j['Sum'] += 1
                elif DataJSON[i]['Risk'] == 'High':
                    j['High'] += 1
                    j['Sum'] += 1
                elif DataJSON[i]['Risk'] == 'Medium':
                    j['Medium'] += 1
                    j['Sum'] += 1
                elif DataJSON[i]['Risk'] == 'Low':
                    j['Low'] += 1
                    j['Sum'] += 1

class_ip = []
[]
for i in list_ip:
    Content_class = {}
    Content_class["class"] = i
    Content_class["total"] = {'Critical': 0,
                              'High': 0, 'Medium': 0, 'Low': 0, 'Sum': 0}
    list_ip_in_class = []
    for j in range_Ip:
        ip_splite2 = (j['host'].split('.'))
        ip_subclass2 = ip_splite2[0]+'.'+ip_splite2[1]+'.'+ip_splite2[2]+".xxx"
        if ip_subclass2 == i:
            list_ip_in_class.append(j)
            Content_class["total"]['Critical'] += j['Critical']
            Content_class["total"]['High'] += j['High']
            Content_class["total"]['Medium'] += j['Medium']
            Content_class["total"]['Low'] += j['Low']
            Content_class["total"]['Sum'] += j['Sum']
        # print(i,j)
    list_ip_in_class = sorted(list_ip_in_class, key=lambda d: (
        tuple(map(int, d['host'].split('.')))))
    index1 = 1
    # print(items)
    for x in list_ip_in_class:
        x['No'] = index1
        index1 += 1

    Content_class["risk"] = list_ip_in_class
    class_ip.append(Content_class)

Content3 = {}

Content3['table3'] = class_ip


doc.render(Content3)
doc.save("D:/github/WebReport/krit/generated_table3.docx")
os.system("D:/github/WebReport/krit/generated_table3.docx")
