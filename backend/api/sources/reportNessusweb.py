import csv
from docxtpl import *
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import json
import pandas
import re
import datetime
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

doc = DocxTemplate("backend/api/sources/templates/templateNessusweb.docx")

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


# <--Burp-->
csvBurp = r'backend/api/sources/iso/KTC-uatloan.csv'
jsonBurp = r'backend/api/sources/dataBurp.json'

# <--Nmap-->
csvNMAP = r'backend/api/sources/iso/null.csv'
jsonNMAP = r'backend/api/sources/dataNmap.json'

makeJson(csvBurp, jsonBurp)
makeJson(csvNMAP, jsonNMAP)

DataBurp = pandas.read_json(jsonBurp)
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


# =================================     Krit NAMP   ===================================================
dict_IP_port = {}
temp_IP = "a"
list_port = []
list_port_prot_serv = []
dict_port_prot_serv = {}

for i in DataNmap:
    if DataNmap[i]['group'] == "burp":
        if DataNmap[i]['host__ports__port__state__state'] == "open":
            dict_port_prot_serv["port"] = DataNmap[i]['host__ports__port__portid']
            dict_port_prot_serv["protocol"] = DataNmap[i]['host__ports__port__protocol']
            dict_port_prot_serv["service"] = DataNmap[i]['host__ports__port__service__name']
            list_port_prot_serv.append(dict_port_prot_serv)
            dict_port_prot_serv = {}

dict_IP_port[temp_IP] = list_port
del dict_IP_port['a']

list_port_prot_serv = delete_dict_duplicate(list_port_prot_serv)

list_port_prot_serv = (
    sorted(list_port_prot_serv, key=lambda x: int(x['port'])))
################################################## krit ##################################################

domainName = [DataNmap[i]['host__hostnames__hostname__name']
              for i in DataNmap if DataNmap[i]['host__hostnames__hostname__name']]
domainName = list(dict.fromkeys(domainName))
# --------------------------------------make data ip port------------------------------------------------------------

dict_url_portopen = {i: {'TCP': [], 'UDP': []} for i in domainName}

# URL
for i in DataNmap:
    if DataNmap[i]["host__hostnames__hostname__name"] in dict_url_portopen.keys():
        if DataNmap[i]["host__ports__port__state__state"] == "open":
            if DataNmap[i]["host__ports__port__protocol"] == 'tcp':
                dict_url_portopen[DataNmap[i]["host__hostnames__hostname__name"]]['TCP'].append(
                    DataNmap[i]["host__ports__port__portid"])

            elif DataNmap[i]["host__ports__port__protocol"] == 'udp':
                dict_url_portopen[DataNmap[i]["host__hostnames__hostname__name"]]['TCP'].append(
                    DataNmap[i]["host__ports__port__portid"])

for i in DataNmap:
    if DataNmap[i]["host__hostnames__hostname__name"] != "" and DataNmap[i]["host__address__addr"] != "":
        dict_url_portopen[DataNmap[i]["host__hostnames__hostname__name"]+","+DataNmap[i]
                          ["host__address__addr"]] = dict_url_portopen[DataNmap[i]["host__hostnames__hostname__name"]]
        del dict_url_portopen[DataNmap[i]["host__hostnames__hostname__name"]]

# URL
for key, value in dict_url_portopen.items():
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
    dict_url_portopen[key]['port'] = temp

list_all_domain_port = []
index = 1
for key, value in dict_url_portopen.items():
    key = key.split(",")
    ip_port_ = {}
    ip_port_['no'] = index
    ip_port_['host'] = key[0]
    ip_port_['ip'] = key[1]
    ip_port_['port'] = value['port']
    list_all_domain_port.append(ip_port_)
    index += 1
# ======================================  krit Burp ====================================================================
GroupName1 = {}
GroupName2 = []
CriticalDict = {}
HighDict = {}
MediumDict = {}
LowDict = {}

# Create New Data Source burp
for row in DataBurp:
    GroupName1["Risk"] = DataBurp[row]["issue__severity"]
    GroupName1["ip"] = DataBurp[row]["issue__host__ip"]
    GroupName1["url"] = DataBurp[row]["issue__host__#Text"]
    GroupName1["Group"] = DataBurp[row]["issue__host__#Text"]
    GroupName1["issue"] = DataBurp[row]["issue__issueBackground"]
    GroupName1["solution"] = DataBurp[row]["issue__remediationBackground"]
    GroupName1["references"] = DataBurp[row]["issue__references"]
    GroupName2.append(GroupName1)
    GroupName1 = {}
    if DataBurp[row]['issue__severity'] == 'Critical':
        if DataBurp[row]['issue__name'] in CriticalDict:
            CriticalDict[DataBurp[row]['issue__name']] += 1
        else:
            CriticalDict[DataBurp[row]['issue__name']] = 1
    elif DataBurp[row]['issue__severity'] == 'High':
        if DataBurp[row]['issue__name'] in HighDict:
            HighDict[DataBurp[row]['issue__name']] += 1
        else:
            HighDict[DataBurp[row]['issue__name']] = 1
    elif DataBurp[row]['issue__severity'] == 'Medium':
        if DataBurp[row]['issue__name'] in MediumDict:
            MediumDict[DataBurp[row]['issue__name']] += 1
        else:
            MediumDict[DataBurp[row]['issue__name']] = 1
    elif DataBurp[row]['issue__severity'] == 'Low':
        if DataBurp[row]['issue__name'] in LowDict:
            LowDict[DataBurp[row]['issue__name']] += 1
        else:
            LowDict[DataBurp[row]['issue__name']] = 1

# # Remove Data is duplicate

newlist = sorted(GroupName2, key=lambda d: d['Group'])

vulnerability_url = []


def DataCollection(**kwargs):
    global DataBurp
    global vulnerability_url
    for data in kwargs:
        for i in kwargs[data]:
            list_url = []
            subContent = {}
            # subContentLow = {}
            countCheck = 0
            for j in DataBurp:
                if DataBurp[j]['issue__severity'] != 'Information':
                    if DataBurp[j]['issue__name'] == i and data == DataBurp[j]['issue__severity']:
                        list_url.append(
                            DataBurp[j]['issue__host__#Text']+DataBurp[j]["issue__location"])
                        countCheck += 1
                        if countCheck == kwargs[data][i]:
                            list_url = list(dict.fromkeys(list_url))
                            url = ""
                            for x in list_url:
                                if url == "":
                                    url = x
                                else:
                                    url = url + '\n' + x
                            list_ref = re.findall(
                                r'(http\S+)\"', DataBurp[j]['issue__references'])
                            ref = ""
                            for temp in list_ref:
                                if ref == "":
                                    ref = temp
                                else:
                                    ref = ref + "\n" + temp
                            if len(DataBurp[j]['issue__host__#Text'].split(":")) == 3:
                                subContent["port"] = DataBurp[j]['issue__host__#Text'].split(":")[
                                    2].split('/')[0]
                            elif DataBurp[j]['issue__host__#Text'].split(":")[0] == "https":
                                subContent["port"] = "443"
                            elif DataBurp[j]['issue__host__#Text'].split(":")[0] == "http":
                                subContent["port"] = "80"
                            else:
                                subContent["port"] = "N/A"
                            subContent["host"] = url
                            subContent["name"] = DataBurp[j]['issue__name']
                            subContent["description"] = cleanCode(
                                DataBurp[j]['issue__issueBackground'])
                            subContent["solution"] = cleanCode(
                                DataBurp[j]['issue__remediationBackground'])
                            subContent["remark"] = ref
                            if data == "Critical":
                                subContent["color"] = "#7030A0"
                                subContent["risk"] = 1
                            elif data == "High":
                                subContent["color"] = "#FF0000"
                                subContent["risk"] = 2
                            elif data == "Medium":
                                subContent["color"] = "#FFC000"
                                subContent["risk"] = 3
                            elif data == "Low":
                                subContent["color"] = "#FFFF00"
                                subContent["risk"] = 4

                            vulnerability_url.append(subContent)


DataCollection(Critical=CriticalDict, High=HighDict,
               Medium=MediumDict, Low=LowDict)

vulnerability_url.sort(key=runIndex, reverse=False)

for i in range(len(vulnerability_url)):
    vulnerability_url[i]['no'] = i+1
    if vulnerability_url[i]['risk'] == 1:
        vulnerability_url[i]['risk'] = "Critical"
    if vulnerability_url[i]['risk'] == 2:
        vulnerability_url[i]['risk'] = "High"
    if vulnerability_url[i]['risk'] == 3:
        vulnerability_url[i]['risk'] = "Medium"
    if vulnerability_url[i]['risk'] == 4:
        vulnerability_url[i]['risk'] = "Low"

# =====================================     Max burp    =====================================================================

count = 1
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

l = list(context2.values())

totalS = (sum([d['Total'] for d in l]))
CriticalS = (sum([d['Critical'] for d in l]))
HighS = (sum([d['High'] for d in l]))
MediumS = (sum([d['Medium'] for d in l]))
LowS = (sum([d['Low'] for d in l]))
Amount = CriticalS+HighS+MediumS+LowS

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
name = csvBurp.split("/")
name = name[-1].split(".csv")

contents['contents_domain'] = list_all_domain_port  # use
contents['vulnerability_url'] = vulnerability_url   # use
contents['table11'] = l3    # use
contents["fileName"] = name[0]  # use
contents['Date'] = dateNow  # use
contents['nmap_port'] = list_port_prot_serv  # use
doc.render(contents)
doc.save("backend/api/sources/results/"+name[0]+" Nessus Web"+".docx")
