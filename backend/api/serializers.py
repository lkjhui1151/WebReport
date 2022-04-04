from statistics import mode
from attr import field
from django.contrib.auth.models import *
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = company
        fields = ['id', 'name', 'file', 'type', 'date']
