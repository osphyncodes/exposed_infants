from django.contrib import admin
from .models import Child, ChildVisit, HTSSample

# Register your models here.
admin.site.register(Child)
admin.site.register(ChildVisit)
admin.site.register(HTSSample)
