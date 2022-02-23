import csv
import json
from docxtpl import *
import pandas
import os

doc = DocxTemplate("D:/github/WebReport/patch/template.docx")


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
    "D:/github/WebReport/patch/dataFile.json", "w")
DataJson.close()

csvFilePath = r'D:/github/WebReport/patch/merge-Cloud-Flexpod.csv'
jsonFilePath = r'D:/github/WebReport/patch/dataFile.json'

makeJson(csvFilePath, jsonFilePath)

DataJSON = pandas.read_json(jsonFilePath)

subContent = {}
Content = {}
GroupName = {}

vulnerability = []

countCheck = 0
address = ""
addrs = ""

Name = [DataJSON[i]["Name"] for i in DataJSON if DataJSON[i]["Risk"] != "None"]
Name = list(dict.fromkeys(Name))

for i in DataJSON:
    if DataJSON[i]['Risk'] != 'None':
        if DataJSON[i]['Name'] in GroupName:
            GroupName[DataJSON[i]['Name']] += 1
        else:
            GroupName[DataJSON[i]['Name']] = 1

for j in Name:
    for i in DataJSON:
        if DataJSON[i]['Risk'] != "None":
            if DataJSON[i]['Name'] == j:
                if address == "":
                    address = DataJSON[i]['Host']
                else:
                    address = address + "\n" + DataJSON[i]['Host']
                countCheck += 1
                if countCheck == GroupName[DataJSON[i]['Name']]:
                    address = address.split('\n')
                    address = sorted(address, key=lambda d: (
                        tuple(map(int, d.split('.')))))
                    address = list(dict.fromkeys(address))
                    for addr in address:
                        if addrs == "":
                            addrs = addr
                        else:
                            addrs = addrs + "\n" + addr
                    subContent["address"] = addrs
                    subContent["name"] = DataJSON[i]['Name'] + \
                        "\n" + "\n" + "- " + DataJSON[i]['Description']
                    subContent["remask"] = DataJSON[i]['Solution']
                    if DataJSON[i]['Risk'] == "Critical":
                        subContent["color"] = "#C20909"
                        subContent["risk"] = 4
                    if DataJSON[i]['Risk'] == "High":
                        subContent["color"] = "#F09D1A"
                        subContent["risk"] = 3
                    if DataJSON[i]['Risk'] == "Medium":
                        subContent["color"] = "#FFD80C"
                        subContent["risk"] = 2
                    if DataJSON[i]['Risk'] == "Low":
                        subContent["color"] = "#23B800"
                        subContent["risk"] = 1
                    vulnerability.append(subContent)
                    subContent = {}
                    countCheck = 0
                    address = ""
                    addrs = ""


def myFunc(e):
    return e['risk']


vulnerability.sort(key=myFunc, reverse=True)

for i in range(len(vulnerability)):
    if vulnerability[i]['risk'] == 4:
        vulnerability[i]['risk'] = "Critical"
    if vulnerability[i]['risk'] == 3:
        vulnerability[i]['risk'] = "High"
    if vulnerability[i]['risk'] == 2:
        vulnerability[i]['risk'] = "Medium"
    if vulnerability[i]['risk'] == 1:
        vulnerability[i]['risk'] = "Low"

Content["table2"] = vulnerability
# print(Content)
# doc.replace_media("D:/github/WebReport/patch/1.png",
#                   "D:/github/WebReport/patch/2.jpg")
doc.render(Content)
doc.save("D:/github/WebReport/patch/generated_doc.docx")
os.system("D:/github/WebReport/patch/generated_doc.docx")
