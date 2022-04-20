from django.contrib import admin
from .models import *

# Register your models here.


class CompanyList(admin.ModelAdmin):
    list_display = ["id", "name_en", "name_th",
                    "initials", "join_date", "service_provider"]
    list_per_page = 10
    search_fields = ["initials"]
    list_filter = ["join_date"]


admin.site.register(company_list, CompanyList)


class Device(admin.ModelAdmin):
    list_display = ["id", "name", "address", "company", "device"]
    list_per_page = 10
    list_filter = ["device", "company"]


admin.site.register(device, Device)


class DeviceType(admin.ModelAdmin):
    list_display = ["id", "type"]
    list_per_page = 10


admin.site.register(device_type, DeviceType)


class AddressList(admin.ModelAdmin):
    list_display = ["id", "address", "company"]
    list_per_page = 10
    list_filter = ["company"]


admin.site.register(address_list, AddressList)


class CompanyContact(admin.ModelAdmin):
    list_display = ["id", "name", "email", "phone", "company"]
    list_per_page = 10
    list_filter = ["company"]


admin.site.register(company_contact, CompanyContact)


class Trend(admin.ModelAdmin):
    list_display = ["id", "company", "type",
                    "src_address", "des_address", "last_datetime"]
    list_per_page = 10
    list_filter = ["company"]


admin.site.register(trend, Trend)


class Vulnerability(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ["id", "name_en", "priority"]
    list_per_page = 10
    list_filter = ["priority"]
    search_fields = ["name_en"]


admin.site.register(vulnerability, Vulnerability)


class CapaDaily(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ["id", "company", "date", "value"]
    list_per_page = 10
    list_filter = ["company"]


admin.site.register(capadailylog, CapaDaily)


class FileReport(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ["id", "name", "file", "date"]
    list_per_page = 10
    list_filter = ["date"]


admin.site.register(file_report, FileReport)


class FileCSV(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ["id", "name", "file", "date"]
    list_per_page = 10
    list_filter = ["date"]


admin.site.register(file_csv, FileCSV)
