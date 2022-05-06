from docxtpl import *
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import re
import datetime
import numpy as np
import mysql.connector
from xml.etree import ElementTree
from collections import OrderedDict

np.seterr(divide='ignore', invalid='ignore')

mydb = mysql.connector.connect(
    host="10.11.101.32",
    user="Administrator@INETMS",
    password="P@ssw0rd@INETMS",
    database="inetms_autoreport"
)
path_nmapXML = "./backend/api/sources/iso/KTC_nmap.xml"
path_nessusCSV = './backend/api/sources/iso/KTC_nessus.csv'
path_burpXML = './backend/api/sources/iso/ktc.xml'
path_doctemplate = "./backend/api/sources/templates/templateNessus.docx"

doc = DocxTemplate(path_doctemplate)

def cleanTags(raw_tag):
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(CLEANR, '', raw_tag)
    return cleantext

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
dict_nessus_data = {}
list_nessus_data = []

date = datetime.datetime.now()
dateNow = date.strftime("%B")+" " + \
    date.strftime("%d")+", "+date.strftime("%Y")

# ===============================================DATA NUESSUS======================================================================
mycursor = mydb.cursor()
with open(path_nessusCSV, mode="r", encoding='utf-8') as f:
    df = pd.read_csv(f)
    data = pd.DataFrame(df)
    for i, dataset in data.iterrows():
        sql = "select plugin from nessus where plugin = %s"
        val = (dataset['Plugin ID'],)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()

        dataset["Solution"] = dataset["Solution"] if isinstance(
            dataset["Solution"], str) == True else None
        dataset["Risk"] = dataset["Risk"] if isinstance(
            dataset["Risk"], str) == True else None
        dataset["See Also"] = dataset["See Also"] if isinstance(
            dataset["See Also"], str) == True else None

        if myresult == []:
            sql = "INSERT INTO nessus (plugin, name_en,description_en,solution_en,remark) VALUES (%s, %s, %s, %s, %s)"
            val = (dataset['Plugin ID'], dataset['Name'],
                   dataset['Description'], dataset['Solution'], dataset['See Also'])
            mycursor.execute(sql, val)
            mydb.commit()

        else:
            dict_nessus_data["Risk"] = dataset["Risk"]
            dict_nessus_data['Plugin ID'] = dataset['Plugin ID']
            dict_nessus_data["Host"] = dataset["Host"]
            dict_nessus_data["Name"] = dataset["Name"]
            dict_nessus_data["Group"] = dataset["Host"]
            dict_nessus_data["Description"] = dataset['Description']
            dict_nessus_data["Protocol"] = dataset["Protocol"]
            dict_nessus_data['Solution'] = dataset['Solution']
            dict_nessus_data["Port"] = dataset["Port"]
            dict_nessus_data['See Also'] = dataset['See Also']
            dict_nessus_data['CVSS v3.0 Base Score'] = dataset['CVSS v3.0 Base Score']
            list_nessus_data.append(dict_nessus_data)
            dict_nessus_data = {}

# Remove Data is duplicate
list_nessus_data = [dict(t)
                    for t in {tuple(d.items()) for d in list_nessus_data}]
list_nessus_data = sorted(list_nessus_data, key=lambda d: (
    tuple(map(int, d['Group'].split('.')))))

# ===========================================================================================================
for row in list_nessus_data:
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

name = [i["Plugin ID"] for i in list_nessus_data if i["Risk"] != "None"]
name = list(dict.fromkeys(name))
dict_port_ip = {}
vulnerability = []
subContent = {}
countCheck = 0
GroupName = {}

for i in list_nessus_data:
    if i['Risk'] != 'None':
        if i['Plugin ID'] in GroupName:
            GroupName[i['Plugin ID']] += 1
        else:
            GroupName[i['Plugin ID']] = 1

for j in name:
    dict_port_ip = {}
    port_udp = []
    port_tcp = []
    for i in list_nessus_data:
        if i['Risk'] != "None":
            if i['Plugin ID'] == j:
                if i['Protocol'] == 'tcp':
                    port_tcp.append(str(i['Port']))
                elif i['Protocol'] == 'udp':
                    port_udp.append(str(i['Port']))
                if i['Host'] in dict_port_ip:
                    dict_port_ip[i['Host']].append(
                        str(i['Port']))
                else:
                    dict_port_ip[i['Host']] = [str(i['Port'])]
                countCheck += 1
                if countCheck == GroupName[i['Plugin ID']]:
                    port_tcp = list(dict.fromkeys(port_tcp))
                    port_tcp = sorted(port_tcp, key=lambda x: int(x))
                    port_udp = list(dict.fromkeys(port_udp))
                    port_udp = sorted(port_udp, key=lambda x: int(x))

                    port = ""
                    if port_tcp:
                        port = 'TCP: '+", ".join(port_tcp)
                    if port_udp:
                        if port != "":
                            port = 'UDP: '+", ".join(port_tcp)
                        eles: port = port+'\nUDP: '+",".join(port_tcp)

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
                        ip = ip + key + '('+", ".join(value) + ')'

                    subContent["host"] = ip
                    subContent["port"] = port
                    subContent["name"] = i['Name']
                    subContent["description"] = i['Description']
                    subContent["solution"] = i['Solution']
                    subContent["cvss"] = i['CVSS v3.0 Base Score']
                    if i['See Also'] == "":
                        subContent["remark"] = " - "
                    else:
                        subContent["remark"] = i['See Also']
                    if i['Risk'] == "Critical":
                        subContent["color"] = "#7030A0"
                        subContent["risk"] = 1
                    elif i['Risk'] == "High":
                        subContent["color"] = "#FF0000"
                        subContent["risk"] = 2
                    elif i['Risk'] == "Medium":
                        subContent["color"] = "#FFC000"
                        subContent["risk"] = 3
                    elif i['Risk'] == "Low":
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

# ===========================================================================================================================
# ======================================  make data Burp ====================================================================
CriticalDict = {}
HighDict = {}
MediumDict = {}
LowDict = {}
tree2 = ElementTree.parse(path_burpXML)
root = tree2.getroot()

# Create New Data Source burp
list_burp_data = []
for item in root.findall('./issue'):
    dict_burp_data = {}
    name = item.find("name").text.strip()

    domain = item.find("host")
    domain = domain.text.strip() if domain is not None else None

    ip = item.find("host")
    ip = ip.get('ip')

    location = item.find("location")
    location = location.text.strip() if location is not None else None

    severity = item.find("severity")
    severity = severity.text.strip() if severity is not None else None

    description = item.find("issueBackground")
    description = cleanTags(description.text.strip()
                            ) if description is not None else None

    solution = item.find("remediationBackground")
    solution = cleanTags(solution.text.strip()
                         ) if solution is not None else None

    remark = item.find("references")
    remark = cleanTags(remark.text.strip()) if remark is not None else None

    dict_burp_data['Risk'] = severity
    dict_burp_data['Name'] = name
    dict_burp_data['Host'] = ip
    dict_burp_data['Domain'] = domain
    dict_burp_data['Location'] = location
    dict_burp_data['Description'] = description
    dict_burp_data['Solution'] = solution
    dict_burp_data['References'] = remark
    list_burp_data.append(dict_burp_data)
delete_dict_duplicate(list_burp_data)
list_burp_data = sorted(list_burp_data, key=lambda d: d['Name'])
list_burp_data = sorted(list_burp_data, key=lambda d: (
    tuple(map(int, d['Host'].split('.')))))
# ========================================BURP ===================================================
mycursor = mydb.cursor()

for dataset in list_burp_data:
    sql = "select name_en from burp where name_en = %s"
    val = (dataset['Name'],)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    dataset['Name'] = dataset["Name"]
    if isinstance(dataset["Description"], str) == True:
        dataset['Description'] = dataset["Description"]
    else:
        dataset['Description'] = None
    dataset['Solution'] = dataset["Solution"]
    dataset['Risk'] = dataset["Risk"]
    if isinstance(dataset["References"], str) == True:
        dataset['References'] = dataset["References"]
    else:
        dataset['References'] = None

    if myresult == []:
        sql = "INSERT INTO burp (name_en,description_en,solution_en,remark) VALUES (%s, %s, %s, %s)"
        val = (dataset['Name'], dataset['Description'],
               dataset['Solution'], dataset['References'])
        mycursor.execute(sql, val)
        mydb.commit()
    else:
        if dataset["Risk"] != "Information":

            if dataset['Risk'] == 'Critical':
                if dataset['Name'] in CriticalDict:
                    CriticalDict[dataset['Name']] += 1
                else:
                    CriticalDict[dataset['Name']] = 1
            elif dataset['Risk'] == 'High':
                if dataset['Name'] in HighDict:
                    HighDict[dataset['Name']] += 1
                else:
                    HighDict[dataset['Name']] = 1
            elif dataset['Risk'] == 'Medium':
                if dataset['Name'] in MediumDict:
                    MediumDict[dataset['Name']] += 1
                else:
                    MediumDict[dataset['Name']] = 1
            elif dataset['Risk'] == 'Low':
                if dataset['Name'] in LowDict:
                    LowDict[dataset['Name']] += 1
                else:
                    LowDict[dataset['Name']] = 1

vulnerability_url = []

def DataCollection(**kwargs):
    for data in kwargs:
        for index in kwargs[data]:
            list_url = []
            subContent = {}
            # subContentLow = {}
            countCheck = 0
            for j in list_burp_data:
                if j['Risk'] != 'Information':
                    if j['Name'] == index and data == j['Risk']:
                        list_url.append(
                            j['Domain']+j["Location"])
                        countCheck += 1
                        if countCheck == kwargs[data][index]:
                            list_url = list(dict.fromkeys(list_url))
                            url = ""
                            for x in list_url:
                                if url == "":
                                    url = x
                                else:
                                    url = url + '\n' + x
                            list_ref = re.findall(
                                r'(http\S+)\"', j['References'])
                            ref = ""
                            for temp in list_ref:
                                if ref == "":
                                    ref = temp
                                else:
                                    ref = ref + "\n" + temp
                            if len(j['Domain'].split(":")) == 3:
                                subContent["port"] = j['Domain'].split(":")[
                                    2].split('/')[0]
                            elif j['Domain'].split(":")[0] == "https":
                                subContent["port"] = "443"
                            elif j['Domain'].split(":")[0] == "http":
                                subContent["port"] = "80"
                            else:
                                subContent["port"] = "N/A"
                            subContent["host"] = url
                            subContent["name"] = j['Name']
                            subContent["description"] = cleanCode(
                                j['Description'])
                            subContent["solution"] = cleanCode(
                                j['Solution'])
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
for row in list_burp_data:
    if row['Domain'] not in context2:
        context2[row['Domain']] = {"No": count, "Name": row['Host'], "url": row['Domain'],
                                   "Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Total": 0}
        count += 1

    if row['Domain'] == "":
        context2[row['Risk']]["Name"] = "etc"
        # Count amount of critaria in each group
    if row['Risk'] == "Critical":
        context2[row['Domain']]["Critical"] += 1
        context2[row['Domain']]["Total"] += 1
    if row['Risk'] == "High":
        context2[row['Domain']]["High"] += 1
        context2[row['Domain']]["Total"] += 1
    if row['Risk'] == "Medium":
        context2[row['Domain']]["Medium"] += 1
        context2[row['Domain']]["Total"] += 1
    if row['Risk'] == "Low":
        context2[row['Domain']]["Low"] += 1
        context2[row['Domain']]["Total"] += 1

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
    fig2.savefig("./backend/api/sources/image/Overview_Graph2.png")

    doc.replace_media("./backend/api/sources/image/1.png",
                      "./backend/api/sources/image/Overview_Graph2.png")
else:
    doc.replace_media("./backend/api/sources/image/1.png",
                      "./backend/api/sources/image/noGraph.jpg")
# ====================================================================================================================================
# ================================================NMAP=============================================================================
# =============================================== make DATA NMAP======================================================================
tree = ElementTree.parse(path_nmapXML)
root = tree.getroot()
header1 = ['IP', 'domain', 'Protocol', 'Port',
           'Status', 'Service']
list_nmap_data = []
for item in root.findall('./host'):
    domain = None
    ptr = None
    port = []
    protocol = []
    status = []
    service = []
    loopLen = 0
    ip = item.find('address').get('addr')
    for item2 in item.find('hostnames'):
        keys = item2.get('type')
        if keys == 'user':
            domain = item2.get('name')
        if keys == 'PTR':
            ptr = item2.get('name')
    loopLen = len(item.find('ports'))
    count = 0
    for item2 in item.find('ports'):
        keys = item2.keys()
        if 'count' not in keys:
            protocol.append(item2.get('protocol'))
            port.append(item2.get('portid'))
            status.append(item2.find('state').get('state'))
            service.append(item2.find('service').get('name'))
        else:
            count += 1

    for item3 in range(loopLen - count):
        dict_nmap_data = {'IP': '', 'Domain': '', 'Protocol': '',
                          'Port': '', 'Status': '', 'Service': '', 'PTR': ''}
        dict_nmap_data['IP'] = ip
        dict_nmap_data['Domain'] = domain
        dict_nmap_data['PTR'] = ptr
        dict_nmap_data['Protocol'] = protocol[item3]
        dict_nmap_data['Port'] = port[item3]
        dict_nmap_data['Status'] = status[item3]
        dict_nmap_data['Service'] = service[item3]
        list_nmap_data.append(dict_nmap_data)
list_nmap_data = delete_dict_duplicate(list_nmap_data)
list_nmap_data = sorted(list_nmap_data, key=lambda d: (
    tuple(map(int, d['IP'].split('.')))))

# ===========================================Table nmap======================================================
list_port_prot_serv = []
dict_port_prot_serv = {}
for i in list_nmap_data:
    if i['Status'] == "open":
        dict_port_prot_serv["port"] = i['Port']
        dict_port_prot_serv["protocol"] = i['Protocol']
        dict_port_prot_serv["service"] = i['Service']
        list_port_prot_serv.append(dict_port_prot_serv)
        dict_port_prot_serv = {}
list_port_prot_serv = delete_dict_duplicate(list_port_prot_serv)
list_port_prot_serv = (
    sorted(list_port_prot_serv, key=lambda x: int(x['port'])))
# --------------------------------------make data ip port Brup------------------------------------------------------------
dict_ip_portopen = {}
for i in list_nmap_data:
    for j in list_burp_data:
        if i['IP'] in j['Host']:
            dict_ip_portopen[i['IP']] = {
                'TCP': [], 'UDP': [], 'Domain': i['Domain'] if i['Domain'] is not None else ""}

for i in list_nmap_data:
    if i['IP'] in dict_ip_portopen.keys():
        if i["Protocol"] == 'tcp':
            dict_ip_portopen[i['IP']]['TCP'].append(i["Port"])
            clearIP = list(dict.fromkeys(dict_ip_portopen[i['IP']]['TCP']))
            dict_ip_portopen[i['IP']]['TCP'] = clearIP

        elif i["Protocol"] == 'udp':
            dict_ip_portopen[i['IP']]['UDP'].append(i["Port"])
            clearIP = list(dict.fromkeys(dict_ip_portopen[i['IP']]['UDP']))
            dict_ip_portopen[i['IP']]['TCP'] = clearIP

for key, value in dict_ip_portopen.items():
    temp = ""
    for i in value:
        if i != 'Domain':
            value[i] = list(dict.fromkeys(value[i]))
            value[i] = sorted(value[i], key=lambda d: (
                tuple(map(int, d.split('.')))))
            if '0' in value[i]:
                value[i].remove('0')
            if value[i]:
                if temp != "":
                    temp = temp+'\n'
                temp = i+' : '+', '.join(value[i])

    dict_ip_portopen[key]['port'] = temp

list_all_ip_port_burp = []
index = 1
for key, value in dict_ip_portopen.items():
    ip_port_ = {}
    ip_port_['no'] = index
    ip_port_['host'] = value['Domain']
    ip_port_['ip'] = key
    ip_port_['port'] = value['port']
    list_all_ip_port_burp.append(ip_port_)
    index += 1
# --------------------------------------make data ip port nessus------------------------------------------------------------
dict_ip_portopen = {i['Host']: {'TCP': [], 'UDP': []}
                    for i in list_nessus_data}
for i in list_nmap_data:
    if i['IP'] in dict_ip_portopen.keys():
        if i["Protocol"] == 'tcp':
            dict_ip_portopen[i['IP']]['TCP'].append(i["Port"])
            clearIP = list(dict.fromkeys(dict_ip_portopen[i['IP']]['TCP']))
            dict_ip_portopen[i['IP']]['TCP'] = clearIP

        elif i["Protocol"] == 'udp':
            dict_ip_portopen[i['IP']]['UDP'].append(i["Port"])
            clearIP = list(dict.fromkeys(dict_ip_portopen[i['IP']]['UDP']))
            dict_ip_portopen[i['IP']]['TCP'] = clearIP

for key, value in dict_ip_portopen.items():
    temp = ""
    for i in value:
        value[i] = list(dict.fromkeys(value[i]))
        value[i] = sorted(value[i], key=lambda d: (
            tuple(map(int, d.split('.')))))
        if '0' in value[i]:
            value[i].remove('0')
        if value[i]:
            if temp != "":
                temp = temp+'\n'
            temp = i+' : '+', '.join(value[i])

    dict_ip_portopen[key]['port'] = temp

list_all_ip_port_nessus = []
index = 1
for key, value in dict_ip_portopen.items():

    ip_port_ = {}
    ip_port_['no'] = index
    ip_port_['host'] = key
    ip_port_['port'] = value['port']
    list_all_ip_port_nessus.append(ip_port_)
    index += 1
# ==========================================================================================================
contents = {}
name = path_nessusCSV.split("/")
name = name[-1].split(".xml")
contents['contents_ip'] = list_all_ip_port_nessus
contents['contents_domain'] = list_all_ip_port_burp  # use
contents['vulnerability'] = vulnerability   # use
contents['vulnerability_url'] = vulnerability_url   # use
contents['table1'] = l2  # use
contents['table11'] = l3    # use
contents["fileName"] = name[0]  # use
contents['Date'] = dateNow  # use
contents['nmap_port'] = list_port_prot_serv  # use

doc.render(contents)
doc.save("./backend/media/report/"+name[0]+".docx")