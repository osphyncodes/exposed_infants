from django.contrib import admin
from .models import *

class PatientAdmin(admin.ModelAdmin):
    search_fields = ('arv_number', 'name')

admin.site.register(
    [
        village, 
        Presentation,
        Survey,
        School,
        Staff,
        Guardian,
        Genotype
    ]
)

admin.site.register(Patient, PatientAdmin)


# Register your models here.
