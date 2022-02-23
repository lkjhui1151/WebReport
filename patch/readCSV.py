from matplotlib import pyplot as plt
from docxtpl import *
import numpy as np
import pandas
import json
import csv
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
countCri = 0
countHigh = 0
countMed = 0
countLow = 0
countInfo = 0
count = 0
context = {}
countIP = 0

Ip = [DataJSON[i]["Host"] for i in DataJSON]
Ip = list(dict.fromkeys(Ip))

Name = [DataJSON[i]["Name"] for i in DataJSON if DataJSON[i]["Risk"] != "None"]
Name = list(dict.fromkeys(Name))

for row in DataJSON:
    if DataJSON[row]['Group'] not in context:
        context[DataJSON[row]['Group']] = {"Name": DataJSON[row]['Group'], "device": {
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
l2 = {"Group": l, "Summary": dictS, "Percent": percent}


array = [
    {
        "risk": "Critical",
        "value": l2["Summary"]["Critical"],
        "colors": "#C20909"
    },
    {
        "risk": "High",
        "value": l2["Summary"]["High"],
        "colors": "#F09D1A"
    },
    {
        "risk": "Medium",
        "value": l2["Summary"]["Medium"],
        "colors": "#FFD80C"
    },
    {
        "risk": "Low",
        "value": l2["Summary"]["Critical"],
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


list_ip = []
for i in Ip:
    ip_splite = (i.split('.'))
    ip_subclass = ip_splite[0]+'.'+ip_splite[1]+'.'+ip_splite[2]+'.'+'0'
    if ip_subclass not in list_ip:
        list_ip.append(ip_subclass)

list_ip = list(dict.fromkeys(list_ip))
list_ip = sorted(list_ip, key=lambda d: (tuple(map(int, d.split('.')))))


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

for i in list_ip:
    Content_class = {}
    Content_class["class"] = i
    Content_class["total"] = {'Critical': 0,
                              'High': 0, 'Medium': 0, 'Low': 0, 'Sum': 0}
    list_ip_in_class = []
    for j in range_Ip:
        ip_splite2 = (j['host'].split('.'))
        ip_subclass2 = ip_splite2[0]+'.' + \
            ip_splite2[1]+'.'+ip_splite2[2]+'.'+'0'
        if ip_subclass2 == i:
            list_ip_in_class.append(j)
            Content_class["total"]['Critical'] += j['Critical']
            Content_class["total"]['High'] += j['High']
            Content_class["total"]['Medium'] += j['Medium']
            Content_class["total"]['Low'] += j['Low']
            Content_class["total"]['Sum'] += j['Sum']

    list_ip_in_class = sorted(list_ip_in_class, key=lambda d: (
        tuple(map(int, d['host'].split('.')))))
    index1 = 1

    for x in list_ip_in_class:
        x['No'] = index1
        index1 += 1

    Content_class["risk"] = list_ip_in_class
    class_ip.append(Content_class)


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

Content["table1"] = l2
Content["table2"] = vulnerability
Content["table3"] = class_ip

# print(Content['table1']["Summary"])
doc.render(Content)
doc.save("D:/github/WebReport/patch/generated_doc.docx")
os.system("D:/github/WebReport/patch/generated_doc.docx")
