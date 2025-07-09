from django.urls import path
from . import views
app_name = "pact"

urlpatterns = [
    path('', views.pact_dashboard, name='pact_dashboard'),
    path('children/', views.children_view, name='children'),
    path('reports/', views.reports, name='reports'),
    path('reminders/', views.reminders, name='reminders'),
    path('import-export/', views.import_export, name='import_export'),
    path('logs/', views.logs, name='logs'),
]