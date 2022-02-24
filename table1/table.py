import csv
from unittest import result
from docxtpl import *
import os
from matplotlib import pyplot as plt
import numpy as np
import json
import pandas

doc = DocxTemplate("D:/github/WebReport/max/template.docx")

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
    "D:/github/WebReport/max/dataFile.json", "w")
DataJson.close()

csvFilePath = r'D:/github/WebReport/max/merge-Cloud-Flexpod.csv'
jsonFilePath = r'D:/github/WebReport/max/dataFile.json'

makeJson(csvFilePath, jsonFilePath)

DataJSON = pandas.read_json(jsonFilePath)

for row in DataJSON:
    host = DataJSON[row]['Group'].split(".")
    # host = list(dict.fromkeys(host))
    host = host[0]+"."+host[1]+"."+host[2]+"."+"0"
    if DataJSON[row]['Group'] not in context:
        context[DataJSON[row]['Group']] = {"Name": host, "device": {
            DataJSON[row]['Host']}, "Total_IP": 0, "Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Info": 0}
    else:
        context[DataJSON[row]['Group']]["device"].add(DataJSON[row]['Host'])

        countIP = len(context[DataJSON[row]['Group']]["device"])
        context[DataJSON[row]['Group']]["Total_IP"] = countIP
    if DataJSON[row]['Group'] == "":
        context[DataJSON[row]['Risk']]["Name"] = "etc"
        # Count amount of critaria in each group
    if DataJSON[row]['Risk'] == "Critical":
        context[DataJSON[row]['Group']]["Critical"] += 1
    if DataJSON[row]['Risk'] == "High":
        context[DataJSON[row]['Group']]["High"] += 1
    if DataJSON[row]['Risk'] == "Medium":
        context[DataJSON[row]['Group']]["Medium"] += 1
    if DataJSON[row]['Risk'] == "Low":
        context[DataJSON[row]['Group']]["Low"] += 1
    if DataJSON[row]['Risk'] == "None":
        context[DataJSON[row]['Group']]["Info"] += 1

l = list(context.values())

totalS = (sum([d['Total_IP'] for d in l]))
CriticalS = (sum([d['Critical'] for d in l]))
HighS = (sum([d['High'] for d in l]))
MediumS = (sum([d['Medium'] for d in l]))
LowS = (sum([d['Low'] for d in l]))
InfoS = (sum([d['Info'] for d in l]))
Amount = CriticalS+HighS+MediumS+LowS
dictS = {"Total_IP": totalS, "Critical": CriticalS,
         "High": HighS, "Medium": MediumS, "Low": LowS, "Info": InfoS}
percent = {"Critical": '%1.0f' % (CriticalS*100/Amount), "High": '%1.0f' % (
    HighS*100/Amount), "Medium": '%1.0f' % (MediumS*100/Amount), "Low": '%1.0f' % (LowS*100/Amount)}
# Final JSON output
l = sorted(l, key=lambda d: (
    tuple(map(int, d['Name'].split('.')))))

groupList = {}

for i in l:
    if i["Name"] in groupList:
        groupList[i["Name"]] += 1
    else:
        groupList[i["Name"]] = 1
key_list = list(groupList.keys())
# print(key_list)
GroupNew = {"Total_IP": 0, "Critical": 0,
            "High": 0, "Medium": 0, "Low": 0, "Info": 0}
totalIP = 0
count = 0
countCH = 0

resultALL = []
ListIP = []
ListIP = []
for i in l:
    if i["Name"] == key_list[count]:
        GroupNew["Total_IP"] += int(i["Total_IP"])
        GroupNew["Critical"] += int(i["Critical"])
        GroupNew["High"] += int(i["High"])
        GroupNew["Medium"] += int(i["Medium"])
        GroupNew["Low"] += int(i["Low"])
        GroupNew["Info"] += int(i["Info"])
        ListIP.append(i["device"])
        countCH += 1
        if countCH >= groupList[i["Name"]]:
            GroupNew["Name"] = i["Name"]
            GroupNew["Device"] = ListIP
            resultALL.append(GroupNew)
            ListIP = []
            GroupNew = {"Total_IP": 0, "Critical": 0,
                        "High": 0, "Medium": 0, "Low": 0, "Info": 0}
            countCH = 0
            count += 1
count = 0

l2 = {"table1": {"Group": resultALL, "Summary": dictS, "Percent": percent}}

doc.render(l2)

array = [
    {
        "risk": "Critical",
        "value": l2["table1"]["Summary"]["Critical"],
        "colors": "#C20909"
    },
    {
        "risk": "High",
        "value": l2["table1"]["Summary"]["High"],
        "colors": "#F09D1A"
    },
    {
        "risk": "Medium",
        "value": l2["table1"]["Summary"]["Medium"],
        "colors": "#FFD80C"
    },
    {
        "risk": "Low",
        "value": l2["table1"]["Summary"]["Critical"],
        "colors": "#23B800"
    }
]


plt.pie([i["value"] for i in array], autopct=lambda p: '{:1.0f}%'.format(
    round(p)) if p > 0 else '', colors=[i["colors"] for i in array])
plt.title('Vulnerability Overview of The System', y=1.05, fontsize=15)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0),
               fancybox=True, shadow=True, ncol=4, labels=[i["risk"] for i in array])

plt.savefig("D:/github/WebReport/max/Overview_Graph.png")

doc.replace_media("D:/github/WebReport/max/1.png",
                  "D:/github/WebReport/max/Overview_Graph.png")

doc.save("D:/github/WebReport/max/generated_doc.docx")
os.system("D:/github/WebReport/max/generated_doc.docx")
