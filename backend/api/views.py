from attr import asdict
from .models import *
from .serializers import *
from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import os
from .sources.genarateDOCX import autoStart


@api_view(['GET'])
def CompanyList(request):
    data = company.objects.all().order_by('-id')
    serializer = CompanySerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def CompanyDetail(request, pk):
    data = company.objects.get(id=pk)
    serializer = CompanySerializer(data, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def CompanyAdd(request):
    name = request.data['fileName']
    file = request.FILES['file']
    # serializer = company_csv(name=name, file=file)
    # serializer.save()
    # data = autoStart(name)
    # name = name.split(".csv")
    if name != None:
        # company = company_csv.objects.values('id', 'name').order_by('-id')[:1]
        # docx = name[0]+".docx"
        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         "INSERT INTO company (name,file,csv_id) VALUES (%s,%s,%s)", [name[0], docx, company[0]["id"]])
        print("Name : ", name)
        print("File : ", file)
        return Response(status.HTTP_200_OK)
    else:
        return Response("Error")


@api_view(['GET'])
def CompanyDownload(request, pk):
    data = company.objects.get(id=pk)
    serializer = CompanySerializer(data, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def CompanyUpdate(request, pk):
    data = company.objects.get(id=pk)
    serializer = CompanySerializer(instance=data, data=request.data)

    if serializer.is_valid():
        return Response(status.HTTP_200_OK)
    else:
        return Response("Error")


@api_view(['DELETE'])
def CompanyDelete(request, pk):
    data = company.objects.get(id=pk)
    data.delete()
    return Response("Success")
