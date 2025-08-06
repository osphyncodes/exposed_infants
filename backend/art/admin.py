from django.contrib import admin
from .models import ChildVisit

class ChildVisitAdmin(admin.ModelAdmin):
    search_fields = ['patient__arv_number']
    autocomplete_fields = ['patient']

admin.site.register(ChildVisit, ChildVisitAdmin)
