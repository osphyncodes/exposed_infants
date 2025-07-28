from django.urls import path
from . import views
app_name = "pact"

urlpatterns = [
    path('', views.pact_dashboard, name='pact_dashboard'),
    path('children/', views.children_view, name='children'),
    path('children/chidren_dashboard/<str:art_number>/', views.children_dashboard_view, name='child_dashboard'),
    path('reports/', views.reports, name='reports'),
    path('reminders/', views.reminders, name='reminders'),
    path('import-export/', views.import_export, name='import_export'),
    path('logs/', views.logs, name='logs'),
    path('api/import/', views.import_patients, name='api_patient_import'),
    path('lab/import/', views.lab_import_view, name='lab_import'),
    path('api/lab/import/', views.import_lab_results, name='api_lab_import'),
    path('import/', views.import_view, name='patient_import'),
    path('api/regimen/import/', views.import_patient_data, name='api_regimen_import'),
]