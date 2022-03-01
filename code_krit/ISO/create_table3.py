import csv
from importlib.resources import contents
import json
from tokenize import group
from turtle import home
from docxtpl import *
import pandas
import os

doc = DocxTemplate("./table3.docx")

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
    "./table3.json", "w")
DataJson.close()

csvFilePath = r'./All Dell cloud.csv'
jsonFilePath = r'./table3.json'
makeJson(csvFilePath, jsonFilePath)


DataJSON = pandas.read_json(jsonFilePath)
GroupName1 = {}
GroupName2 = {}
for row in DataJSON:
    GroupName1["Risk"] = DataJSON[row]["Risk"]
    GroupName1["Host"] = DataJSON[row]["Host"]
    GroupName1["Name"] = DataJSON[row]["Name"]
    GroupName1["Group"] = DataJSON[row]["Group"]
    GroupName2.append(GroupName1)
    GroupName1 = {}

# Remove Data is duplicate
results = [dict(t) for t in {tuple(d.items()) for d in GroupName2}]




Ip=[]
Group=[]
for i in DataJSON:
    Ip.append(DataJSON[i]["Host"])
    Group.append(DataJSON[i]["Group"])

Ip = list(dict.fromkeys(Ip))
Ip = sorted(Ip, key=lambda d: (tuple(map(int, d.split('.')))))
Group =list(dict.fromkeys(Group))

list_range_ip = []
for i in Ip:
    ip_splite = (i.split('.'))
    ip_subclass = ip_splite[0]+'.'+ip_splite[1]+'.'+ip_splite[2]+'.'+'0'
    if ip_subclass not in list_range_ip:
        list_range_ip.append(ip_subclass)

list_range_ip = list(dict.fromkeys(list_range_ip))
# list_range_ip = sorted(list_range_ip, key=lambda d: (tuple(map(int, d.split('.')))))
# print(list_range_ip)

Content_risk = {}
range_Ip=[]
for i in Ip:
    ip_splite = (i.split('.'))
    ip_subclass = ip_splite[0]+'.'+ip_splite[1]+'.'+ip_splite[2]+'.'+'0'
    Content_risk["class"] = ip_subclass
    Content_risk["host"] = i
    Content_risk["Critical"]=0
    Content_risk["High"]=0
    Content_risk["Medium"]=0
    Content_risk["Low"]=0
    Content_risk["Sum"]=0
    range_Ip.append(Content_risk)
    Content_risk={} 

dict_group_ip = {}


for  i in DataJSON:
    if DataJSON[i]['Host'] != 'None':
        for j in range_Ip:
            if  j['host']== DataJSON[i]['Host']:
                if DataJSON[i]['Risk'] == 'Critical':
                    j['Critical']+=1
                    j['Sum']+=1 
                elif DataJSON[i]['Risk'] == 'High':
                    j['High']+=1
                    j['Sum']+=1 
                elif DataJSON[i]['Risk'] == 'Medium':
                    j['Medium']+=1
                    j['Sum']+=1 
                elif DataJSON[i]['Risk'] == 'Low':
                    j['Low']+=1
                    j['Sum']+=1 
for x in Group:
    list_group_ip = []
    for  i in DataJSON:
        if DataJSON[i]['Group'] == x:
            list_group_ip.append(DataJSON[i]['Host'])
            list_group_ip = list(dict.fromkeys(list_group_ip))
            dict_group_ip[x] = list_group_ip
print(range_Ip)
# print(list_range_ip)


class_ip=[]
for group_key,group_value_listIP in dict_group_ip.items():
    Content_group = {}
    Content_group["group"] = group_key
    list_class= []
    for class_ in list_range_ip:
        Content_class= {}
        Content_class['class'] = class_
        Content_class['total'] = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Sum': 0}
        list_range_ip_in_class = []
        for ip in range_Ip:
            if ip['host'] in group_value_listIP:
                if ip['class'] == class_:
                    # print(class_,ip)
                    list_range_ip_in_class.append(ip)
                    Content_class['total']['Critical']+=ip['Critical']
                    Content_class['total']['High']+=ip['High']
                    Content_class['total']['Medium']+=ip['Medium']
                    Content_class['total']['Low']+=ip['Low']
                    Content_class['total']['Sum']+=ip['Sum']
#                 # print(list_range_ip_in_class,"\n")
        
#         list_range_ip_in_class = sorted(list_range_ip_in_class, key=lambda d: (tuple(map(int, d['host'].split('.')))))
        index1 = 1 
        for x in list_range_ip_in_class:
            x['No']= index1
            index1+=1
        Content_class['risk'] = list_range_ip_in_class
        
        if list_range_ip_in_class:
            list_class.append(Content_class)
            Content_group["mega_class"]=list_class
    
    class_ip.append(Content_group)
Content3 = {}
Content3['vulnerability'] = class_ip
# 
# print(Content3)

doc.render(Content3)
doc.save("generated_table3.docx")
os.system("generated_table3.docx")

