from .models import *
from .serializers import *
from rest_framework.response import Response
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
            print("oK")
            # company = company_csv.objects.values('id', 'name').order_by('-id')[:1]
            # docx = name[0]+".docx"
            # with connection.cursor() as cursor:
            #     cursor.execute(
            #         "INSERT INTO company (name,file,csv_id) VALUES (%s,%s,%s)", [name[0], docx, company[0]["id"]])
            # print("Name : ", name)
            # print("File : ", file)
            return Response(status.HTTP_200_OK)
        else:
            return Response("Error")
    if file_type == 'nessus':
        pass
    if file_type == 'nessus infra':
        pass
    if file_type == 'nessus web':
        pass


@api_view(['DELETE'])
def ReportDelete(request, pk):
    data = file_report.objects.get(id=pk)
    data.delete()
    return Response("Success")
