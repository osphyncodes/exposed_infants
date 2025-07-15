from django.contrib import admin
from .models import Child, ChildVisit, HTSSample

# Register your models here.
class ChildAdmin(admin.ModelAdmin):
    search_fields = ('child_name', 'hcc_number', 'child_dob')

class ChildVisitAdmin(admin.ModelAdmin):
    search_fields = ('child__child_name', 'child__hcc_number', 'visit_date')


admin.site.register(Child, ChildAdmin)
admin.site.register(ChildVisit, ChildVisitAdmin)
admin.site.register(HTSSample)
