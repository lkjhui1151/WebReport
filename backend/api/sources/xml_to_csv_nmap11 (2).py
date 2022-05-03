from xml.etree import ElementTree
import csv
import os

file = 'SIPH phase1.xml'
tree = ElementTree.parse(
    "D:/INET-MS/Auto report/GitHub/WebReport/backend/api/sources/iso/"+file)
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

for i in list_nmap_data:
    print(i)