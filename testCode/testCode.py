countGroupID = {}
vulnerability_url = []

for i in DataBurp:
    if DataBurp[i]['severity'] != 'Information':
        if DataBurp[i]['name'] in countGroupID:
            countGroupID[DataBurp[i]['name']] += 1
        else:
            countGroupID[DataBurp[i]['name']] = 1

def cleanCode(x):
    x = re.sub('</?[a-z]*>', "", x)
    return (x)

CriticalList = [DataBurp[i]['name']
                for i in DataBurp if DataBurp[i]['severity'] == 'Critical']
CriticalList = list(dict.fromkeys(CriticalList))

HighList = [DataBurp[i]['name']
            for i in DataBurp if DataBurp[i]['severity'] == 'High']
HighList = list(dict.fromkeys(HighList))

MediumList = [DataBurp[i]['name']
              for i in DataBurp if DataBurp[i]['severity'] == 'Medium']
MediumList = list(dict.fromkeys(MediumList))

LowList = [DataBurp[i]['name']
           for i in DataBurp if DataBurp[i]['severity'] == 'Low']
LowList = list(dict.fromkeys(LowList))

def DataCollection(**kwargs):
    global DataBurp
    global vulnerability_url
    global countGroupID
    for data in kwargs:
        for i in kwargs[data]:
            list_url = []
            subContent = {}
            # subContentLow = {}
            countCheck = 0
            for j in DataBurp:
                if DataBurp[j]['severity'] != 'Information':
                    if DataBurp[j]['name'] == i:
                        list_url.append(
                            DataBurp[j]['host/__text']+DataBurp[j]["location"])
                        countCheck += 1
                        # print(countCheck)
                        if countCheck == countGroupID[i]:
                            list_url = list(dict.fromkeys(list_url))
                            url = ""
                            for x in list_url:
                                if url == "":
                                    url = x
                                else:
                                    url = url + '\n' + x
                            list_ref = re.findall(
                                r'(http\S+)\"', DataBurp[j]['references'])
                            ref = ""
                            for temp in list_ref:
                                if ref == "":
                                    ref = temp
                                else:
                                    ref = ref + "\n" + temp
                            if data == "CriticalList":
                                if len(DataBurp[j]['host/__text'].split(":")) == 3:
                                    subContent["port"] = DataBurp[j]['host/__text'].split(":")[
                                        2].split('/')[0]
                                elif DataBurp[j]['host/__text'].split(":")[0] == "https":
                                    subContent["port"] = "443"
                                elif DataBurp[j]['host/__text'].split(":")[0] == "http":
                                    subContent["port"] = "80"
                                else:
                                    subContent["port"] = "N/A"
                                subContent["host"] = url
                                subContent["name"] = DataBurp[j]['name']
                                subContent["description"] = cleanCode(
                                    DataBurp[j]['issueBackground'])
                                subContent["solution"] = cleanCode(
                                    DataBurp[j]['remediationBackground'])
                                subContent["remark"] = ref
                                subContent["color"] = "#7030A0"
                                subContent["severity"] = 1
                                vulnerability_url.append(subContent)
                            if data == "HighList":
                                if len(DataBurp[j]['host/__text'].split(":")) == 3:
                                    subContent["port"] = DataBurp[j]['host/__text'].split(":")[
                                        2].split('/')[0]
                                elif DataBurp[j]['host/__text'].split(":")[0] == "https":
                                    subContent["port"] = "443"
                                elif DataBurp[j]['host/__text'].split(":")[0] == "http":
                                    subContent["port"] = "80"
                                else:
                                    subContent["port"] = "N/A"
                                subContent["host"] = url
                                subContent["name"] = DataBurp[j]['name']
                                subContent["description"] = cleanCode(
                                    DataBurp[j]['issueBackground'])
                                subContent["solution"] = cleanCode(
                                    DataBurp[j]['remediationBackground'])
                                subContent["remark"] = ref
                                subContent["color"] = "#FF0000"
                                subContent["severity"] = 2
                                vulnerability_url.append(subContent)
                            if data == "MediumList":
                                if len(DataBurp[j]['host/__text'].split(":")) == 3:
                                    subContent["port"] = DataBurp[j]['host/__text'].split(":")[
                                        2].split('/')[0]
                                elif DataBurp[j]['host/__text'].split(":")[0] == "https":
                                    subContent["port"] = "443"
                                elif DataBurp[j]['host/__text'].split(":")[0] == "http":
                                    subContent["port"] = "80"
                                else:
                                    subContent["port"] = "N/A"
                                subContent["host"] = url
                                subContent["name"] = DataBurp[j]['name']
                                subContent["description"] = cleanCode(
                                    DataBurp[j]['issueBackground'])
                                subContent["solution"] = cleanCode(
                                    DataBurp[j]['remediationBackground'])
                                subContent["remark"] = ref
                                subContent["color"] = "#FFC000"
                                subContent["severity"] = 3
                                vulnerability_url.append(subContent)
                            if data == "LowList":
                                if len(DataBurp[j]['host/__text'].split(":")) == 3:
                                    subContent["port"] = DataBurp[j]['host/__text'].split(":")[
                                        2].split('/')[0]
                                elif DataBurp[j]['host/__text'].split(":")[0] == "https":
                                    subContent["port"] = "443"
                                elif DataBurp[j]['host/__text'].split(":")[0] == "http":
                                    subContent["port"] = "80"
                                else:
                                    subContent["port"] = "N/A"
                                subContent["host"] = url
                                subContent["name"] = DataBurp[j]['name']
                                subContent["description"] = cleanCode(
                                    DataBurp[j]['issueBackground'])
                                subContent["solution"] = cleanCode(
                                    DataBurp[j]['remediationBackground'])
                                subContent["remark"] = ref
                                subContent["color"] = "#FFFF00"
                                subContent["severity"] = 4
                                vulnerability_url.append(subContent)


DataCollection(CriticalList=CriticalList, HighList=HighList,
               MediumList=MediumList, LowList=LowList)

def runIndex(e):
    return e['severity']

vulnerability_url.sort(key=runIndex, reverse=False)

for i in range(len(vulnerability_url)):
    vulnerability_url[i]['no'] = i+1
    if vulnerability_url[i]['severity'] == 1:
        vulnerability_url[i]['severity'] = "Critical"
    if vulnerability_url[i]['severity'] == 2:
        vulnerability_url[i]['severity'] = "High"
    if vulnerability_url[i]['severity'] == 3:
        vulnerability_url[i]['severity'] = "Medium"
    if vulnerability_url[i]['severity'] == 4:
        vulnerability_url[i]['severity'] = "Low"

try:
    with open('backend/api/sources/dataout.json', 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(vulnerability_url, indent=4))
except NameError as err:
    print(err)
except:
    with open('backend/api/sources/dataout.json', 'w', encoding='ISO-8859-1') as jsonf:
        jsonf.write(json.dumps(vulnerability_url, indent=4))