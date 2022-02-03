
from rest_framework import viewsets
from .serializers import *
from .models import *


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = company.objects.all()
    serializer_class = CompanySerializer
