import csv
from docxtpl import *
import os
from matplotlib import pyplot as plt
import numpy as np


doc = DocxTemplate("E:/INETMS/doc/Auto gen report/VA ISO/WebReport/test2.docx")

countCri = 0
countHigh = 0
countMed = 0
countLow = 0
countInfo = 0
count = 0
context = {}
countIP =0



with open('E:/INETMS/doc/Auto gen report/VA ISO/WebReport/test code/A2.csv', encoding="utf8") as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
            if row['Group'] not in context:
                context[row['Group']] = {"Name":row['Group'] ,"device":{row['Host']} ,"Total_IP":0 ,"Critical":0 ,"High":0,"Medium":0,"Low":0,"Info":0}    
            else:
                #count total devices
                context[row['Group']]["device"].add(row['Host'])
                countIP = len(context[row['Group']]["device"])
                context[row['Group']]["Total_IP"] = countIP
            
            if row['Group'] == "":
                context[row['Group']]["Name"] = "etc"
            #Count amount of critaria in each group
            if row['Risk'] == "Critical":
                context[row['Group']]["Critical"]+=1
            elif row['Risk'] == "High":
                context[row['Group']]["High"]+=1
            elif row['Risk'] == "Medium":
                context[row['Group']]["Medium"]+=1
            elif row['Risk'] == "Low":
                context[row['Group']]["Low"]+=1
            elif row['Risk'] == "None":
                context[row['Group']]["Info"]+=1
            
    
# riskColor = {
#     'Critical': '#C20909',
#     'High': '#F09D1A',
#     'Medium': '#FFD80C',
#     'Low': '#23B800',
# }

# context = {
#     "vulnerability": [
#         {
#             'id': "1",
#             'address': "172.16.20.1,\n172.16.21.1,\n172.16.22.1,\n172.16.23.1",
#             'detail': "abc",
#             'risk': "Low",
#             'remask': "None",
#             'color': riskColor['Critical']
#         }
#     ]
# }
#print(countDevice)
#print(group)

l = list(context.values())
#print(len(l))
#print(l[0]["Name"])
#check if there are no group at all
#if len(l) == 1 and l[0]["Name"] == "etc":
#    l[0]["Name"] = "Cloud Name"
# total amount of vulnerabilities critaria
totalS = (sum([d['Total_IP'] for d in l]))
CriticalS = (sum([d['Critical'] for d in l]))
HighS = (sum([d['High'] for d in l]))
MediumS = (sum([d['Medium'] for d in l]))
LowS = (sum([d['Low'] for d in l]))
InfoS = (sum([d['Info'] for d in l]))
Amount = CriticalS+HighS+MediumS+LowS
dictS = {"Total_IP": totalS, "Critical":CriticalS, "High":HighS, "Medium": MediumS, "Low":LowS, "Info": InfoS}
percent = {"Critical":'%.2f' %(CriticalS*100/Amount), "High":'%.2f' %(HighS*100/Amount), "Medium": '%.2f' %(MediumS*100/Amount), "Low":'%.2f' %(LowS*100/Amount)}
# Final JSON output
l2 = {"Group":l, "Summary":dictS, "Percent":percent}
print(l2["Summary"]["High"])
#render word file
#print(percent.values())
doc.render(l2)
doc.save("generated_doc.docx")
os.system("generated_doc.docx")

#risk = [key for key,value in percent.items() if value!='0.00']
#values = [value for value in percent.values() if value!='0.00']


# Creating plot
#fig = plt.figure(figsize =(10, 7))
#plt.pie(values, labels=risk)
 
# show plot
#plt.show()

#risk = ['Critical','High', 'Medium','Low']
#values = [value for value in percent.values() if value!='0.00']

array = [
   {
        "risk": "Critical",
        "value": l2["Summary"]["Critical"],
        "colors": "#C20909"
    },
    {
        "risk": "High",
        "value": l2["Summary"]["High"],
        "colors": "#F09D1A"
    },
    {
        "risk": "Medium",
        "value": l2["Summary"]["Medium"],
        "colors": "#FFD80C"
    },
    {
        "risk": "Low",
        "value": l2["Summary"]["Critical"],
        "colors": "#23B800"
    }
]


plt.pie([i["value"] for i in array], labels=[i["risk"] for i in array], labeldistance=1.15, autopct= lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '' , colors=[i["colors"] for i in array])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0),
               fancybox=True, shadow=True, ncol=4)
plt.show()
#plt.savefig("D:/github/WebReport/backend/api/image/Graph.png")

