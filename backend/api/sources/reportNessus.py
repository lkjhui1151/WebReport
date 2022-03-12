import csv
from docxtpl import *
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import json
import pandas
from collections import OrderedDict
import re

import datetime
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

doc = DocxTemplate("backend/api/sources/templates/templateNessus.docx")

countCri = 0
countHigh = 0
countMed = 0
countLow = 0
countInfo = 0
count = 1
context = {}
context2 = {}
countIP = 0
genGraph = 1


date = datetime.datetime.now()

dateNow = date.strftime("%B")+" " + \
    date.strftime("%d")+" "+date.strftime("%Y")


def makeJson(csvFilePath, csvFilePath2, jsonFilePath, jsonFilePath2):
    data = {}
    data2 = {}
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

        with open(csvFilePath2, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            key_id = 0
            for rows in csvReader:
                key = key_id
                data2[key] = rows
                key_id += 1
        with open(jsonFilePath2, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data2, indent=4))
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

        with open(csvFilePath2, encoding='ISO-8859-1') as csvf:
            csvReader = csv.DictReader(csvf)
            key_id = 0
            for rows in csvReader:
                key = key_id
                data2[key] = rows
                key_id += 1
        with open(jsonFilePath2, 'w', encoding='ISO-8859-1') as jsonf:
            jsonf.write(json.dumps(data2, indent=4))


csvFilePath = r'backend/api/sources/iso/Network Cloud.csv'
jsonFilePath = r'backend/api/sources/dataNessus.json'

# <--Burp-->
csvFilePath2 = r'backend/api/sources/iso/burpresult3.csv'
jsonFilePath2 = r'backend/api/sources/dataBurp.json'

makeJson(csvFilePath, csvFilePath2, jsonFilePath, jsonFilePath2)

DataJSON = pandas.read_json(jsonFilePath)
DataBurp = pandas.read_json(jsonFilePath2)

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
# InfoS = (sum([d['Info'] for d in l]))
Amount = CriticalS+HighS+MediumS+LowS
dictS = {"Critical": CriticalS,
         "High": HighS, "Medium": MediumS, "Low": LowS, "Total": totalS}

if Amount == 0:
    Amount = 1
    genGraph = 0
else:
    Amount

percent = {"Critical": '%0.2f' % (CriticalS/Amount*100), "High": '%0.2f' % (
    HighS/Amount*100), "Medium": '%0.2f' % (MediumS/Amount*100), "Low": '%0.2f' % (LowS/Amount*100)}

l2 = {"table1": {"Group": l, "Summary": dictS, "Percent": percent}}


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

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
Critical = mpatches.Patch(
    color="#7030A0", label='Critical')
High = mpatches.Patch(
    color="#FF0000", label='High')
Medium = mpatches.Patch(
    color="#FFC000", label='Medium')
Low = mpatches.Patch(
    color="#FFFF00", label='Low')


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

if genGraph != 0:
    value = [i["value"] for i in array if i["value"] != 0]
    if value[2] == value[3]:
        a, b = value[1], value[0]
        value[b], value[a] = value[a], value[b]
    ax1.pie(value, labels=[i["labels"] for i in array if i["value"] != 0], colors=[
        i["colors"] for i in array if i["value"] != 0], pctdistance=1.2)
    ax1.set_title('Summary Vulnerability by Severity', y=1.05, fontsize=15)
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 0),
               fancybox=True, shadow=True, ncol=4, handles=[Critical, High, Medium, Low])
    # plt.show()
    fig1.savefig("backend/api/sources/image/Overview_Graph.png")
    doc.replace_media("backend/api/sources/image/2.png",
                      "backend/api/sources/image/Overview_Graph.png")
else:
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

# ======================================  krit Burp ====================================================================
countGroupID = {}
vulnerability_url = []

for i in DataBurp:
    if DataBurp[i]['severity'] != 'Information':
        if DataBurp[i]['name'] in countGroupID:
            countGroupID[DataBurp[i]['name']] += 1
        else:
            countGroupID[DataBurp[i]['name']] = 1


def cleanCode(x):
    x = re.sub('</?[a-z]*>', "", x)
    return (x)


CriticalList = [DataBurp[i]['name']
                for i in DataBurp if DataBurp[i]['severity'] == 'Critical']
CriticalList = list(dict.fromkeys(CriticalList))

HighList = [DataBurp[i]['name']
            for i in DataBurp if DataBurp[i]['severity'] == 'High']
HighList = list(dict.fromkeys(HighList))

MediumList = [DataBurp[i]['name']
              for i in DataBurp if DataBurp[i]['severity'] == 'Medium']
MediumList = list(dict.fromkeys(MediumList))

LowList = [DataBurp[i]['name']
           for i in DataBurp if DataBurp[i]['severity'] == 'Low']
LowList = list(dict.fromkeys(LowList))


def DataCollection(**kwargs):
    global DataBurp
    global vulnerability_url
    global countGroupID
    for data in kwargs:
        for i in kwargs[data]:
            list_url = []
            subContent = {}
            # subContentLow = {}
            countCheck = 0
            for j in DataBurp:
                if DataBurp[j]['severity'] != 'Information':
                    if DataBurp[j]['name'] == i:
                        list_url.append(
                            DataBurp[j]['host/__text']+DataBurp[j]["location"])
                        countCheck += 1
                        # print(countCheck)
                        if countCheck == countGroupID[i]:
                            list_url = list(dict.fromkeys(list_url))
                            url = ""
                            for x in list_url:
                                if url == "":
                                    url = x
                                else:
                                    url = url + '\n' + x
                            list_ref = re.findall(
                                r'(http\S+)\"', DataBurp[j]['references'])
                            ref = ""
                            for temp in list_ref:
                                if ref == "":
                                    ref = temp
                                else:
                                    ref = ref + "\n" + temp
                            if data == "CriticalList":
                                if len(DataBurp[j]['host/__text'].split(":")) == 3:
                                    subContent["port"] = DataBurp[j]['host/__text'].split(":")[
                                        2].split('/')[0]
                                elif DataBurp[j]['host/__text'].split(":")[0] == "https":
                                    subContent["port"] = "443"
                                elif DataBurp[j]['host/__text'].split(":")[0] == "http":
                                    subContent["port"] = "80"
                                else:
                                    subContent["port"] = "N/A"
                                subContent["host"] = url
                                subContent["name"] = DataBurp[j]['name']
                                subContent["description"] = cleanCode(
                                    DataBurp[j]['issueBackground'])
                                subContent["solution"] = cleanCode(
                                    DataBurp[j]['remediationBackground'])
                                subContent["remark"] = ref
                                subContent["color"] = "#7030A0"
                                subContent["severity"] = 1
                                vulnerability_url.append(subContent)
                            if data == "HighList":
                                if len(DataBurp[j]['host/__text'].split(":")) == 3:
                                    subContent["port"] = DataBurp[j]['host/__text'].split(":")[
                                        2].split('/')[0]
                                elif DataBurp[j]['host/__text'].split(":")[0] == "https":
                                    subContent["port"] = "443"
                                elif DataBurp[j]['host/__text'].split(":")[0] == "http":
                                    subContent["port"] = "80"
                                else:
                                    subContent["port"] = "N/A"
                                subContent["host"] = url
                                subContent["name"] = DataBurp[j]['name']
                                subContent["description"] = cleanCode(
                                    DataBurp[j]['issueBackground'])
                                subContent["solution"] = cleanCode(
                                    DataBurp[j]['remediationBackground'])
                                subContent["remark"] = ref
                                subContent["color"] = "#FF0000"
                                subContent["severity"] = 2
                                vulnerability_url.append(subContent)
                            if data == "MediumList":
                                if len(DataBurp[j]['host/__text'].split(":")) == 3:
                                    subContent["port"] = DataBurp[j]['host/__text'].split(":")[
                                        2].split('/')[0]
                                elif DataBurp[j]['host/__text'].split(":")[0] == "https":
                                    subContent["port"] = "443"
                                elif DataBurp[j]['host/__text'].split(":")[0] == "http":
                                    subContent["port"] = "80"
                                else:
                                    subContent["port"] = "N/A"
                                subContent["host"] = url
                                subContent["name"] = DataBurp[j]['name']
                                subContent["description"] = cleanCode(
                                    DataBurp[j]['issueBackground'])
                                subContent["solution"] = cleanCode(
                                    DataBurp[j]['remediationBackground'])
                                subContent["remark"] = ref
                                subContent["color"] = "#FFC000"
                                subContent["severity"] = 3
                                vulnerability_url.append(subContent)
                            if data == "LowList":
                                if len(DataBurp[j]['host/__text'].split(":")) == 3:
                                    subContent["port"] = DataBurp[j]['host/__text'].split(":")[
                                        2].split('/')[0]
                                elif DataBurp[j]['host/__text'].split(":")[0] == "https":
                                    subContent["port"] = "443"
                                elif DataBurp[j]['host/__text'].split(":")[0] == "http":
                                    subContent["port"] = "80"
                                else:
                                    subContent["port"] = "N/A"
                                subContent["host"] = url
                                subContent["name"] = DataBurp[j]['name']
                                subContent["description"] = cleanCode(
                                    DataBurp[j]['issueBackground'])
                                subContent["solution"] = cleanCode(
                                    DataBurp[j]['remediationBackground'])
                                subContent["remark"] = ref
                                subContent["color"] = "#FFFF00"
                                subContent["severity"] = 4
                                vulnerability_url.append(subContent)


DataCollection(CriticalList=CriticalList, HighList=HighList,
               MediumList=MediumList, LowList=LowList)


def runIndex(e):
    return e['severity']


vulnerability_url.sort(key=runIndex, reverse=False)

for i in range(len(vulnerability_url)):
    vulnerability_url[i]['no'] = i+1
    if vulnerability_url[i]['severity'] == 1:
        vulnerability_url[i]['severity'] = "Critical"
    if vulnerability_url[i]['severity'] == 2:
        vulnerability_url[i]['severity'] = "High"
    if vulnerability_url[i]['severity'] == 3:
        vulnerability_url[i]['severity'] = "Medium"
    if vulnerability_url[i]['severity'] == 4:
        vulnerability_url[i]['severity'] = "Low"

try:
    with open('backend/api/sources/dataout.json', 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(vulnerability_url, indent=4))
except NameError as err:
    print(err)
except:
    with open('backend/api/sources/dataout.json', 'w', encoding='ISO-8859-1') as jsonf:
        jsonf.write(json.dumps(vulnerability_url, indent=4))
# ==========================================================================================================

# =====================================     Max burp    =====================================================================
GroupName1 = {}
GroupName2 = []
# Create New Data Source burp
for row in DataBurp:
    GroupName1["Risk"] = DataBurp[row]["severity"]
    GroupName1["ip"] = DataBurp[row]["host/_ip"]
    GroupName1["url"] = DataBurp[row]["host/__text"]
    GroupName1["Group"] = DataBurp[row]["host/__text"]
    GroupName1["issue"] = DataBurp[row]["issueBackground"]
    GroupName1["solution"] = DataBurp[row]["remediationBackground"]
    GroupName1["references"] = DataBurp[row]["references"]
    GroupName2.append(GroupName1)
    GroupName1 = {}

# # Remove Data is duplicate
results = [dict(t) for t in {tuple(d.items()) for d in GroupName2}]
newlist = sorted(results, key=lambda d: d['Group'])

for row in newlist:
    if row['Group'] not in context2:
        context2[row['Group']] = {"No": count, "Name": row['ip'], "url": row['url'],
                                  "Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Total": 0}
        count += 1

    if row['Group'] == "":
        context2[row['Risk']]["Name"] = "etc"
        # Count amount of critaria in each group
    if row['Risk'] == "Critical":
        context2[row['Group']]["Critical"] += 1
        context2[row['Group']]["Total"] += 1
    if row['Risk'] == "High":
        context2[row['Group']]["High"] += 1
        context2[row['Group']]["Total"] += 1
    if row['Risk'] == "Medium":
        context2[row['Group']]["Medium"] += 1
        context2[row['Group']]["Total"] += 1
    if row['Risk'] == "Low":
        context2[row['Group']]["Low"] += 1
        context2[row['Group']]["Total"] += 1

# # print(context)

l = list(context2.values())

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
# +++++++++++++++++++++++++++++== FIX HERE +++++++++++++++++++++++++++++++++++++
percent = {"Critical": '%0.2f' % (CriticalS/Amount*100), "High": '%0.2f' % (
    HighS/Amount*100), "Medium": '%0.2f' % (MediumS/Amount*100), "Low": '%0.2f' % (LowS/Amount*100)}
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

l3 = {"table1": {"Group": l, "Summary": dictS, "Percent": percent}}

# print(l3)
# +++++++++++++++++++++++++++++== FIX HERE +++++++++++++++++++++++++++++++++++++
array2 = [
    {
        "risk": "Critical",
        "value": l3["table1"]["Summary"]["Critical"],
        "colors": "#7030A0",
        "labels": "Critical, " + str(l3["table1"]["Summary"]["Critical"]) + " (" + str(l3["table1"]["Percent"]["Critical"])+"%)"
    },
    {
        "risk": "High",
        "value": l3["table1"]["Summary"]["High"],
        "colors": "#FF0000",
        "labels": "High, " + str(l3["table1"]["Summary"]["High"]) + " (" + str(l3["table1"]["Percent"]["High"])+"%)"
    },
    {
        "risk": "Medium",
        "value": l3["table1"]["Summary"]["Medium"],
        "colors": "#FFC000",
        "labels": "Medium, " + str(l3["table1"]["Summary"]["Medium"]) + " (" + str(l3["table1"]["Percent"]["Medium"])+"%)"
    },
    {
        "risk": "Low",
        "value": l3["table1"]["Summary"]["Low"],
        "colors": "#FFFF00",
        "labels": "Low, " + str(l3["table1"]["Summary"]["Low"]) + " (" + str(l3["table1"]["Percent"]["Low"])+"%)"
    }
]

if genGraph != 0:
    # +++++++++++++++++++++++++++++== FIX HERE +++++++++++++++++++++++++++++++++++++
    value2 = [i["value"] for i in array2 if i["value"] != 0]
    # print(value2)
    ax2.pie(value2, labels=[i["labels"] for i in array2 if i["value"] != 0], colors=[
            i["colors"] for i in array2 if i["value"] != 0], pctdistance=1.2)
    ax2.set_title('Summary Vulnerability by Severity', y=1.05, fontsize=15)
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 0),
               fancybox=True, shadow=True, ncol=4, handles=[Critical, High, Medium, Low])
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    fig2.savefig("backend/api/sources/image/Overview_Graph2.png")

    doc.replace_media("backend/api/sources/image/1.png",
                      "backend/api/sources/image/Overview_Graph2.png")
else:
    doc.replace_media("backend/api/sources/image/1.png",
                      "backend/api/sources/image/noGraph.jpg")
# ==========================================================================================================
contents = {}

name = csvFilePath.split("/")
name = name[-1].split(".csv")

contents['contents_ip'] = list_all_ip_port
contents['vulnerability'] = vulnerability
contents['vulnerability_url'] = vulnerability_url
contents['table1'] = l2
contents['table11'] = l3
contents["fileName"] = name[0]
contents['Date'] = dateNow

doc.render(contents)

doc.save("backend/api/sources/results/"+name[0]+" Nessus"+".docx")
