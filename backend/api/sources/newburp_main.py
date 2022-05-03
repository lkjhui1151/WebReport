import csv
from docxtpl import *
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import json
import pandas as pd
import re
import datetime
import numpy as np
from xml.etree import ElementTree
import mysql.connector
np.seterr(divide='ignore', invalid='ignore')

mydb = mysql.connector.connect(
    host="10.11.101.32",
    user="Administrator@INETMS",
    password="P@ssw0rd@INETMS",
    database="inetms_autoreport"
)
path_nmapXML = "./backend/api/sources/iso/SIPH phase1.xml"
path_burpXML = './backend/api/sources/iso/ktc.xml'
path_doctemplate = "./backend/api/sources/templates/templateNessusweb.docx"

doc = DocxTemplate(path_doctemplate)

tree = ElementTree.parse(path_burpXML)
root = tree.getroot()

header1 = ['Risk', 'Name', 'Host', 'Domain',
           'Location', 'Description', 'Solution', 'References']

def cleanTags(raw_tag):
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(CLEANR, '', raw_tag)
    return cleantext


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

# ===============================================DATA NMAP======================================================================
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
print(list_nmap_data)
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
# ======================================  make data Burp ====================================================================
GroupName1 = {}
GroupName2 = []
CriticalDict = {}
HighDict = {}
MediumDict = {}
LowDict = {}
tree = ElementTree.parse(path_nmapXML)
root = tree.getroot()

# Create New Data Source burp
list_burp_data = []
for item in root.findall('issue/issue'):
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

    dict_burp_data['severity'] = severity
    dict_burp_data['name'] = name
    dict_burp_data['ip'] = ip
    dict_burp_data['domain'] = domain
    dict_burp_data['location'] = location
    dict_burp_data['description'] = description
    dict_burp_data['solution'] = solution
    dict_burp_data['remark'] = remark
    list_burp_data.append(dict_burp_data)
delete_dict_duplicate(list_burp_data)
for i in list_burp_data:
    print(i)

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
            GroupName1["Risk"] = dataset["Risk"]
            GroupName1["ip"] = dataset["Host"]
            GroupName1["url"] = dataset["Domain"]
            GroupName1["Group"] = dataset["Domain"]
            GroupName1["issue"] = dataset["Description"]
            GroupName1["solution"] = dataset["Solution"]
            GroupName1["references"] = dataset["References"]

            GroupName2.append(GroupName1)
            GroupName1 = {}
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

# # Remove Data is duplicate

newlist = sorted(GroupName2, key=lambda d: d['Group'])

vulnerability_url = []


def DataCollection(**kwargs):
    for data in kwargs:
        for index in kwargs[data]:
            list_url = []
            subContent = {}
            # subContentLow = {}
            countCheck = 0
            for i, j in data2.iterrows():
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
    fig2.savefig("./backend/api/sources/image/Overview_Graph2.png")

    doc.replace_media("./backend/api/sources/image/1.png",
                      "./backend/api/sources/image/Overview_Graph2.png")
else:
    doc.replace_media("./backend/api/sources/image/1.png",
                      "./backend/api/sources/image/noGraph.jpg")
# ==========================================================================================================
contents = {}
name = path_burpXML.split("/")
name = name[-1].split(".xml")

contents['contents_domain'] = list_all_ip_port  # use
contents['vulnerability_url'] = vulnerability_url   # use
contents['table11'] = l3    # use
contents["fileName"] = name[0]  # use
contents['Date'] = dateNow  # use
contents['nmap_port'] = list_port_prot_serv  # use
doc.render(contents)
doc.save("./backend/media/report/"+name[0]+".docx")
