import csv
import json
from multiprocessing import context
resk_per_ip = {}
range_ip = {}
context = {}
context2 = {}
#  = {}
with open('./A2.csv', encoding="utf8") as read_f:
    reader = csv.DictReader(read_f, delimiter=',')
    for row in reader:

        ip_splite = (row['Host'].split('.'))
        ip = ip_splite[0]+'.'+ip_splite[1]+'.'+ip_splite[2]+".xxx"

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

DataJson = open(
    "D:/INET-MS/Auto report/GitHub/WebReport/table3.json", "w")
DataJson.close()

csvFilePath = r'D:/INET-MS/Auto report/GitHub/WebReport/A2.csv'
jsonFilePath = r'D:/INET-MS/Auto report/GitHub/WebReport/table3.json'

makeJson(csvFilePath, jsonFilePath)





















#         # # if resk_per_ip['host'] != [row['Host']]:
#         # resk_per_ip['host'] = row['Host']

#         if ip in context:
#             if not row['Host'] in context[ip]:
#                 context[ip][row['Host']] = {
#                     "Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Summary": 0}
#         else:
#             context[ip] = {row['Host']: {
#                 "Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Summary": 0}}

#         if row['Risk'] != "None":
#             if row['Risk'] == "Critical":
#                 context[ip][row['Host']]["Critical"] += 1
#             elif row['Risk'] == "High":
#                 context[ip][row['Host']]["High"] += 1
#             elif row['Risk'] == "Medium":
#                 context[ip][row['Host']]["Medium"] += 1
#             elif row['Risk'] == "Low":
#                 context[ip][row['Host']]["Low"] += 1
#             context[ip][row['Host']]["Summary"] = context[ip][row['Host']]["Critical"]+context[ip
#                                                                                                ][row['Host']]["High"]+context[ip][row['Host']]["Medium"]+context[ip][row['Host']]["Low"]
# context2["valnerability"] = [context]
# print(context2)


# {'A': {'203.150.237.1': {'Critical': 0, 'High': 1, 'Medium': 1, 'Low': 0, 'Summary': 2}, '203.150.237.2': {'Critical': 0, 'High': 1, 'Medium': 1, 'Low': 0, 'Summary': 2}, '203.150.237.3': {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Summary': 0}, '203.150.237.4': {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Summary': 0}, '203.150.237.5': {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Summary': 0}, '203.150.237.6': {'Critical': 0, 'High': 0, 'Medium': 0,
# 'Low': 0, 'Summary': 0}, '203.150.237.7': {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Summary': 0}}, 'B': {'203.150.237.10': {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Summary': 0}, '203.150.237.11': {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Summary': 0}, '203.150.237.12': {'Critical': 0, 'High': 0, 'Medium': 2, 'Low': 0, 'Summary': 2}, '203.150.237.13': {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Summary': 0}, '203.150.237.14': {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Summary': 0}, '203.150.237.15': {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Summary': 0}, '203.150.237.8': {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Summary': 0}, '203.150.237.9':
# {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0, 'Summary': 0}}}
