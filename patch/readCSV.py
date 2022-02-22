import csv
import json
from docxtpl import *
import pandas
import os

doc = DocxTemplate("D:/github/WebReport/table2.docx")


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

csvFilePath = r'D:/github/WebReport/patch/A2.csv'
jsonFilePath = r'D:/github/WebReport/patch/dataFile.json'

makeJson(csvFilePath, jsonFilePath)

DataJSON = pandas.read_json(jsonFilePath)

subContent = {}
Content = {}
GroupName = {}

vulnerability = []

countCheck = 0
id = 1
address = ""

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
                    subContent["id"] = id
                    subContent["address"] = address
                    subContent["name"] = DataJSON[i]['Name'] + \
                        "\n" + "\n" + "- " + DataJSON[i]['Description']
                    subContent["risk"] = DataJSON[i]['Risk']
                    subContent["remask"] = DataJSON[i]['Solution']
                    if DataJSON[i]['Risk'] == "Critical":
                        subContent["color"] = "#C20909"
                    if DataJSON[i]['Risk'] == "High":
                        subContent["color"] = "#F09D1A"
                    if DataJSON[i]['Risk'] == "Medium":
                        subContent["color"] = "#FFD80C"
                    if DataJSON[i]['Risk'] == "Low":
                        subContent["color"] = "#23B800"
                    vulnerability.append(subContent)
                    subContent = {}
                    countCheck = 0
                    address = ""
                    id += 1

Content["vulnerability"] = vulnerability
# print(Content)
doc.render(Content)
doc.save("generated_doc.docx")
os.system("generated_doc.docx")
