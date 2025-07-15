from django.contrib import admin
from .models import Child, ChildVisit, HTSSample

# Register your models here.
class ChildAdmin(admin.ModelAdmin):
    search_fields = ('child_name', 'hcc_number', 'child_dob')

class ChildVisitAdmin(admin.ModelAdmin):
    list_display = ('child', 'visit_date', 'height', 'weight', 'muac', 'wasting', 'breastfeeding', 'mother_art_status', 'follow_up_outcome', 'next_appointment_or_outcome_date')
    list_filter = ('child', 'visit_date', 'wasting', 'breastfeeding')
    search_fields = ('child__child_name', 'child__hcc_number', 'visit_date')


admin.site.register(Child, ChildAdmin)
admin.site.register(ChildVisit, ChildVisitAdmin)
admin.site.register(HTSSample)
