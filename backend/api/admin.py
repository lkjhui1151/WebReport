from django.contrib import admin
from .models import *

# Register your models here.


class Company(admin.ModelAdmin):
    list_display = ["id", "name", "file", "type", "date"]
    list_per_page = 10
    list_editable = ["name"]
    search_fields = ["date", "type"]
    list_filter = ["date"]


class CompanyCSV(admin.ModelAdmin):
    list_display = ["id", "name", "file"]
    list_per_page = 10
    search_fields = ["company"]


class Vulnerability(admin.ModelAdmin):
    list_display = ["id", "Plugin_ID", "Synopsis"]
    list_per_page = 10
    search_fields = ["Synopsis"]


admin.site.register(company, Company)
admin.site.register(company_csv, CompanyCSV)
admin.site.register(vulnerability, Vulnerability)
