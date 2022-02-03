from django.contrib import admin
from .models import *

# Register your models here.


class Company(admin.ModelAdmin):
    list_display = ["id", "name", "dete"]
    list_per_page = 10
    list_editable = ["name"]
    search_fields = ["name", "dete"]
    list_filter = ["dete"]


class Vulnerability(admin.ModelAdmin):
    list_display = ["id", "Plugin_ID", "Synopsis"]
    list_per_page = 10
    search_fields = ["Synopsis"]


admin.site.register(company, Company)
admin.site.register(vulnerability, Vulnerability)
