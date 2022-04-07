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
doc = DocxTemplate("backend/api/sources/templates/templateNessusinfra.docx")

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
    date.strftime("%d")+", "+date.strftime("%Y")


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


# <--Nessus-->
CSVNessus = r'backend/api/sources/iso/SIPH-nessus.csv'
jsonNessus = r'backend/api/sources/dataNessus.json'

# <--Nmap-->
CSVNMAP = r'backend/api/sources/iso/SIPH-nmap.csv'
jsonNMAP = r'backend/api/sources/dataNmap.json'

makeJson(CSVNessus, jsonNessus)
makeJson(CSVNMAP, jsonNMAP)

DataJSON = pandas.read_json(jsonNessus)
DataNmap = pandas.read_json(jsonNMAP)


def delete_dict_duplicate(dict_dup):
    seen = set()
    new_l = []
    for d in dict_dup:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)
    return new_l


def runIndex(e):
    return e['risk']


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        if pct > 0:
            return '{v:d} ({p:1.0f}%)'.format(p=pct, v=val)
        else:
            return ''
    return my_autopct


def cleanCode(x):
    x = re.sub(r'\\n', '\n', x)
    x = re.sub(r'</?[a-z]*>', "", x)
    return (x)


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

value = [i["value"] for i in array]

if genGraph != 0:
    value = [i["value"] for i in array if i["value"] != 0]
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

# =================================     Krit NAMP   ===================================================
dict_IP_port = {}
temp_IP = "a"
list_port = []
list_port_prot_serv = []
dict_port_prot_serv = {}

for i in DataNmap:
    if DataNmap[i]['host__address__addr'] != "":
        dict_IP_port[temp_IP] = list_port
        if DataNmap[i]['group'] == "nessus":
            temp_IP = DataNmap[i]['group']+"," + \
                DataNmap[i]['host__address__addr']
        if DataNmap[i]['group'] == "burp":
            temp_IP = DataNmap[i]['group']+"," + \
                DataNmap[i]['host__hostnames__hostname__name']
        list_port = []
    list_port.append(DataNmap[i]['host__ports__port__protocol'] +
                     ","+DataNmap[i]['host__ports__port__portid'])
# ===========================================Table nmap======================================================
    if DataNmap[i]['host__ports__port__state__state'] == "open":
        dict_port_prot_serv["port"] = DataNmap[i]['host__ports__port__portid']
        dict_port_prot_serv["protocol"] = DataNmap[i]['host__ports__port__protocol']
        dict_port_prot_serv["service"] = DataNmap[i]['host__ports__port__service__name']
        list_port_prot_serv.append(dict_port_prot_serv)
        dict_port_prot_serv = {}
dict_IP_port[temp_IP] = list_port

del dict_IP_port['a']


ip = [DataNmap[i]['host__address__addr'] for i in DataNmap]
ip = list(dict.fromkeys(ip))
# ip.remove("")
ip = sorted(ip, key=lambda d: (tuple(map(int, d.split('.')))))

list_port_prot_serv = delete_dict_duplicate(list_port_prot_serv)
list_port_prot_serv = (
    sorted(list_port_prot_serv, key=lambda x: int(x['port'])))
# --------------------------------------make data ip port------------------------------------------------------------

dict_ip_portopen = {i: {'TCP': [], 'UDP': []} for i in ip}

for i in DataNmap:
    if DataNmap[i]["host__address__addr"] in dict_ip_portopen.keys():
        if DataNmap[i]["host__ports__port__protocol"] == 'tcp':
            dict_ip_portopen[DataNmap[i]["host__address__addr"]]['TCP'].append(
                DataNmap[i]["host__ports__port__portid"])
            clearIP = list(dict.fromkeys(
                dict_ip_portopen[DataNmap[i]["host__address__addr"]]['TCP']))
            dict_ip_portopen[DataNmap[i]
                             ["host__address__addr"]]['TCP'] = clearIP
            # print(clearIP)
        elif DataNmap[i]["host__ports__port__protocol"] == 'udp':
            dict_ip_portopen[DataNmap[i]["host__address__addr"]]['UDP'].append(
                DataNmap[i]["host__ports__port__portid"])
            clearIP = list(dict.fromkeys(
                dict_ip_portopen[DataNmap[i]["host__address__addr"]]['UDP']))
            dict_ip_portopen[DataNmap[i]
                             ["host__address__addr"]]['TCP'] = clearIP

# print(dict_ip_portopen)

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
                        temp = i+': '+value[i][index]
                else:
                    temp = i+': '+value[i][index]
            else:
                temp = temp+', '+value[i][index]
    dict_ip_portopen[key]['port'] = temp

list_all_ip_port = []
index = 1
for key, value in dict_ip_portopen.items():
    ip_port_ = {}
    ip_port_['no'] = index
    ip_port_['host'] = key
    ip_port_['port'] = value['port']
    list_all_ip_port.append(ip_port_)
    index += 1

# # ==============================================-make data detail==============================================================
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
                                port = port + '\nUDP: '+port_udp[index]
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
name = CSVNessus.split("/")
name = name[-1].split(".csv")

contents['contents_ip'] = list_all_ip_port  # use
contents['vulnerability'] = vulnerability   # use
contents['table1'] = l2  # use
contents["fileName"] = name[0]  # use
contents['Date'] = dateNow  # use
contents['nmap_port'] = list_port_prot_serv  # use
doc.render(contents)
doc.save("backend/api/sources/results/"+name[0]+" Nessus Infra"+".docx")
