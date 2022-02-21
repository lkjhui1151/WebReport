from importlib.resources import path
from ntpath import join
from statistics import mode
from django.db import models
from django.core.validators import MinLengthValidator
from matplotlib.pyplot import cla
from django.db.models.deletion import CASCADE
import os


def file_path(instance, filename):
    path = ""
    format = filename
    return os.path.join(path, format)

# Create your models here.


class company_csv(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to=file_path)

    def __str__(self):
        return "ID : "+str(self.id)+" "+"FILE : "+self.name

    class Meta:
        ordering = ('id',)
        db_table = 'company_csv'
        verbose_name = "ORG File"
        verbose_name_plural = "ORG File"


class company(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to=file_path)
    csv = models.ForeignKey(
        company_csv, on_delete=CASCADE, null=True, blank=True)
    dete = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        db_table = 'company'
        verbose_name = "Company"
        verbose_name_plural = "Company List"


class vulnerability(models.Model):
    Plugin_ID = models.IntegerField(max_length=15, null=True, blank=True)
    CVE = models.CharField(max_length=50, null=True, blank=True)
    CVSS_v2_0_Base_Score = models.CharField(
        max_length=50, null=True, blank=True)
    Risk = models.CharField(max_length=50, null=True, blank=True)
    Host = models.CharField(max_length=50, null=True, blank=True)
    Protocol = models.CharField(max_length=50, null=True, blank=True)
    Port = models.IntegerField(max_length=50, null=True, blank=True)
    Name = models.CharField(max_length=100, null=True, blank=True)
    Synopsis = models.TextField(validators=[MinLengthValidator(20)])
    Description = models.TextField(validators=[MinLengthValidator(20)])
    Solution = models.TextField(validators=[MinLengthValidator(20)])
    See_Also = models.CharField(max_length=50, null=True, blank=True)
    Plugin_Output = models.TextField(validators=[MinLengthValidator(20)])
    STIG_Severity = models.CharField(max_length=50, null=True, blank=True)
    CVSS_v3_0_Base_Score = models.IntegerField(
        max_length=15, null=True, blank=True)
    CVSS_v2_0_Temporal_Score = models.IntegerField(
        max_length=15, null=True, blank=True)
    CVSS_v3_0_Temporal_Score = models.IntegerField(
        max_length=15, null=True, blank=True)
    Risk_Factor = models.CharField(max_length=50, null=True, blank=True)
    BID = models.IntegerField(max_length=15, null=True, blank=True)
    XREF = models.CharField(max_length=50, null=True, blank=True)
    MSKB = models.CharField(max_length=50, null=True, blank=True)
    Plugin_Publication_Date = models.CharField(
        max_length=50, null=True, blank=True)
    Plugin_Modification_Date = models.CharField(
        max_length=50, null=True, blank=True)
    Metasploit = models.CharField(max_length=50, null=True, blank=True)
    Core_Impact = models.CharField(max_length=50, null=True, blank=True)
    CANVAS = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.Plugin_ID

    class Meta:
        ordering = ('id',)
        verbose_name = "Vulnerability"
        verbose_name_plural = "Vulnerability List"
