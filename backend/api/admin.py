from django.contrib import admin
from .models import *

# Register your models here.
class Company(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_per_page = 10
    list_editable = ["name"]
    search_fields = ["name"]

admin.site.register(company, Company)