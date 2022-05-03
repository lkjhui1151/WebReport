from ast import Break
from itertools import count
from tracemalloc import stop
from xml.etree import ElementTree
import csv
import os

file = 'SIPH phase1.xml'
tree = ElementTree.parse("D:/INET-MS/Auto report/GitHub/WebReport/backend/api/sources/iso/"+file)
root = tree.getroot()
list_nmap_data = []
for item in root.findall('./host'):
    ip = item.find('address').get('addr')
    domain = item.find('hostnames').find('hostname').get(
        'name') if item.find('hostnames').find('hostname') != None else None
    for item2 in root.findall('./host/ports/port'):
        dict_nmap_data = {'ip':'', 'domain':'','protocol':'', 'port':'', 'status':'', 'service':''}
        dict_nmap_data['ip'] = ip
        dict_nmap_data['domain'] = domain
        dict_nmap_data['protocol'] = item2.get('protocol')
        dict_nmap_data['port'] = item2.get('portid')
        dict_nmap_data['status'] = item2.find('state').get('state')
        dict_nmap_data['service'] = item2.find('service').get('name')
        list_nmap_data.append(dict_nmap_data)
for i in list_nmap_data:
    print(i)
ip = [i['ip'] for i in list_nmap_data]
ip = list(dict.fromkeys(ip))
ip = sorted(ip, key=lambda d: (tuple(map(int, d.split('.')))))
dict_ip_portopen = {i: {'TCP': [], 'UDP': []} for i in ip}

a=0
for i in list_nmap_data:
    # if i["ip"] in dict_ip_portopen.keys():
    if i["protocol"] == 'tcp':
        dict_ip_portopen[i["ip"]]['TCP'].append(i["port"])
        clearIP = list(dict.fromkeys(dict_ip_portopen[i["ip"]]['TCP']))
        dict_ip_portopen[i["ip"]]['TCP'] = clearIP

    elif i["protocol"] == 'udp':
        dict_ip_portopen[i["ip"]]['UDP'].append(i["port"])
        clearIP = list(dict.fromkeys(dict_ip_portopen[i["ip"]]['UDP']))
        dict_ip_portopen[i["ip"]]['TCP'] = clearIP
    a +=1
    print(i)
    if a==220:
    
        break

print(dict_ip_portopen)
