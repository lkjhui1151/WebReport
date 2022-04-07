import re
from tokenize import group
import pandas as pd
import re
df = pd.read_csv('ticket.csv')

list_data=[]

for index, row in df.iterrows():
    srcIP=""
    desIP=""
    dict_data={}
    dict_data['Customer_Name'] = row['Customer_Name']
    description   = re.findall('ประเภทของภัยคุกคาม:\s(.*)[^ค]*',row['Description'])
    if  description :
        if description[0][0:8]==('Outbound'):
            srcIP   =   re.findall('IP เครื่องเป้าหมาย:\s(\d+\.\d+\.\d+\.\d+)[^ห]*',row['Description'])
            desIP   =   re.findall('IP เครื่องปลายทาง:\s(\d+\.\d+\.\d+\.\d+)[^โ]*',row['Description'])
        else:
            srcIP   =   re.findall('IP เครื่องต้นทาง:\s(\d+\.\d+\.\d+\.\d+)[^ห]*',row['Description'])
            desIP   =   re.findall('IP เครื่องเป้าหมาย:\s(\d+\.\d+\.\d+\.\d+)[^โ]*',row['Description'])
        prot =  re.findall('โปรโตคอล:\s(\S+)',row['Description'])
        port = re.findall('โปรโตคอล:\s(\S+)',row['Description'])
        act =  re.findall('Action:?\s*(\S+)',row['Description'])
        time = re.findall('\s*(\d+/\d+/\d+\s*\d\d:\d+:\d+)\s*น?.?',row['Description'])
        print(index,"description",description,"src:",srcIP,"des:",desIP,"protocol",prot,"action",act,"time",time)
    # b   = re.search(r': (.*)\sเ',row['Description'])
    # print(index,description)
    # print(index,b)
    # list_data.append(dict_data)