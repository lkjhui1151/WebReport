import mysql.connector
from docxtpl import *

mydb = mysql.connector.connect(
    host="10.11.101.32",
    user="admin01@INETMS",
    password="P@ssw0rd@INETMS",
    database="inetms_autoreport"
)

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
doc = DocxTemplate(path+"templateSOC.docx")


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

device = []
vulnerability = []
create_index(device, device_DB)
create_index(vulnerability, vulnerability_DB)

contents = {}
img = "inet.png" if device_DB[0]['service_provider'] == "INET" else "inetms.png"
image = InlineImage(doc, path+img)
contents['img_provider'] =  image
contents['month_report'] = month_report
contents['Service_provider'] = "บริษัท อินเทอร์เน็ตประเทศไทย จำกัด (มหาชน)" if device_DB[0]['service_provider'] == "INET" else "บริษัท ไอเน็ต แมเนจด์ เซอร์วิสเซส จำกัด"
contents['name_capany'] = device_DB[0]['name_th']
contents['inet_create'] = 'บริษัท อินเทอร์เน็ตประเทศไทย จำกัด (มหาชน)'
contents['capa'] = '{:.4f}'.format(float(capa_DB[0]['AVG(value)']))
contents['vulnerability'] = vulnerability
contents['device'] = device

image = InlineImage(doc, path+"inet.png")
doc.render(contents)
doc.save(path+"SOC.docx")
# os.system(path+"SOC.docx")
