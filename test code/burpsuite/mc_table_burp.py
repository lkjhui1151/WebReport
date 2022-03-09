from cProfile import label
import csv
from docxtpl import *
import os
from matplotlib import pyplot as plt
import numpy as np
import json
import pandas
import sys
import matplotlib.patches as mpatches

maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

doc = DocxTemplate("E:/INETMS/doc/Nessus_template/template_burp.docx")

countCri = 0
countHigh = 0
countMed = 0
countLow = 0
countInfo = 0
count = 1
context = {}
countIP = 0
genGraph = 1

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
    "E:/INETMS/doc/Nessus_template/dataFile.json", "w")
DataJson.close()

csvFilePath = r'E:/INETMS/doc/Nessus_template/Burp.csv'
jsonFilePath = r'E:/INETMS/doc/Nessus_template/dataFile.json'

makeJson(csvFilePath, jsonFilePath)

DataJSON = pandas.read_json(jsonFilePath)

GroupName1 = {}
GroupName2 = []

# Create New Data Source
for row in DataJSON:
    GroupName1["Risk"] = DataJSON[row]["severity"]
    GroupName1["ip"] = DataJSON[row]["host/_ip"]
    GroupName1["url"] = DataJSON[row]["host/__text"]
    GroupName1["Group"] = DataJSON[row]["host/__text"]
    GroupName1["path"] = DataJSON[row]["path"]
    GroupName1["location"] = DataJSON[row]["location"]
    GroupName1["issue"] = DataJSON[row]["issueBackground"]
    GroupName1["solution"] = DataJSON[row]["remediationBackground"]
    GroupName1["references"] = DataJSON[row]["references"]
    GroupName1["detail"] = DataJSON[row]["issueDetail"]
    GroupName2.append(GroupName1)
    GroupName1 = {}

# # Remove Data is duplicate
results = [dict(t) for t in {tuple(d.items()) for d in GroupName2}]
newlist = sorted(results, key=lambda d: d['Group'])
# print(newlist)

# # Mean for loop
# # seen = set()
# # new_l = []
# # for d in GroupName2:
# #     t = tuple(d.items())
# #     if t not in seen:
# #         seen.add(t)
# #         new_l.append(d)

for row in newlist:
    if row['Group'] not in context:
        context[row['Group']] = {"No":count,"Name": row['ip'], "url": row['url'], "Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Total": 0}
        count+=1

        
    if row['Group'] == "":
        context[row['Risk']]["Name"] = "etc"
        # Count amount of critaria in each group
    if row['Risk'] == "Critical":
        context[row['Group']]["Critical"] += 1
        context[row['Group']]["Total"] += 1
    if row['Risk'] == "High":
        context[row['Group']]["High"] += 1
        context[row['Group']]["Total"] += 1
    if row['Risk'] == "Medium":
        context[row['Group']]["Medium"] += 1
        context[row['Group']]["Total"] += 1
    if row['Risk'] == "Low":
        context[row['Group']]["Low"] += 1
        context[row['Group']]["Total"] += 1
      

# # print(context)

l = list(context.values())

totalS = (sum([d['Total'] for d in l]))
CriticalS = (sum([d['Critical'] for d in l]))
HighS = (sum([d['High'] for d in l]))
MediumS = (sum([d['Medium'] for d in l]))
LowS = (sum([d['Low'] for d in l]))
#InfoS = (sum([d['Info'] for d in l]))
Amount = CriticalS+HighS+MediumS+LowS
#Amount = 0
if Amount == 0:
    Amount = 1
    genGraph = 0
else:
    Amount
dictS = {"Critical": CriticalS,
         "High": HighS, "Medium": MediumS, "Low": LowS, "Total": totalS}
#+++++++++++++++++++++++++++++== FIX HERE +++++++++++++++++++++++++++++++++++++
percent = {"Critical": '%0.2f' % (CriticalS/Amount*100), "High": '%0.2f' % (
    HighS/Amount*100), "Medium": '%0.2f' % (MediumS/Amount*100), "Low": '%0.2f' % (LowS/Amount*100)}
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

l2 = {"table1": {"Group": l, "Summary": dictS, "Percent": percent}}

doc.render(l2)
#+++++++++++++++++++++++++++++== FIX HERE +++++++++++++++++++++++++++++++++++++
array = [
    {
        "risk": "Critical",
        "value": l2["table1"]["Summary"]["Critical"],
        "colors": "#7030A0",
        "labels": "Critical, " + str(l2["table1"]["Summary"]["Critical"]) + " (" + str(l2["table1"]["Percent"]["Critical"])+"%)"
    },
    {
        "risk": "High",
        "value": l2["table1"]["Summary"]["High"],
        "colors": "#FF0000",
        "labels": "High, " + str(l2["table1"]["Summary"]["High"]) + " (" + str(l2["table1"]["Percent"]["High"])+"%)"
    },
    {
        "risk": "Medium",
        "value": l2["table1"]["Summary"]["Medium"],
        "colors": "#FFC000",
        "labels": "Medium, " + str(l2["table1"]["Summary"]["Medium"]) + " (" + str(l2["table1"]["Percent"]["Medium"])+"%)"
    },
    {
        "risk": "Low",
        "value": l2["table1"]["Summary"]["Low"],
        "colors": "#FFFF00",
        "labels": "Low, " + str(l2["table1"]["Summary"]["Low"]) + " (" + str(l2["table1"]["Percent"]["Low"])+"%)"
    }
]
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# def make_autopct(values):
#     def my_autopct(pct):
#         total = sum(values)
#         val = int(round(pct*total/100.0))
#         if pct > 0: 
#             print(values)
#             return '{v:d} ({p:1.0f}%)'.format(p=pct,v=val) 
#         else:
#             return ''
#     return my_autopct

#+++++++++++++++++++++++++++++== FIX HERE +++++++++++++++++++++++++++++++++++++
fig, ax = plt.subplots()
Critical = mpatches.Patch(
    color="#7030A0", label='Critical')
High = mpatches.Patch(
    color="#FF0000", label='High')
Medium = mpatches.Patch(
    color="#FFC000", label='Medium')
Low = mpatches.Patch(
    color="#FFFF00", label='Low')
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if genGraph != 0:
#+++++++++++++++++++++++++++++== FIX HERE +++++++++++++++++++++++++++++++++++++    
    value = [i["value"] for i in array if i["value"]!=0] 
    plt.pie(value, labels=[i["labels"] for i in array if i["value"]!=0], colors=[i["colors"] for i in array if i["value"]!=0], pctdistance=1.2)
    plt.title('Summary Vulnerability by Severity', y=1.05, fontsize=15)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0),
                    fancybox=True, shadow=True, ncol=4, handles=[Critical, High, Medium, Low])
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    plt.savefig("E:/INETMS/doc/Nessus_template/Overview_Graph.png")

    doc.replace_media("E:/INETMS/doc/Nessus_template/1.png",
                    "E:/INETMS/doc/Nessus_template/Overview_Graph.png")
    

doc.save("E:/INETMS/doc/Nessus_template/generated_doc.docx")
os.system("E:/INETMS/doc/Nessus_template/generated_doc.docx")