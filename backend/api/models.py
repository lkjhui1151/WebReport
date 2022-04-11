from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import MinLengthValidator
import os
# Create your models here.

def file_path(instance, filename):
    path = ""
    format = filename
    return os.path.join(path, format)



class company_list(models.Model):
    name_en = models.CharField(max_length=100, null=True, blank=True)
    name_th = models.CharField(max_length=100, null=True, blank=True)
    initials = models.CharField(max_length=100, null=True, blank=True)
    join_date = models.DateField(auto_now_add=True, null=True, blank=True)
    service_provider = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.initials

    class Meta:
        db_table = 'company_list'
        verbose_name = "Company List"
        verbose_name_plural = "Company Table"


class address_list(models.Model):
    company = models.ForeignKey(
        company_list, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.address

    class Meta:
        db_table = 'address_list'
        verbose_name = "IP Address List"
        verbose_name_plural = "IP Address Table"


class device_type(models.Model):
    type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'device_type'
        verbose_name = "Device Type List"
        verbose_name_plural = "Device Type Table"


class device(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    device = models.ForeignKey(device_type, on_delete=models.CASCADE)
    company = models.ForeignKey(company_list, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'device'
        verbose_name = "Device List"
        verbose_name_plural = "Device Table"


class company_contact(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey(company_list, on_delete=models.CASCADE)

    class Meta:
        db_table = 'company_contact'
        verbose_name = "Contact List"
        verbose_name_plural = "Contact Table"


class trend(models.Model):
    type = models.CharField(max_length=100, null=True, blank=True)
    src_address = models.CharField(max_length=100, null=True, blank=True)
    des_address = models.CharField(max_length=100, null=True, blank=True)
    src_user = models.CharField(max_length=100, null=True, blank=True)
    des_user = models.CharField(max_length=100, null=True, blank=True)
    protocol = models.CharField(max_length=100, null=True, blank=True)
    port = models.CharField(max_length=100, null=True, blank=True)
    action = models.CharField(max_length=100, null=True, blank=True)
    last_datetime = models.DateTimeField(auto_now=False, null=True, blank=True)
    url = models.CharField(max_length=100, null=True, blank=True)
    file_path = models.CharField(max_length=100, null=True, blank=True)
    file_name = models.CharField(max_length=100, null=True, blank=True)
    malware_name = models.CharField(max_length=100, null=True, blank=True)
    src_geolocation = models.CharField(max_length=100, null=True, blank=True)
    des_geolocation = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey(company_list, on_delete=models.CASCADE)

    class Meta:
        db_table = 'trend'
        verbose_name = "Trend List"
        verbose_name_plural = "Trend Table"


class vulnerability(models.Model):
    category = models.CharField(max_length=100, null=True, blank=True)
    name_en = models.CharField(max_length=100, null=True, blank=True)
    name_th = models.CharField(max_length=100, null=True, blank=True)
    detail_en = models.TextField(null=True, blank=True)
    detail_th = models.TextField(null=True, blank=True)
    analysis_en = models.TextField(null=True, blank=True)
    analysis_th = models.TextField(null=True, blank=True)
    effect_en = models.TextField(null=True, blank=True)
    effect_th = models.TextField(null=True, blank=True)
    solution_en = models.TextField(null=True, blank=True)
    solution_th = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=100, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'vulnerability'
        verbose_name = "Vulnerability List"
        verbose_name_plural = "Vulnerability Table"


class capadailylog(models.Model):
    date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    value = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey(company_list, on_delete=models.CASCADE)

    class Meta:
        db_table = 'capa_daily_log'
        verbose_name = "Capa Daily Log List"
        verbose_name_plural = "Capa Daily Log Table"


class file_report(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to="report")
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return "ID : "+str(self.id)+" "+"FILE : "+self.name

    class Meta:
        ordering = ('id',)
        db_table = 'file_report'
        verbose_name = "File Report List"
        verbose_name_plural = "File Report Table"


class file_csv(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to="file")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID : "+str(self.id)+" "+"FILE : "+self.name

    class Meta:
        ordering = ('id',)
        db_table = 'file_csv'
        verbose_name = "File CSV List"
        verbose_name_plural = "File CSV Table"
