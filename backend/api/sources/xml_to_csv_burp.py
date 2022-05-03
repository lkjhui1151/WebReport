from xml.etree import ElementTree
import csv
import re
import os

tree = ElementTree.parse("D:/INET-MS/Auto report/GitHub/WebReport/backend/api/sources/iso/Burp.xml")
root = tree.getroot()

header1 = ['Risk', 'Name', 'Host', 'Domain',
           'Location', 'Description', 'Solution', 'References']


def cleanTags(raw_tag):
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(CLEANR, '', raw_tag)
    return cleantext


with open('burp.csv', mode='w', encoding='utf-8', newline="") as file:
    write_csv = csv.writer(file)
    write_csv.writerow(header1)

    for item in root:
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

        data = [severity, name, ip, domain,
                location, description, solution, remark]

        write_csv.writerow(data)

os.system('burp.csv')