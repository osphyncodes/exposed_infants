from django.contrib import admin
from tracing.models import Tracing,PhoneTracing,HomeTracing

# Register your models here.
admin.site.site_header = "Tracing Admin"
admin.site.site_title = "Tracing Admin Portal"
admin.site.index_title = "Welcome to the Tracing Admin Portal"

class tracingModel(admin.ModelAdmin):
    search_fields = ['unique_id']
admin.site.register(Tracing, tracingModel)
admin.site.register(PhoneTracing)
admin.site.register(HomeTracing)
