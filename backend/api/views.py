from .models import *
from .serializers import *
from rest_framework.response import Response
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework import status
import time
import os
from .sources.reportISO import report_iso


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
    data = file_report.objects.filter(type=type)
    serializer = ReportSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def CompanyAdd(request):
    print(request)
    name = request.data['fileName']
    file = request.FILES['file']
    file_type = request.data['type']
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
            # print("Name : ", name)
            # print("File : ", file)
            return Response(status.HTTP_200_OK)
        else:
            return Response("Error")
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


@api_view(['DELETE'])
def ReportDelete(request, pk):
    data = file_report.objects.get(id=pk)
    data.delete()
    return Response("Success")
