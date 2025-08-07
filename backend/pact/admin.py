from django.contrib import admin
from .models import *

class PatientAdmin(admin.ModelAdmin):
    search_fields = ('arv_number', 'name')

class LabAdmin(admin.ModelAdmin):
    autocomplete_fields = ['patient']
    search_fields = ['order_date','patient__arv_number']

admin.site.register(
    [
        village, 
        Presentation,
        Survey,
        School,
        Staff,
        Guardian,
        Genotype,
    ]
)

admin.site.register(Patient, PatientAdmin)
admin.site.register(LabResult, LabAdmin)


# Register your models here.
