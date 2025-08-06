from django.urls import path
from . import views

app_name = "art"

urlpatterns = [
    path('', views.index, name='index'),
    path('patient/<int:patient_id>/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/<int:patient_id>/add-visit/', views.add_visit, name='add_visit'),
    path('patient/<int:visit_id>/edit/', views.edit_visit, name='edit_visit'),
    path('patient/<int:visit_id>/delete/', views.delete_visit, name='delete_visit'),
    path('reports/visit_stats/', views.visit_stats, name='visit_stats')
]
