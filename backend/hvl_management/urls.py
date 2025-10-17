from django.urls import path
from . import views

app_name = 'hvl_management'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('collect-data/', views.collect_data, name='collect_data'),
    path('import-export/', views.import_export, name='import_export'),
    path('notifications/', views.notifications, name='notifications'), 
    path('api/get-hvl-data/', views.get_hvl_data, name='get_hvl_data'), 
]
