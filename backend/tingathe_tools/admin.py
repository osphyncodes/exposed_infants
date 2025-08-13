from django.contrib import admin
from .models import *


class ClientCardAdmin(admin.ModelAdmin):
    list_display = ('patient', 'unique_id', 'card_type', 'date_opened', 'status')
    search_fields = ['patient__arv_number',]

admin.site.register(ClientCard, ClientCardAdmin)

