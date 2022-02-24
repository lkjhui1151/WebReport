from matplotlib import pyplot as plt
from docxtpl import *
import numpy as np
import pandas
import json
import csv
import os
import datetime

today = datetime.date.today()
yearBE = today.year + 543

doc = DocxTemplate("D:/github/WebReport/backend/api/sources/template.docx")


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
    "D:/github/WebReport/backend/api/sources/dataFile.json", "w")
DataJson.close()

csvFilePath = r'D:/github/WebReport/backend/api/sources/All Dell cloud.csv'
jsonFilePath = r'D:/github/WebReport/backend/api/sources/dataFile.json'

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
GroupName1 = {}
GroupName2 = []

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

# ******************************************* Krit *******************************
Ip = []
Group = []
for i in DataJSON:
    Ip.append(DataJSON[i]["Host"])
    Group.append(DataJSON[i]["Group"])

Ip = list(dict.fromkeys(Ip))
Ip = sorted(Ip, key=lambda d: (tuple(map(int, d.split('.')))))
Group = list(dict.fromkeys(Group))

list_range_ip = []
for i in Ip:
    ip_splite = (i.split('.'))
    ip_subclass = ip_splite[0]+'.'+ip_splite[1]+'.'+ip_splite[2]+'.'+'0'
    if ip_subclass not in list_range_ip:
        list_range_ip.append(ip_subclass)

list_range_ip = list(dict.fromkeys(list_range_ip))


Content_risk = {}
range_Ip = []
for i in Ip:
    ip_splite = (i.split('.'))
    ip_subclass = ip_splite[0]+'.'+ip_splite[1]+'.'+ip_splite[2]+'.'+'0'
    Content_risk["class"] = ip_subclass
    Content_risk["host"] = i
    Content_risk["Critical"] = 0
    Content_risk["High"] = 0
    Content_risk["Medium"] = 0
    Content_risk["Low"] = 0
    Content_risk["Sum"] = 0
    range_Ip.append(Content_risk)
    Content_risk = {}

dict_group_ip = {}

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

for x in Group:
    list_group_ip = []
    for i in DataJSON:
        if DataJSON[i]['Group'] == x:
            list_group_ip.append(DataJSON[i]['Host'])
            list_group_ip = list(dict.fromkeys(list_group_ip))
            dict_group_ip[x] = list_group_ip


class_ip = []
for group_key, group_value_listIP in dict_group_ip.items():
    Content_group = {}
    Content_group["group"] = group_key
    list_class = []
    for class_ in list_range_ip:
        Content_class = {}
        Content_class['class'] = class_
        Content_class['total'] = {'Critical': 0,
                                  'High': 0, 'Medium': 0, 'Low': 0, 'Sum': 0}
        list_range_ip_in_class = []
        for ip in range_Ip:
            if ip['host'] in group_value_listIP:
                if ip['class'] == class_:
                    list_range_ip_in_class.append(ip)
                    Content_class['total']['Critical'] += ip['Critical']
                    Content_class['total']['High'] += ip['High']
                    Content_class['total']['Medium'] += ip['Medium']
                    Content_class['total']['Low'] += ip['Low']
                    Content_class['total']['Sum'] += ip['Sum']

        index1 = 1
        for x in list_range_ip_in_class:
            x['No'] = index1
            index1 += 1
        Content_class['risk'] = list_range_ip_in_class

        if list_range_ip_in_class:
            list_class.append(Content_class)
            Content_group["mega_class"] = list_class

    class_ip.append(Content_group)

# ***************************************** MAC *********************************
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

groupList = {}

for i in l:
    if i["Name"] in groupList:
        groupList[i["Name"]] += 1
    else:
        groupList[i["Name"]] = 1

key_list = list(groupList.keys())

GroupNew = {"Total_IP": 0, "Critical": 0,
            "High": 0, "Medium": 0, "Low": 0, "Info": 0}
totalIP = 0
count = 0
countCH = 0

resultALL = []
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

# print(resultALL)
l2 = {"Group": resultALL, "Summary": dictS, "Percent": percent}


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

################################################################################################


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

plt.savefig("D:/github/WebReport/backend/api/sources/Overview_Graph.png")

doc.replace_media("D:/github/WebReport/backend/api/sources/1.png",
                  "D:/github/WebReport/backend/api/sources/Overview_Graph.png")

Content["table1"] = l2
Content["table2"] = vulnerability
Content["table3"] = class_ip
Content["year"] = yearBE
Content["date"] = yearBE

doc.render(Content)
doc.save("D:/github/WebReport/backend/api/sources/generated_doc.docx")
os.system("D:/github/WebReport/backend/api/sources/generated_doc.docx")