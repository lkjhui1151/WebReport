from ast import Global
from logging import critical
from statistics import median
from turtle import circle
from executing import Source
import mysql.connector
from docxtpl import *

mydb = mysql.connector.connect(
    host="10.11.101.32",
    user="admin01@INETMS",
    password="P@ssw0rd@INETMS",
    database="inetms_autoreport"
)


def count_event(data):
    count = 0
    for i in trend_DB:
        if i['priority'] == data:
            count += 1
    return count


def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def create_index(list, DB):
    temp_index = 1
    for i in DB:
        i['no'] = temp_index
        list.append(i)
        temp_index += 1
    return(list)


path = 'D:/INET-MS/Auto report/GitHub/WebReport/code_krit/report_SOC/'
doc = DocxTemplate(path+"templates/templateSOC.docx")


start_date = '2022-03-01'
end_date = '2022-04-01'
month_report = "มีนาคม 2565"
cus_name = "xspringam"

mycursor = mydb.cursor()

sql = "select category,name_en,detail_th,priority from vulnerability"
mycursor.execute(sql)
vulnerability_DB = dictfetchall(mycursor)

sql = "select name,address,remark,type,name_th,service_provider from device join company_list ON device.company_id = company_list.id join device_type ON device_type.id = device.device_id where company_list.initials = \""+cus_name+"\""
mycursor.execute(sql)
device_DB = dictfetchall(mycursor)

sql = "select AVG(value) from capa_daily_log join company_list ON company_list.id = capa_daily_log.company_id where company_list.initials = \"" + \
    cus_name+"\" and capa_daily_log.date between \"" + \
    start_date+"\" and \""+end_date+"\""
mycursor.execute(sql)
capa_DB = dictfetchall(mycursor)
# category,type,action,des_address,port,protocol,src_address,des_geolocation,last_datetime,priority,des_geolocation,solution_th,file_path,src_user,src_geolocation,des_user,file_name,malware_name
sql = "select * from trend join vulnerability on vulnerability.name_en = trend.type join company_list ON company_list.id =trend.company_id where company_list.initials = \""+cus_name+"\"and trend.last_datetime between \"" + \
    start_date+"\" and \""+end_date+"\""
mycursor.execute(sql)
trend_DB = dictfetchall(mycursor)


crit = count_event('Critical (P1)')
high = count_event('High (P2)')
medium = count_event('Medium (P3)')
low = count_event('Low (P4)')
sumPriority = int(crit)+int(high)+int(medium)+int(low)

device = []
vulnerability = []
create_index(device, device_DB)
create_index(vulnerability, vulnerability_DB)

head_tbl_vul_map = {'src_address': 'Source IP', 'des_address': 'Destination IP', 'src_geolocation': 'Source Geolocation', 'des_geolocation': 'Destination Geolocation', 'src_user': 'Source User', 'des_user': 'Destination User',
                    'port': 'Port', 'action': 'Event Subtype', 'last_datetime': 'Time', 'protocol': 'Protocol', 'url': 'URL', 'file_name': 'File Name', 'file_path': 'File Path', 'malware_name': 'Malware Name'}


head_tbl_vul = {'Inbound Communication With Blacklist IP Address': ['src_address', 'src_geolocation', 'des_address', 'port', 'action', 'last_datetime'],
                'Brute Force Login Attack Failed': [
                    'src_address', 'src_geolocation', 'src_user', 'des_address', 'last_datetime'],
                'Brute Force Login Attack Success': [
                    'src_address', 'src_geolocation', 'src_user', 'des_address', 'last_datetime'],
                'Outbound Communication with Blacklist IP Address Block': [
                    'src_address', 'des_address', 'des_geolocation', 'port', 'action', 'last_datetime'],
                'Outbound Communication with Blacklist IP Address Pass': [
                    'src_address', 'des_address', 'des_geolocation', 'port', 'action', 'last_datetime'],
                'SSH Access from Suspicious IP': [
                    'src_address', 'src_geolocation', 'des_address', 'action', 'last_datetime'],
                'RDP Access from Suspicious IP': [
                    'src_address', 'src_geolocation', 'des_address', 'action', 'last_datetime'],
                'Delegate Authentication Request': [
                    'src_address', 'src_user', 'des_address', 'des_user', 'action',  'last_datetime'],
                'SQL Injection (System Detect) Pass': [
                    'src_address', 'src_geolocation', 'des_address', 'action', 'last_datetime'],
                'Cross-Site Scripting (Custom Detected)': [
                    'src_address', 'src_geolocation', 'des_address', 'action', 'last_datetime'],
                'Virus or Spyware Detected': [
                    'src_address', 'des_address', 'des_geolocation', 'file_path', 'last_datetime'],
                'Virus or Spyware Detected But Failed to Clean': [
                    'src_address', 'des_address', 'des_geolocation', 'file_path', 'last_datetime'],
                'Port Sweep': [
                    'src_address', 'des_geolocation', 'port', 'last_datetime'],
                'Port Scan': ['src_address', 'des_geolocation', 'des_address', 'last_datetime']}


dict_group_event = {}
list_category = []
for i in trend_DB:
    list_category.append(i['category'])

    if i['type'] in dict_group_event:
        dict_group_event[i['type']] += 1
    else:
        dict_group_event[i['type']] = 1
list_category = list(dict.fromkeys(list_category))

new_dict_group_event = dict((k.lower(), v)
                            for k, v in dict_group_event .items())

list_group_category = []
for j in list_category:
    dict_group_category = {}
    list_event = []
    count = 0
    for i in vulnerability_DB:
        if j == i['category']:
            if i['name_en'].lower() in new_dict_group_event:
                event = {}
                event['type'] = i['name_en']
                event['priority'] = i['priority']
                event['count'] = new_dict_group_event[i['name_en'].lower()]
                count += new_dict_group_event[i['name_en'].lower()]
                list_event.append(event)
    dict_group_category['category'] = j
    dict_group_category['count'] = count
    dict_group_category['event'] = list_event
    list_group_category.append(dict_group_category)

count = 0
for i in list_group_category:
    count += i['count']

all_event_list = []
head_tbl_vul_new = []

for x in dict_group_event:
    one_event_dict = {}
    one_event_list = []

    for i in trend_DB:
        event = []
        event_dict = {}
        if x == i['type']:
            for j in head_tbl_vul[x]:
                event.append(i[j])
            event_dict['event'] = event
            one_event_list.append(event_dict)
            one_event_dict['cols'] = one_event_list
            one_event_dict['detail'] = i['solution_th']
            one_event_dict['vul'] = i['intro_th']

    head_tbl_vul_new = []
    for j in head_tbl_vul[x]:
        head_tbl_vul_new.append(head_tbl_vul_map[j])
    one_event_dict['col_label'] = head_tbl_vul_new
    all_event_list.append(one_event_dict)

contents = {}

img = "inet.png" if device_DB[0]['service_provider'] == "INET" else "inetms.png"
image = InlineImage(doc, path+img)
contents['img_provider'] = image
contents['month_report'] = month_report
contents['Service_provider'] = "บริษัท อินเทอร์เน็ตประเทศไทย จำกัด (มหาชน)" if device_DB[
    0]['service_provider'] == "INET" else "บริษัท ไอเน็ต แมเนจด์ เซอร์วิสเซส จำกัด"
contents['name_capany'] = device_DB[0]['name_th']

contents['capa'] = '{:.4f}'.format(float(capa_DB[0]['AVG(value)']))

contents['vulnerability'] = vulnerability

contents['device'] = device

contents['crit'] = crit
contents['medium'] = medium
contents['low'] = low
contents['sum'] = sumPriority

contents['high'] = high

contents['all_event'] = all_event_list

contents['category'] = list_group_category
contents['category_count'] = count


image = InlineImage(doc, path+"inet.png")
doc.render(contents)
doc.save(path+"output\SOC.docx")
# os.system(path+"SOC.docx")
