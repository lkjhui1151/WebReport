import csv
import errno
from msilib.schema import Error
from unittest import result
from docxtpl import *
import os
from matplotlib import pyplot as plt
import numpy as np
import json
import pandas

doc = DocxTemplate("D:/github/WebReport/testCode/template.docx")

countCri = 0
countHigh = 0
countMed = 0
countLow = 0
countInfo = 0
count = 0
context = {}
countIP = 0


def makeJson(csvFilePath, jsonFilePath):
    data = {}
    try:
        with open(csvFilePath, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            key_id = 0
            for rows in csvReader:
                key = key_id
                data[key] = rows
                key_id += 1
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))
    except NameError as exception:
        print(exception)
    except:
        with open(csvFilePath, encoding='ISO-8859-1') as csvf:
            csvReader = csv.DictReader(csvf)
            key_id = 0
            for rows in csvReader:
                key = key_id
                data[key] = rows
                key_id += 1
        with open(jsonFilePath, 'w', encoding='ISO-8859-1') as jsonf:
            jsonf.write(json.dumps(data, indent=4))


DataJson = open(
    "D:/github/WebReport/testCode/dataFile.json", "w")
DataJson.close()

csvFilePath = r'D:/github/WebReport/testCode/Burp.csv'
jsonFilePath = r'D:/github/WebReport/testCode/dataFile.json'

makeJson(csvFilePath, jsonFilePath)

# DataJSON = pandas.read_json(jsonFilePath)

# GroupName1 = {}
# GroupName2 = []

# # Create New Data Source
# for row in DataJSON:
#     GroupName1["Risk"] = DataJSON[row]["Risk"]
#     GroupName1["Host"] = DataJSON[row]["Host"]
#     GroupName1["Name"] = DataJSON[row]["Name"]
#     GroupName2.append(GroupName1)
#     GroupName1 = {}

# # Remove Data is duplicate
# results = [dict(t) for t in {tuple(d.items()) for d in GroupName2}]
# newlist = sorted(results, key=lambda d: d['Host'].split("."))
# print(newlist)
