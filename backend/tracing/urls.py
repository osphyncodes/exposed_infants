from django.urls import path
app_name = 'tracing'
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),   
    path('import', views.import_export, name='import_export'), 
    path('api/tracing/', views.import_tracing_data, name='api_tracing')
]
