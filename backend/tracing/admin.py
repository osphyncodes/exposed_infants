from django.contrib import admin
from tracing.models import Tracing

# Register your models here.
admin.site.site_header = "Tracing Admin"
admin.site.site_title = "Tracing Admin Portal"
admin.site.index_title = "Welcome to the Tracing Admin Portal"
admin.site.register(Tracing)
