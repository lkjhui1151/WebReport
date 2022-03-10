import csv
from docxtpl import *
from matplotlib import pyplot as plt
import json
import pandas
import matplotlib.patches as mpatches

doc = DocxTemplate("D:/github/WebReport/testCode/templateBurp.docx")

countCri = 0
countHigh = 0
countMed = 0
countLow = 0
countInfo = 0
count = 1
context = {}
countIP = 0
genGraph = 1


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


csvFilePath = r'D:/github/WebReport/testCode/Burp.csv'
jsonFilePath = r'D:/github/WebReport/testCode/dataFile.json'

makeJson(csvFilePath, jsonFilePath)

DataJSON = pandas.read_json(jsonFilePath)

GroupName1 = {}
GroupName2 = []

# Create New Data Source
for row in DataJSON:
    GroupName1["Risk"] = DataJSON[row]["severity"]
    GroupName1["ip"] = DataJSON[row]["host/_ip"]
    GroupName1["url"] = DataJSON[row]["host/__text"]
    GroupName1["Group"] = DataJSON[row]["host/__text"]
    GroupName1["path"] = DataJSON[row]["path"]
    GroupName1["location"] = DataJSON[row]["location"]
    GroupName1["issue"] = DataJSON[row]["issueBackground"]
    GroupName1["solution"] = DataJSON[row]["remediationBackground"]
    GroupName1["references"] = DataJSON[row]["references"]
    GroupName1["detail"] = DataJSON[row]["issueDetail"]
    GroupName2.append(GroupName1)
    GroupName1 = {}

# # Remove Data is duplicate
results = [dict(t) for t in {tuple(d.items()) for d in GroupName2}]
newlist = sorted(results, key=lambda d: d['Group'])


for row in newlist:
    if row['Group'] not in context:
        context[row['Group']] = {"No": count, "Name": row['ip'], "url": row['url'],
                                 "Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Total": 0}
        count += 1

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


# # print(context)

l = list(context.values())

totalS = (sum([d['Total'] for d in l]))
CriticalS = (sum([d['Critical'] for d in l]))
HighS = (sum([d['High'] for d in l]))
MediumS = (sum([d['Medium'] for d in l]))
LowS = (sum([d['Low'] for d in l]))
#InfoS = (sum([d['Info'] for d in l]))
Amount = CriticalS+HighS+MediumS+LowS
#Amount = 0
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

l2 = {"table1": {"Group": l, "Summary": dictS, "Percent": percent}}

# +++++++++++++++++++++++++++++== FIX HERE +++++++++++++++++++++++++++++++++++++
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
# +++++++++++++++++++++++++++++== FIX HERE +++++++++++++++++++++++++++++++++++++
fig, ax = plt.subplots()
Critical = mpatches.Patch(
    color="#7030A0", label='Critical')
High = mpatches.Patch(
    color="#FF0000", label='High')
Medium = mpatches.Patch(
    color="#FFC000", label='Medium')
Low = mpatches.Patch(
    color="#FFFF00", label='Low')
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if genGraph != 0:
    # +++++++++++++++++++++++++++++== FIX HERE +++++++++++++++++++++++++++++++++++++
    value = [i["value"] for i in array if i["value"] != 0]
    plt.pie(value, labels=[i["labels"] for i in array if i["value"] != 0], colors=[
            i["colors"] for i in array if i["value"] != 0], pctdistance=1.2)
    plt.title('Summary Vulnerability by Severity', y=1.05, fontsize=15)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0),
               fancybox=True, shadow=True, ncol=4, handles=[Critical, High, Medium, Low])
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    plt.savefig("D:/github/WebReport/testCode/Overview_Graph.png")

    doc.replace_media("D:/github/WebReport/testCode/1.png",
                      "D:/github/WebReport/testCode/Overview_Graph.png")
doc.render(l2)
# print(l2)

doc.save("D:/github/WebReport/testCode/generated_doc.docx")
