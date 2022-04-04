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
    type = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

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


# class company_list(models.Model):
#     name_en = models.CharField(max_length=100, null=True, blank=True)
#     name_th = models.CharField(max_length=100, null=True, blank=True)
#     initials = models.CharField(max_length=100, null=True, blank=True)
#     join_date = models.DateField(auto_now_add=True)

#     class Meta:
#         db_table = 'company_list'


# class address_list(models.Model):
#     company_id = models.ForeignKey(company_list, on_delete=models.CASCADE)
#     address = models.CharField(max_length=100, null=True, blank=True)

#     class Meta:
#         db_table = 'address_list'


# class device_type(models.Model):
#     type = models.CharField(max_length=100, null=True, blank=True)

#     class Meta:
#         db_table = 'device_type'


# class device(models.Model):
#     name = models.CharField(max_length=100, null=True, blank=True)
#     address = models.CharField(max_length=100, null=True, blank=True)
#     remark = models.CharField(max_length=100, null=True, blank=True)
#     device_id = models.ForeignKey(device_type, on_delete=models.CASCADE)
#     company_id = models.ForeignKey(company_list, on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'device'


# class company_contact(models.Model):
#     first_name_en = models.CharField(max_length=100, null=True, blank=True)
#     last_name_en = models.CharField(max_length=100, null=True, blank=True)
#     first_name_th = models.CharField(max_length=100, null=True, blank=True)
#     last_name_th = models.CharField(max_length=100, null=True, blank=True)
#     email = models.CharField(max_length=100, null=True, blank=True)
#     phone = models.IntegerField(max_length=100, null=True, blank=True)
#     company_id = models.ForeignKey(company_list, on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'company_contact'


# class trend(models.Model):
#     type = models.CharField(max_length=100, null=True, blank=True)
#     critical = models.IntegerField(max_length=100, null=True, blank=True)
#     high = models.IntegerField(max_length=100, null=True, blank=True)
#     medium = models.IntegerField(max_length=100, null=True, blank=True)
#     low = models.IntegerField(max_length=100, null=True, blank=True)
#     company_id = models.ForeignKey(company_list, on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'trend'


# class vulnerability(models.Model):
#     category = models.CharField(max_length=100, null=True, blank=True)
#     name_en = models.CharField(max_length=100, null=True, blank=True)
#     name_th = models.CharField(max_length=100, null=True, blank=True)
#     detail_en = models.TextField(validators=[MinLengthValidator(20)])
#     detail_th = models.TextField(validators=[MinLengthValidator(20)])
#     solution_en = models.TextField(validators=[MinLengthValidator(20)])
#     solution_th = models.TextField(validators=[MinLengthValidator(20)])
#     priority = models.CharField(max_length=100, null=True, blank=True)
#     remark = models.CharField(max_length=100, null=True, blank=True)
#     company_id = models.ForeignKey(company_list, on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'vulnerability'
