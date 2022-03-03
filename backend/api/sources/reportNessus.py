import csv
from docxtpl import *
import os
from matplotlib import pyplot as plt
import numpy as np
import json
import pandas
from collections import OrderedDict

import datetime

doc = DocxTemplate("backend/api/sources/templates/templateNessus.docx")

countCri = 0
countHigh = 0
countMed = 0
countLow = 0
countInfo = 0
count = 1
context = {}
countIP = 0


date = datetime.datetime.now()

dateNow = date.strftime("%B")+" " + \
    date.strftime("%d")+" "+date.strftime("%Y")


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
    "backend/api/sources/dataFile.json", "w")
DataJson.close()

csvFilePath = r'backend/api/sources/iso/USUI.csv'
jsonFilePath = r'backend/api/sources/dataFile.json'

makeJson(csvFilePath, jsonFilePath)

DataJSON = pandas.read_json(jsonFilePath)

GroupName1 = {}
GroupName2 = []

# Create New Data Source
for row in DataJSON:
    GroupName1["Risk"] = DataJSON[row]["Risk"]
    GroupName1["Host"] = DataJSON[row]["Host"]
    GroupName1["Name"] = DataJSON[row]["Name"]
    GroupName1["Group"] = DataJSON[row]["Host"]
    GroupName1["Protocol"] = DataJSON[row]["Protocol"]
    GroupName1["Port"] = DataJSON[row]["Port"]
    GroupName2.append(GroupName1)
    GroupName1 = {}

# Remove Data is duplicate
results = [dict(t) for t in {tuple(d.items()) for d in GroupName2}]
newlist = sorted(results, key=lambda d: (
    tuple(map(int, d['Group'].split('.')))))
# print(newlist)

for row in newlist:
    if row['Group'] not in context:
        context[row['Group']] = {"No": count, "Name": row['Group'], "device": {
            row['Host']}, "Total_IP": 0, "Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Total": 0}
        count += 1
    else:
        context[row['Group']]["device"].add(row['Host'])

        countIP = len(context[row['Group']]["device"])
        context[row['Group']]["Total_IP"] = countIP
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

l = list(context.values())

totalS = (sum([d['Total'] for d in l]))
CriticalS = (sum([d['Critical'] for d in l]))
HighS = (sum([d['High'] for d in l]))
MediumS = (sum([d['Medium'] for d in l]))
LowS = (sum([d['Low'] for d in l]))
#InfoS = (sum([d['Info'] for d in l]))
Amount = CriticalS+HighS+MediumS+LowS
dictS = {"Critical": CriticalS,
         "High": HighS, "Medium": MediumS, "Low": LowS, "Total": totalS}

Amount = 1 if Amount == 0 else Amount

percent = {"Critical": '%1.0f' % (CriticalS*100/Amount), "High": '%1.0f' % (
    HighS*100/Amount), "Medium": '%1.0f' % (MediumS*100/Amount), "Low": '%1.0f' % (LowS*100/Amount)}

l2 = {"table1": {"Group": l, "Summary": dictS, "Percent": percent}}


array = [
    {
        "risk": "Critical",
        "value": l2["table1"]["Summary"]["Critical"],
        "colors": "#7030a0"
    },
    {
        "risk": "High",
        "value": l2["table1"]["Summary"]["High"],
        "colors": "#C20909"
    },
    {
        "risk": "Medium",
        "value": l2["table1"]["Summary"]["Medium"],
        "colors": "#F09D1A"
    },
    {
        "risk": "Low",
        "value": l2["table1"]["Summary"]["Low"],
        "colors": "#FFD80C"
    }
]


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        if pct > 0:
            return '{v:d} ({p:1.0f}%)'.format(p=pct, v=val)
        else:
            return ''
    return my_autopct


value = [i["value"] for i in array]

try:
    plt.pie(value, autopct=make_autopct(value),
            colors=[i["colors"] for i in array])
    plt.title('Vulnerability by Severity', y=1.05, fontsize=15)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0),
               fancybox=True, shadow=True, ncol=4, labels=[i["risk"] for i in array])

    plt.savefig("backend/api/sources/image/Overview_Graph.png")

    doc.replace_media("backend/api/sources/image/2.png",
                      "backend/api/sources/image/Overview_Graph.png")
except NameError as err:
    print()
except:
    doc.replace_media("backend/api/sources/image/2.png",
                      "backend/api/sources/image/noGraph.jpg")


################################################## krit ##################################################


ip = [DataJSON[i]["Host"] for i in DataJSON]
ip = list(dict.fromkeys(ip))
ip = sorted(ip, key=lambda d: (tuple(map(int, d.split('.')))))
# --------------------------------------make data ip port------------------------------------------------------------
dict_ip_portopen = {}
for i in ip:
    dict_ip_portopen[i] = {'TCP': [], 'UDP': []}

for i in DataJSON:
    if DataJSON[i]["Protocol"] == 'tcp':
        dict_ip_portopen[DataJSON[i]["Host"]
                         ]['TCP'].append(DataJSON[i]["Port"])
    elif DataJSON[i]["Protocol"] == 'udp':
        dict_ip_portopen[DataJSON[i]["Host"]
                         ]['UDP'].append(DataJSON[i]["Port"])

for key, value in dict_ip_portopen.items():
    temp = ""
    for i in value:
        value[i] = list(dict.fromkeys(value[i]))
        value[i] = sorted(value[i], key=lambda d: (
            tuple(map(int, d.split('.')))))
        if '0' in value[i]:
            value[i].remove('0')

        for index in range(len(value[i])):
            if index == 0:
                if i == 'UDP':
                    if temp != "":
                        temp = temp+'\n'+i+' : '+value[i][index]
                    else:
                        temp = i+' : '+value[i][index]
                else:
                    temp = i+' : '+value[i][index]
            else:
                temp = temp+', '+value[i][index]
    dict_ip_portopen[key]['port'] = temp
list_all_ip_port = []
index = 1
for key, value in dict_ip_portopen.items():
    ip_port_ = {}
    ip_port_['No'] = index
    ip_port_['host'] = key
    ip_port_['port'] = value['port']
    list_all_ip_port.append(ip_port_)
    index += 1
# -----------------------------------------------------------------------------------------------------------------------------
# ==============================================-make data detail==============================================================
name = [DataJSON[i]["Plugin ID"]
        for i in DataJSON if DataJSON[i]["Risk"] != "None"]
name = list(dict.fromkeys(name))
dict_port_ip = {}
vulnerability = []
subContent = {}
countCheck = 0
GroupName = {}

for i in DataJSON:
    if DataJSON[i]['Risk'] != 'None':
        if DataJSON[i]['Plugin ID'] in GroupName:
            GroupName[DataJSON[i]['Plugin ID']] += 1
        else:
            GroupName[DataJSON[i]['Plugin ID']] = 1

for j in name:
    dict_port_ip = {}
    port_udp = []
    port_tcp = []
    for i in DataJSON:

        if DataJSON[i]['Risk'] != "None":
            if DataJSON[i]['Plugin ID'] == j:

                if DataJSON[i]['Protocol'] == 'tcp':
                    port_tcp.append(DataJSON[i]['Port'])
                elif DataJSON[i]['Protocol'] == 'udp':
                    port_udp.append(DataJSON[i]['Port'])

                if DataJSON[i]['Host'] in dict_port_ip:
                    dict_port_ip[DataJSON[i]['Host']].append(
                        DataJSON[i]['Port'])
                else:
                    dict_port_ip[DataJSON[i]['Host']] = [DataJSON[i]['Port']]
                countCheck += 1
                if countCheck == GroupName[DataJSON[i]['Plugin ID']]:

                    port_tcp = list(dict.fromkeys(port_tcp))
                    port_tcp = sorted(port_tcp, key=lambda x: int(x))
                    port_udp = list(dict.fromkeys(port_udp))
                    port_udp = sorted(port_udp, key=lambda x: int(x))

                    port = ""
                    for index in range(len(port_tcp)):
                        if index == 0:
                            port = 'TCP: '+port_tcp[index]
                        else:
                            port = port + ', ' + port_tcp[index]
                    for index in range(len(port_udp)):
                        if index == 0:
                            if port == "":
                                port = 'UDP: '+port_udp[index]
                            else:
                                port = port + '\n UDP: '+port_udp[index]
                        else:
                            port = port + ', ' + port_udp[index]

                    ip = ""
                    list_ip = sorted(dict_port_ip, key=lambda d: (
                        tuple(map(int, d.split('.')))))
                    dict_port_ip = dict(OrderedDict(
                        [(a, dict_port_ip[a])for a in list_ip]))

                    for key, value in dict_port_ip.items():
                        value = list(dict.fromkeys(value))
                        value = sorted(value, key=lambda d: int(d))
                        if ip == "":
                            pass
                        else:
                            ip = ip + ', '
                        ip = ip + key + '('
                        for index in range(len(value)):
                            if index == 0:
                                ip = ip + value[index]
                            else:
                                ip = ip + ', ' + value[index]
                        ip = ip + ')'
                    subContent["host"] = ip
                    subContent["port"] = port
                    subContent["name"] = DataJSON[i]['Name']
                    subContent["description"] = DataJSON[i]['Description']
                    subContent["solution"] = DataJSON[i]['Solution']
                    if DataJSON[i]['See Also'] == "":
                        subContent["remark"] = " - "
                    else:
                        subContent["remark"] = DataJSON[i]['See Also']

                    if DataJSON[i]['Risk'] == "Critical":
                        subContent["color"] = "#7030A0"
                        subContent["risk"] = 1
                    elif DataJSON[i]['Risk'] == "High":
                        subContent["color"] = "#FF0000"
                        subContent["risk"] = 2
                    elif DataJSON[i]['Risk'] == "Medium":
                        subContent["color"] = "#FFC000"
                        subContent["risk"] = 3
                    elif DataJSON[i]['Risk'] == "Low":
                        subContent["color"] = "#FFFF00"
                        subContent["risk"] = 4
                    vulnerability.append(subContent)
                    subContent = {}
                    countCheck = 0


def runIndex(e):
    return e['risk']


vulnerability.sort(key=runIndex, reverse=False)
for i in range(len(vulnerability)):
    vulnerability[i]['no'] = i+1
    if vulnerability[i]['risk'] == 1:
        vulnerability[i]['risk'] = "Critical"
    if vulnerability[i]['risk'] == 2:
        vulnerability[i]['risk'] = "High"
    if vulnerability[i]['risk'] == 3:
        vulnerability[i]['risk'] = "Medium"
    if vulnerability[i]['risk'] == 4:
        vulnerability[i]['risk'] = "Low"

# ==========================================================================================================
contents = {}

name = csvFilePath.split("/")
name = name[-1].split(".csv")

contents['contents_ip'] = list_all_ip_port
contents['vulnerability'] = vulnerability
contents['table1'] = l2
contents["fileName"] = name[0]
contents['Date'] = dateNow

doc.render(contents)

doc.save("backend/api/sources/results/"+name[0]+" Nessus"+".docx")
# os.system("backend/api/sources/results/generated_doc.docx")
