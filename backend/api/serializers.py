from django.contrib.auth.models import *
from rest_framework import serializers
from .models import *


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = company_list
        fields = ['name_en', 'name_th', 'initials', 'join_date']


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = file_report
        fields = ['id', 'name', 'file', 'type']
