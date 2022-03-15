import csv
from importlib.resources import contents
import json
from docxtpl import *
import pandas

path = "D:/github/WebReport/testCode/"
inputCSV = "nmap.csv"
doc = DocxTemplate(path+"nmap.docx")


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

csvFilePath = path+inputCSV
jsonFilePath = path+'nmap.json'
makeJson(csvFilePath, jsonFilePath)

DataJSON = pandas.read_json(jsonFilePath)
dict_IP_port = {}
temp_IP = "a"
list_port = []
list_port_prot_serv = []
dict_port_prot_serv = {}

for i in DataJSON:
    if DataJSON[i]['host__address__addr'] != "":
        dict_IP_port[temp_IP] = list_port
        temp_IP = DataJSON[i]['host__address__addr']
        list_port = []
    list_port.append(DataJSON[i]['host__ports__port__portid'])
# ======================================================================================================
    if DataJSON[i]['host__ports__port__state__state'] == "open":
        dict_port_prot_serv["port"] = DataJSON[i]['host__ports__port__portid']
        dict_port_prot_serv["protocol"] = DataJSON[i]['host__ports__port__protocol']
        dict_port_prot_serv["service"] = DataJSON[i]['host__ports__port__service__name']
        list_port_prot_serv.append(dict_port_prot_serv)
        dict_port_prot_serv = {}

dict_IP_port[temp_IP] = list_port
del dict_IP_port['a']

seen = set()
new_l = []
for d in list_port_prot_serv:
    t = tuple(d.items())
    if t not in seen:
        seen.add(t)
        new_l.append(d)

list_port_prot_serv = (sorted(new_l, key=lambda x: int(x['port'])))
# =======================================================================================================


contents = {}
contents['nmap_port'] = list_port_prot_serv

doc.render(contents)
doc.save(path+"generated_nmap.docx")