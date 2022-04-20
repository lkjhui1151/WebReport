from .models import *
from .serializers import *
from rest_framework.response import Response
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework import status
import time
import os
import random
from .sources.reportISO import report_iso
from .sources.reportNessusinfra import report_infra
from .sources.reportNessusweb import report_web
from .sources.reportNessus import report_nessus


@api_view(['GET'])
def CompanyList(request):
    data = company_list.objects.all()
    serializer = CompanySerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def CompanyDetail(request, pk):
    data = company_list.objects.get(id=pk)
    serializer = CompanySerializer(data, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def ReportDetail(request, type):
    data = file_report.objects.filter(type=type).order_by('-id')
    serializer = ReportSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def ReportAddISO(request):
    fileOld = os.listdir('../backend/media/file')
    number = random.sample(range(10000000), 1)
    name = request.data['fileName']
    file = request.FILES['file']
    file_type = request.data['type']
    for item in fileOld:
        if item == name:
            items = item.split('.csv')
            nameNew = items[0]+"_"+str(number[0])+'.csv'
            os.rename(r'../backend/media/file/{}'.format(item),
                      r'../backend/media/file/{}'.format(nameNew))
    if file_type == 'iso':
        file_org = file_csv(name=name, file=file)
        file_org.save()
        data = report_iso(file)
        name = name.split(".csv")
        if data == True:
            docx = name[0]+".docx"
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO file_report (name,file,type) VALUES (%s,%s,%s)", [name[0], docx, "iso"])
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)
    directory = "../backend/media/file"
    files_in_directory = os.listdir(directory)
    filtered_files = [
        file for file in files_in_directory if file.endswith(".csv")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)
    directoryJson = "../backend/api/sources"

    files_in_directory = os.listdir(directoryJson)
    filtered_files = [
        file for file in files_in_directory if file.endswith(".json")]
    for file in filtered_files:
        path_to_file = os.path.join(directoryJson, file)
        os.remove(path_to_file)


@api_view(['POST'])
def ReportAddNessus(request):
    fileOld = os.listdir('../backend/media/file')
    number = random.sample(range(10000000), 1)
    file_nessus = ''
    file_burp = ''
    file_nmap = ''
    for name in request.data.getlist('fileName'):
        check = name.split("_")
        if check[-1] == 'nessus.csv':
            file_nessus = name
        elif check[-1] == 'burp.csv':
            file_burp = name
        elif check[-1] == 'nmap.csv':
            file_nmap = name

    for item in fileOld:
        if item == file_nessus:
            items = item.split('.csv')
            nameNew = items[0]+"_"+str(number[0])+'.csv'
            os.rename(r'../backend/media/file/{}'.format(item),
                      r'../backend/media/file/{}'.format(nameNew))
        elif item == file_burp:
            items = item.split('.csv')
            nameNew = items[0]+"_"+str(number[0])+'.csv'
            os.rename(r'../backend/media/file/{}'.format(item),
                      r'../backend/media/file/{}'.format(nameNew))
        elif item == file_nmap:
            items = item.split('.csv')
            nameNew = items[0]+"_"+str(number[0])+'.csv'
            os.rename(r'../backend/media/file/{}'.format(item),
                      r'../backend/media/file/{}'.format(nameNew))

    for files in request.FILES.getlist('file'):
        check = str(files).split("_")
        if check[-1] == 'nessus.csv':
            file_org = file_csv(name=file_nessus, file=files)
            file_org.save()
        elif check[-1] == 'burp.csv':
            file_org = file_csv(name=file_burp, file=files)
            file_org.save()
        elif check[-1] == 'nmap.csv':
            file_org = file_csv(name=file_nmap, file=files)
            file_org.save()

    data = report_nessus(file_nessus, file_burp, file_nmap)
    name = file_nessus.split(".csv")
    if data == True:
        docx = name[0]+".docx"
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO file_report (name,file,type) VALUES (%s,%s,%s)", [name[0], docx, "nessus"])
        return Response(status.HTTP_200_OK)
    else:
        return Response(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


@api_view(['POST'])
def ReportAddWeb(request):
    fileOld = os.listdir('../backend/media/file')
    number = random.sample(range(10000000), 1)
    burp = ""
    nmap = ""
    for name in request.data.getlist('fileName'):
        check = name.split("_")
        if check[-1] == 'burp.csv':
            burp = name
        elif check[-1] == 'nmapweb.csv':
            nmap = name
    for item in fileOld:
        if item == burp:
            items = item.split('.csv')
            nameNew = items[0]+"_"+str(number[0])+'.csv'
            os.rename(r'../backend/media/file/{}'.format(item),
                      r'../backend/media/file/{}'.format(nameNew))
        elif item == nmap:
            items = item.split('.csv')
            nameNew = items[0]+"_"+str(number[0])+'.csv'
            os.rename(r'../backend/media/file/{}'.format(item),
                      r'../backend/media/file/{}'.format(nameNew))
    for files in request.FILES.getlist('file'):
        check = str(files).split("_")
        if check[-1] == 'burp.csv':
            file_org = file_csv(name=burp, file=files)
            file_org.save()
        else:
            file_org = file_csv(name=nmap, file=files)
            file_org.save()

    data = report_web(burp, nmap)
    name = burp.split(".csv")
    if data == True:
        docx = name[0]+".docx"
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO file_report (name,file,type) VALUES (%s,%s,%s)", [name[0], docx, "web"])
        return Response(status.HTTP_200_OK)
    else:
        return Response(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


@api_view(['POST'])
def ReportAddInfra(request):
    fileOld = os.listdir('../backend/media/file')
    nessus = ""
    nmap = ""
    number = random.sample(range(10000000), 1)
    for name in request.data.getlist('fileName'):
        check = name.split("_")
        if check[-1] == 'nessus.csv':
            nessus = name
        elif check[-1] == 'nmapinfra.csv':
            nmap = name
    for item in fileOld:
        if item == nessus:
            items = item.split('.csv')
            nameNew = items[0]+"_"+str(number[0])+'.csv'
            os.rename(r'../backend/media/file/{}'.format(item),
                      r'../backend/media/file/{}'.format(nameNew))
        elif item == nmap:
            items = item.split('.csv')
            nameNew = items[0]+"_"+str(number[0])+'.csv'
            os.rename(r'../backend/media/file/{}'.format(item),
                      r'../backend/media/file/{}'.format(nameNew))
    for files in request.FILES.getlist('file'):
        check = str(files).split("_")
        if check[-1] == 'nessus.csv':
            file_org = file_csv(name=nessus, file=files)
            file_org.save()
        elif check[-1] == 'nmapinfra.csv':
            file_org = file_csv(name=nmap, file=files)
            file_org.save()

    data = report_infra(nessus, nmap)
    name = nessus.split(".csv")
    if data == True:
        docx = name[0]+".docx"
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO file_report (name,file,type) VALUES (%s,%s,%s)", [name[0], docx, "infra"])
        return Response(status.HTTP_200_OK)
    else:
        return Response(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


@api_view(['DELETE'])
def ReportDelete(request, pk):
    data = file_report.objects.get(id=pk)
    data.delete()
    return Response("Success")
