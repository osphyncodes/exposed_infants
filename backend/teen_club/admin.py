from django.contrib import admin
from .models import *

# Register your models here.
class AttendanceAdmin(admin.ModelAdmin):
    search_fields = ['purpose']
    autocomplete_fields = ['patient']

admin.site.register( 
    [
    Session
    ]
)

admin.site.register(Attendance, AttendanceAdmin)

