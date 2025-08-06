from django.contrib import admin
from .models import ChildICT

# Register your models here.
class ChildICTAdmin(admin.ModelAdmin):
    autocomplete_fields = ['mother']
admin.site.register(ChildICT)