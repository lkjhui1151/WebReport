import csv
from unittest import result
from docxtpl import *
import os
from matplotlib import pyplot as plt
import numpy as np
import json
import pandas

doc = DocxTemplate("D:/github/WebReport/table1/template.docx")

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
    "D:/github/WebReport/table1/dataFile.json", "w")
DataJson.close()

csvFilePath = r'D:/github/WebReport/table1/All Dell cloud.csv'
jsonFilePath = r'D:/github/WebReport/table1/dataFile.json'

makeJson(csvFilePath, jsonFilePath)

DataJSON = pandas.read_json(jsonFilePath)

GroupName1 = {}
GroupName2 = []

# Create New Data Source
for row in DataJSON:
    GroupName1["Risk"] = DataJSON[row]["Risk"]
    GroupName1["Host"] = DataJSON[row]["Host"]
    GroupName1["Name"] = DataJSON[row]["Name"]
    GroupName1["Group"] = DataJSON[row]["Group"]
    GroupName2.append(GroupName1)
    GroupName1 = {}

# Remove Data is duplicate
results = [dict(t) for t in {tuple(d.items()) for d in GroupName2}]

# Mean for loop
# seen = set()
# new_l = []
# for d in GroupName2:
#     t = tuple(d.items())
#     if t not in seen:
#         seen.add(t)
#         new_l.append(d)

for row in results:
    if row['Group'] not in context:
        context[row['Group']] = {"Name": row['Group'], "device": {
            row['Host']}, "Total_IP": 0, "Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Info": 0}
    else:
        context[row['Group']]["device"].add(row['Host'])

        countIP = len(context[row['Group']]["device"])
        context[row['Group']]["Total_IP"] = countIP
    if row['Group'] == "":
        context[row['Risk']]["Name"] = "etc"
        # Count amount of critaria in each group
    if row['Risk'] == "Critical":
        context[row['Group']]["Critical"] += 1
    if row['Risk'] == "High":
        context[row['Group']]["High"] += 1
    if row['Risk'] == "Medium":
        context[row['Group']]["Medium"] += 1
    if row['Risk'] == "Low":
        context[row['Group']]["Low"] += 1
    if row['Risk'] == "None":
        context[row['Group']]["Info"] += 1

# print(context)

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
# l = sorted(l, key=lambda d: (
#     tuple(map(int, d['Name'].split('.')))))

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

plt.savefig("D:/github/WebReport/table1/Overview_Graph.png")

doc.replace_media("D:/github/WebReport/table1/1.png",
                  "D:/github/WebReport/table1/Overview_Graph.png")

doc.save("D:/github/WebReport/table1/generated_doc.docx")
os.system("D:/github/WebReport/table1/generated_doc.docx")
