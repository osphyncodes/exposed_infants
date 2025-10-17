from django.urls import path
from . import views

app_name = 'hvl_management'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('collect-data/', views.collect_data, name='collect_data'),
    path('import-export/', views.import_export, name='import_export'),
    path('notifications/', views.notifications, name='notifications'), 
    path('api/get-hvl-data/', views.get_hvl_data, name='get_hvl_data'), 
    path('iac-sessions/', views.iac_sessions, name='iac_sessions'),

    path('case/<int:sn>/', views.hvl_case_detail, name='hvl_case_detail'),
    path('case/<int:sn>/add-iac-session/', views.add_iac_session, name='add_iac_session'),
    path('case/<int:sn>/add-iac-followup/', views.add_iac_followup, name='add_iac_followup'),
    path('case/<int:sn>/add-resistance-test/', views.add_resistance_test, name='add_resistance_test'),
    path('case/<int:sn>/notify-client/', views.notify_client, name='notify_client'),
]
