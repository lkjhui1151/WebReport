from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import *
from .models import *


@api_view(['GET'])
def CompanyList(request):
    data = company.objects.all()
    serializer = CompanySerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def CompanyDetail(request, pk):
    data = company.objects.get(id=pk)
    serializer = CompanySerializer(data, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def CompanyAdd(request):
    serializer = CompanySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_200_OK)
    else:
        return Response("Error")


@api_view(['POST'])
def CompanyUpdate(request, pk):
    data = company.objects.get(id=pk)
    serializer = CompanySerializer(instance=data, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_200_OK)
    else:
        return Response("Error")


@api_view(['DELETE'])
def CompanyDelete(request, pk):
    data = company.objects.get(id=pk)
    data.delete()
    return Response("Success")
