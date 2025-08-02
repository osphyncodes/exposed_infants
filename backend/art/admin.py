from django.contrib import admin
from .models import ChildVisit

class ChildVisitAdmin(admin.ModelAdmin):
    autocomplete_fields = ['patient']

admin.site.register(ChildVisit, ChildVisitAdmin)
