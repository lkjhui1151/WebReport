import math
from docxtpl import *
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from collections import OrderedDict
import re
import datetime
import numpy as np
import mysql.connector
from xml.etree import ElementTree

mydb = mysql.connector.connect(
    host="10.11.101.32",
    user="Administrator@INETMS",
    password="P@ssw0rd@INETMS",
    database="inetms_autoreport"
)

path_nmap = './backend/api/sources/iso/SIPH phase 2.xml'
pathGreenbone = './backend/api/sources/iso/SIPH-greenbone.csv'
path_doctemplate = "backend/api/sources/templates/templateGreenbone.docx"

np.seterr(divide='ignore', invalid='ignore')
doc = DocxTemplate(path_doctemplate)

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

# ===============================================DATA NUESSUS======================================================================

GroupName1 = {}
GroupName2 = []
# Create New Data Source
mycursor = mydb.cursor()

with open(pathGreenbone, mode="r", encoding='utf-8') as f:
    df = pd.read_csv(f)
    data = pd.DataFrame(df)
    for i, dataset in data.iterrows():
        sql = "select nvt_oid from greenbone where nvt_oid = %s"
        val = (dataset['NVT OID'],)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        dataset['NVT OID'] = dataset["NVT OID"]
        dataset['NVT Name'] = dataset["NVT Name"]
        if isinstance(dataset["Vulnerability Insight"], str) == True:
            dataset['Vulnerability Insight'] = dataset["Vulnerability Insight"]
        else:
            dataset['Vulnerability Insight'] = None
        dataset['Solution'] = dataset["Solution"]
        dataset['Severity'] = dataset["Severity"]
        if isinstance(dataset["CVEs"], str) == True:
            dataset['CVEs'] = dataset["CVEs"]
        else:
            dataset['CVEs'] = None

        if myresult == []:
            sql = "INSERT INTO greenbone (nvt_oid, name_en,description_en,solution_en,remark) VALUES (%s, %s, %s, %s, %s)"
            val = (dataset['NVT OID'], dataset['NVT Name'],
                   dataset['Vulnerability Insight'], dataset['Solution'], dataset['CVEs'])
            mycursor.execute(sql, val)
            mydb.commit()
        else:
            GroupName1["Risk"] = dataset["Severity"]
            GroupName1["Host"] = dataset["IP"]
            GroupName1["Name_vulnerability"] = dataset["NVT Name"]
            GroupName1["Protocol"] = dataset["Port Protocol"]
            GroupName1["Port"] = dataset["Port"]
            GroupName1["Description"] = dataset["Vulnerability Insight"]
            GroupName1["Solution"] = dataset["Solution"]
            GroupName1["Remark"] = dataset["Other References"]
            GroupName1["ID"] = dataset["Result ID"]
            GroupName1["NVT_OID"] = dataset["NVT OID"]

            GroupName1["CVE"] = dataset["CVEs"]
            GroupName1["CVSS"] = dataset["CVSS"]

            GroupName2.append(GroupName1)
            GroupName1 = {}


# Remove Data is duplicate
results = [dict(t) for t in {tuple(d.items()) for d in GroupName2}]
newlist = sorted(results, key=lambda d: (
    tuple(map(int, d['Host'].split('.')))))

# ===============================================DATA NMAP======================================================================
tree = ElementTree.parse(path_nmap)
root = tree.getroot()
header1 = ['IP', 'domain', 'Protocol', 'Port',
           'Status', 'Service']
list_nmap_data = []
for item in root.findall('./host'):
    port = []
    protocol = []
    status = []
    service = []
    loopLen = 0
    ip = item.find('address').get('addr')
    domain = item.find('hostnames').find('hostname').get(
        'name') if item.find('hostnames').find('hostname') != None else None
    loopLen = len(item.find('ports')) - 1
    for item2 in item.find('ports'):
        keys = item2.keys()
        if 'count' not in keys:
            protocol.append(item2.get('protocol'))
            port.append(item2.get('portid'))
            status.append(item2.find('state').get('state'))
            service.append(item2.find('service').get('name'))

    for item3 in range(loopLen):
        dict_nmap_data = {'ip': '', 'domain': '', 'protocol': '',
                          'port': '', 'status': '', 'service': ''}
        dict_nmap_data['ip'] = ip
        dict_nmap_data['domain'] = domain
        dict_nmap_data['protocol'] = protocol[item3]
        dict_nmap_data['port'] = port[item3]
        dict_nmap_data['status'] = status[item3]
        dict_nmap_data['service'] = service[item3]
        list_nmap_data.append(dict_nmap_data)
list_nmap_data = delete_dict_duplicate(list_nmap_data)

# ===============================================start analys=========================================================================
for i in newlist:
    print(i['Name_vulnerability'])
for row in newlist:
    if row['Host'] not in context:
        context[row['Host']] = {"No": count, "Name": row['Host'], "device": {
            row['Host']}, "Total_IP": 0, "Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Total": 0}
        count += 1
    else:
        context[row['Host']]["device"].add(row['Host'])

        countIP = len(context[row['Host']]["device"])
        context[row['Host']]["Total_IP"] = countIP
    if row['Host'] == "":
        context[row['Risk']]["Name"] = "etc"
        # Count amount of critaria in each group
    if row['Risk'] == "Critical":
        context[row['Host']]["Critical"] += 1
        context[row['Host']]["Total"] += 1
    if row['Risk'] == "High":
        context[row['Host']]["High"] += 1
        context[row['Host']]["Total"] += 1
    if row['Risk'] == "Medium":
        context[row['Host']]["Medium"] += 1
        context[row['Host']]["Total"] += 1
    if row['Risk'] == "Low":
        context[row['Host']]["Low"] += 1
        context[row['Host']]["Total"] += 1

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

# ===========================================Table nmap======================================================
list_port_prot_serv = []
dict_port_prot_serv = {}
for i in list_nmap_data:
    if i['status'] == "open":
        dict_port_prot_serv["port"] = i['port']
        dict_port_prot_serv["protocol"] = i['protocol']
        dict_port_prot_serv["service"] = i['service']
        list_port_prot_serv.append(dict_port_prot_serv)
        dict_port_prot_serv = {}
list_port_prot_serv = delete_dict_duplicate(list_port_prot_serv)
list_port_prot_serv = (
    sorted(list_port_prot_serv, key=lambda x: int(x['port'])))

# --------------------------------------make data ip port------------------------------------------------------------
ip = [i['ip'] for i in list_nmap_data]
ip = list(dict.fromkeys(ip))
ip = sorted(ip, key=lambda d: (tuple(map(int, d.split('.')))))
dict_ip_portopen = {i: {'TCP': [], 'UDP': []} for i in ip}


for i in list_nmap_data:
    if i["ip"] in dict_ip_portopen.keys():
        if i["protocol"] == 'tcp':
            dict_ip_portopen[i["ip"]]['TCP'].append(i["port"])
            clearIP = list(dict.fromkeys(dict_ip_portopen[i["ip"]]['TCP']))
            dict_ip_portopen[i["ip"]]['TCP'] = clearIP

        elif i["protocol"] == 'udp':
            dict_ip_portopen[i["ip"]]['UDP'].append(i["port"])
            clearIP = list(dict.fromkeys(dict_ip_portopen[i["ip"]]['UDP']))
            dict_ip_portopen[i["ip"]]['TCP'] = clearIP

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

list_all_ip_port = []
index = 1
for key, value in dict_ip_portopen.items():
    ip_port_ = {}
    ip_port_['no'] = index
    ip_port_['host'] = key
    ip_port_['port'] = value['port']
    list_all_ip_port.append(ip_port_)
    index += 1

print('====================================================================================')
# # # # ==============================================-make data detail==============================================================

NVT_OID = [i["NVT_OID"]for i in newlist]
NVT_OID = list(dict.fromkeys(NVT_OID))
vulnerability = []
subContent = {}
countCheck = 0
GroupName = {}

for i in newlist:
    if i["NVT_OID"] in GroupName:
        GroupName[i["NVT_OID"]] += 1
    else:
        GroupName[i["NVT_OID"]] = 1

for j in NVT_OID:
    dict_port_ip = {}
    port_udp = []
    port_tcp = []
    for i in newlist:
        if i['NVT_OID'] == j:
            if i['Protocol'] == 'tcp':
                port_tcp.append(str(int(i['Port'])))
            elif i['Protocol'] == 'udp':
                port_udp.append(str(int(i['Port'])))
            else:
                port_tcp.append('0')
            if i['Host'] in dict_port_ip:
                dict_port_ip[i['Host']].append(str(int(i['Port'])))
            else:
                if math.isnan(i['Port']):
                    dict_port_ip[i['Host']] = ['0']
                else:
                    dict_port_ip[i['Host']] = [str(int(i['Port']))]
            countCheck += 1
            if countCheck == GroupName[i["NVT_OID"]]:
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
                ref = ""
                if i['CVE'] is not None and isinstance(i['CVE'], str) == True:
                    cve = i['CVE'].split(',')
                    if len(cve) != 1 or cve[0] != '':
                        for a in cve:
                            if ref == "":
                                ref = "CVE: "+a
                            else:
                                ref = ref+"\nCVE: "+a
                if i['Remark'] is not None and isinstance(i['Remark'], str) == True:
                    remark = i['Remark'].split(',')
                    if len(remark) != 1 or remark[0] != '':
                        for a in remark:
                            if ref == "":
                                ref = "remark: "+a
                            else:
                                ref = ref+"\nremark: "+a

                subContent["host"] = ip
                subContent["port"] = port
                subContent["name"] = i['Name_vulnerability']
                print(i['Name_vulnerability'])
                subContent["description"] = i['Description']
                subContent["solution"] = i['Solution']
                subContent["cvss"] = i['CVSS']

                subContent["remark"] = ref
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

# # ==========================================================================================================
contents = {}
name = pathGreenbone.split("/")
name = name[-1].split(".csv")

contents['contents_ip'] = list_all_ip_port  # use
contents['vulnerability'] = vulnerability   # use
contents['table1'] = l2  # use
contents["fileName"] = name[0]  # use
contents['Date'] = dateNow  # use
contents['nmap_port'] = list_port_prot_serv  # use
doc.render(contents)
doc.save("backend/api/sources/results/"+name[0]+" Greenbone.docx")
